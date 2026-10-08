# INCIDENT REPORT: Operation Silent SSH

| Field | Value |
|---|---|
| **Report ID** | IR-2026-1008-001 |
| **Analyst** | Evans Davou |
| **Date** | 2026-10-08 |
| **Severity** | High |
| **Status** | Resolved (Simulated) |

---

## 1. Executive Summary

A simulated phishing campaign compromised the `victim` account on an Ubuntu Server (192.168.56.101). The attacker (Kali Linux, 192.168.56.10) hosted a fake SSO login page, harvested credentials, and used them to authenticate via SSH.

Detection was achieved via `/var/log/auth.log`, `auditd`, and `systemd-logind`. The complete attack chain took under 5 minutes.

---

## 2. Lab Environment

| Role | OS | IP |
|---|---|---|
| Attacker | Kali Linux 2026.4 | 192.168.56.10 |
| Victim | Ubuntu Server 26.04.1 LTS | 192.168.56.101 |
| Network | VirtualBox Host-Only | 192.168.56.0/24 |

---

## 3. Attack Timeline

| Time (UTC) | Event |
|---|---|
| 15:57:10 | Phishing server started on Kali:80 |
| 16:00:39 | Victim submitted credentials |
| 15:01:49 | SSH login as `victim` from Kali |
| 15:01:52 | auditd logs session init |
| 15:02:04 | Attacker logs out; `.bash_history` written |

---

## 4. Detection Evidence

### auth.log

```
2026-10-08T15:01:49.190933+00:00 bby sshd-session[49264]:
Accepted password for victim from 192.168.56.10 port 40850 ssh2
```

### systemd-logind

```
2026-10-08T15:01:49.263178+00:00 bby systemd-logind[821]:
New session '5' of user 'victim' with class 'user' and type 'tty'.
```

### auditd

```
type=SYSCALL msg=audit(1791471712.629:664):
  comm="sshd-session" auid=1003 ses=5 key="victim_home"
```

### Attacker Commands Recovered

```
whoami
id
hostname
ls -la /home/victim
cat /etc/passwd | head
exit
```

### Session Correlation

| Source | Session ID | Timestamp |
|---|---|---|
| `auth.log` | — | 15:01:49 |
| `systemd-logind` | 5 | 15:01:49 |
| `auditd` (sshd) | 5 | 15:01:52 |
| `auditd` (bash) | 5 | 15:02:04 |

---

## 5. MITRE ATT&CK Mapping

| Tactic | Technique | ID |
|---|---|---|
| Initial Access | Spearphishing Link | T1566.002 |
| Credential Access | Input Capture: Web Portal | T1056.003 |
| Initial Access | Valid Accounts: Local | T1078.003 |
| Discovery | System Owner/User Discovery | T1033 |
| Discovery | Account Discovery: Local | T1087.001 |
| Lateral Movement | Remote Services: SSH | T1021.004 |
| Collection | Data from Local System | T1005 |

---

## 6. Root Cause

1. Weak password (`Password123`)
2. No MFA on SSH
3. Password authentication enabled
4. No login alerting
5. No IP allowlist
6. User submitted credentials to a fake page

---

## 7. Recommendations

### Immediate
- Disable SSH password authentication (use keys + MFA)
- Install `fail2ban`
- Restrict SSH by source IP
- Real-time alerts on every SSH login

### Short-Term
- Phishing awareness training
- Deploy Wazuh/Splunk for log correlation
- Harden SSH: `PermitRootLogin no`, `MaxAuthTries 3`

### Long-Term
- Zero Trust architecture
- JIT privileged access
- Continuous phishing simulations

---

## 8. Conclusion

Identity-based threats remain the most effective attack vector in 2026. Every step of the attack was detectable with native Linux logging — but only because logging was configured in advance. **MFA would have stopped the attack entirely.**

**Risk (pre-mitigation):** 🔴 High
**Risk (post-mitigation):** 🟢 Low
