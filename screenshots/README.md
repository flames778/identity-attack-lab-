# Screenshots Index

| # | Filename | Description |
|---|---|---|
| 01 | `01-kali-network.png` | Kali ifconfig showing 192.168.56.10 on host-only adapter |
| 02 | `02-kali-phish-server-start.png` | Flask server starting on port 80 |
| 03 | `03-kali-phish-page-localhost.png` | Phishing login page rendered in browser |
| 04 | `04-kali-phish-capture-live.png` | Terminal showing live credential capture |
| 05 | `05-kali-creds-file.png` | `cat creds.txt` showing captured credentials |
| 06 | `06-kali-ssh-takeover.png` | SSH session established as `victim` user |
| 07 | `07-kali-discovery.png` | Post-exploitation: whoami, id, hostname, ls, passwd |
| 08 | `08-ubuntu-network.png` | Ubuntu ifconfig showing 192.168.56.101 |
| 09 | `09-ubuntu-victim-user.png` | `id victim` and `/etc/passwd` entry |
| 10 | `10-ubuntu-curl-phish.png` | curl command simulating victim credential submission |
| 11 | `11-ubuntu-curl-post.png` | curl POST response (redirect HTML) |
| 12 | `12-ubuntu-authlog-login.png` | `auth.log` showing "Accepted password for victim" |
| 13 | `13-ubuntu-last-logins.png` | `last -a` showing session from 192.168.56.10 |
| 14a | `14a-ubuntu-ausearch-tail.png` | auditd: sshd-session event with ses=5 |
| 14b | `14b-ubuntu-bash-history.png` | auditd: bash history write event on exit |
| 15 | `15-ubuntu-systemd-sessions.png` | journalctl showing systemd-logind session 5 |
| 16 | `16-mitre-navigator.png` | ATT&CK Navigator layer with highlighted techniques |
| 17 | `17-lab-architecture.png` | Network diagram of the lab setup |
| 18 | `18-final-verification.png` | Side-by-side: attack terminal + detection terminal |

## How to Capture

Screenshots should be taken in order during the lab run.
Use `scrot`, `gnome-screenshot`, or your VM's screenshot tool.
Crop to relevant content; include terminal title bars for context.
