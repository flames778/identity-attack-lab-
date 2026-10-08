# 🎯 Operation Silent SSH

> A purple team lab simulating the #1 cyber threat of 2026: **identity-based attacks** — phishing, credential theft, and SSH account takeover.

![Status](https://img.shields.io/badge/status-complete-success)
![Platform](https://img.shields.io/badge/platform-Kali%20%7C%20Ubuntu-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![MITRE](https://img.shields.io/badge/MITRE-ATT%26CK-red)

---

## 📖 Overview

This lab demonstrates how a modern attacker can:

1. Host a convincing phishing page
2. Harvest credentials from a victim
3. Use those credentials to log into a remote system via SSH
4. Perform post-exploitation discovery

...**and** how a defender can detect every step using native Linux logging.

The lab is based on real-world trends from:
- CrowdStrike 2026 Global Threat Report
- INTERPOL African Cyberthreat Assessment 2026
- Palo Alto Unit 42 2026 Incident Response Report
- WEF Global Cybersecurity Outlook 2026

All of these identify **identity attacks** as the dominant threat vector in 2026.

---

## 🏗️ Lab Architecture

```
┌─────────────────────┐         ┌─────────────────────┐
│   KALI LINUX        │         │   UBUNTU SERVER     │
│   (Attacker)        │         │   (Victim)          │
│   192.168.56.10     │◄───────►│   192.168.56.101    │
│                     │         │                     │
│  • Flask phishing   │         │  • SSH server       │
│  • SSH client       │         │  • victim user      │
│  • creds.txt        │         │  • auditd           │
└─────────────────────┘         └─────────────────────┘
         │                                │
         │    VirtualBox Host-Only        │
         └──────── 192.168.56.0/24 ───────┘
```

---

## 🎬 Attack Chain

| Phase | Action | Result |
|---|---|---|
| 1 | Phishing page served on Kali:80 | Victim reaches fake SSO login |
| 2 | Victim submits credentials | `creds.txt` populated |
| 3 | Attacker SSHes with stolen creds | Account takeover |
| 4 | Post-exploitation discovery | `whoami`, `id`, `cat /etc/passwd` |
| 5 | Detection | `auth.log`, `auditd`, `systemd-logind` fire |

---

## ⏱️ Timeline

| Time (UTC) | Event | Source |
|---|---|---|
| 14:27 | `victim` account created | `adduser` |
| 14:46 | auditd watch rules configured | `auditctl` |
| 15:57 | Phishing server started | Flask |
| 16:00:39 | Credentials captured | `creds.txt` |
| 15:01:49 | SSH login as `victim` | `auth.log` |
| 15:01:52 | auditd logs session init | `ausearch` |
| 15:02:04 | Attacker exits; `.bash_history` written | `ausearch` |
| 15:02:04 | Session closed | `auth.log` |

Full timeline: see [`incident-report.md`](incident-report.md).

---

## 🛠️ Tools Used

| Category | Tool | Purpose |
|---|---|---|
| Attacker | Python 3 + Flask | Fake SSO login page |
| Attacker | OpenSSH client | Account takeover |
| Attacker | curl | Simulate victim submission |
| Victim | Ubuntu Server 26.04 | Target host |
| Victim | OpenSSH server | Entry point |
| Detection | auditd | Filesystem auditing |
| Detection | journald / auth.log | Auth event logging |
| Detection | systemd-logind | Session tracking |

---

## 📊 MITRE ATT&CK Coverage

| Tactic | Technique | ID |
|---|---|---|
| Reconnaissance | Active Scanning | T1595 |
| Resource Development | Acquire Infrastructure: Server | T1583.005 |
| Initial Access | Spearphishing Link | T1566.002 |
| Credential Access | Input Capture: Web Portal | T1056.003 |
| Initial Access | Valid Accounts: Local | T1078.003 |
| Discovery | System Owner/User Discovery | T1033 |
| Discovery | Account Discovery: Local | T1087.001 |
| Lateral Movement | Remote Services: SSH | T1021.004 |
| Collection | Data from Local System | T1005 |
| Defense Evasion | Indicator Removal (NOT used) | T1070.003 |

Load the layer in [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) using [`mitre/attack-layer.json`](mitre/attack-layer.json).

---

## 🚨 Key Findings

**For attackers:**
- Phishing remains the cheapest, fastest initial access vector
- A single captured password = full remote access
- No malware required — "living off the land" with SSH

**For defenders:**
- Every step was detectable using native Linux logging
- Session IDs (`ses=`) correlate events across 4 log sources
- `.bash_history` is forensic gold — attackers often forget to clear it
- **MFA would have stopped this attack completely**

---

## 🧪 Reproduce the Lab

### Prerequisites
- VirtualBox (or VMware)
- Kali Linux VM
- Ubuntu Server VM
- 16 GB RAM minimum

### Steps

1. **Set both VMs to Host-Only network** (`192.168.56.0/24`)
2. **On Ubuntu:**
   ```bash
   sudo adduser victim
   echo "PasswordAuthentication yes" | sudo tee /etc/ssh/sshd_config.d/99-lab.conf
   sudo systemctl restart ssh
   sudo apt install -y auditd
   sudo auditctl -w /home/victim -p wa -k victim_home
   ```
3. **On Kali:**
   ```bash
   cd attack
   sudo python3 phish.py
   ```
4. **From Ubuntu:** simulate victim
   ```bash
   curl -X POST http://192.168.56.10/ \
     -d "username=victim@company.local" \
     -d "password=Password123"
   ```
5. **From Kali:** use stolen creds
   ```bash
   ssh victim@192.168.56.101
   ```
6. **From Ubuntu:** detect
   ```bash
   sudo grep "Accepted password" /var/log/auth.log
   sudo ausearch -k victim_home -ts today
   sudo cat /home/victim/.bash_history
   ```

---

## 📁 Repository Structure

```
├── README.md
├── LICENSE
├── .gitignore
├── incident-report.md          # Full IR write-up
├── attack/
│   └── phish.py                # Flask phishing server
├── detection/
│   ├── detect.sh               # Real-time alert script
│   └── splunk-queries.spl      # SIEM detection queries
├── evidence/                   # Raw log evidence
├── mitre/
│   └── attack-layer.json       # ATT&CK Navigator layer
└── screenshots/                # 18 documented screenshots
```

---

## ⚖️ Legal Disclaimer

This lab was performed in an **isolated, host-only network** with no external connectivity. All IPs are private (`192.168.56.0/24`). No real systems, credentials, or user data were involved.

**Never run these techniques against systems you don't own or have written authorization to test.**

---

## 📚 References

- [CrowdStrike 2026 Global Threat Report](https://www.crowdstrike.com/en-gb/global-threat-report/)
- [INTERPOL African Cyberthreat Assessment 2026](https://www.interpol.int/)
- [Palo Alto Unit 42 2026 IR Report](https://www.paloaltonetworks.com/)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [WEF Global Cybersecurity Outlook 2026](https://www.weforum.org/)
- [ENISA Threat Landscape 2026](https://www.enisa.europa.eu/)

---

## 👤 Author

**Evans Davou**
Cybersecurity Student | Purple Team Enthusiast

- GitHub: [@flames778](https://github.com/flames778)
- LinkedIn: [Evans Davou](https://www.linkedin.com/in/evansdavou)

---

## 📝 License

MIT — see [LICENSE](LICENSE) for details.
