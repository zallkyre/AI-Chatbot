<div align="center">

# 🤖 AI Chatbot

**A lightweight Discord AI bot that lives 24/7 on a Raspberry Pi 3**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2.svg)](https://discordpy.readthedocs.io/)
[![Groq](https://img.shields.io/badge/Groq-gpt--oss--20b-orange.svg)](https://groq.com/)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-3-red.svg)](https://www.raspberrypi.com/)

Fast. Stable. Hands-off. Built for the 1 GB RAM limit of the Pi 3.

</div>

---

## ✨ Features

| | |
|---|---|
| 🧠 **AI-powered** | Answers via Groq's `gpt-oss-20b` — instant responses, no GPU needed |
| 💀 **Immortal** | `systemd` auto-restarts it on crash or reboot. You never touch it again |
| ⚡ **Fast** | Groq API = sub-second replies, even on a Pi 3 |
| 🔋 **Low power** | Optimized for 1 GB RAM — idles at ~170 MB |
| 🌍 **Global reach** | Slash commands work in servers *and* DMs |
| 🎮 **10 commands** | AI, dice, 8-ball, jokes, Pi stats, and more |

---

## 🎮 Commands

| Command | What it does |
|---------|-------------|
| `/ai <prompt>` | Ask gpt-oss-20b anything |
| `/ping` | Bot latency |
| `/stats` | Pi RAM, CPU, uptime, temperature |
| `/roll 2d6` | Roll dice (any format, e.g. `3d20`) |
| `/coin` | Flip a coin |
| `/8ball <question>` | Consult the magic 8-ball |
| `/joke` | Random programmer joke |
| `/uptime` | How long the bot has been alive |
| `/avatar [user]` | Grab someone's avatar |
| `/serverinfo` | Server member count + creation date |

---

## 🛠️ Installation

### 1. Prepare the Pi

```bash
ssh zallkyre@<pi-ip>
mkdir discord_bot && cd discord_bot
pip install discord.py groq psutil requests
```

### 2. Add your secrets

The bot reads credentials from text files so they never end up in your code:

```bash
nano Discord.txt   # paste your Discord bot token
nano AI.txt        # paste your Groq API key
```

### 3. Add the code

```bash
nano Main.py       # paste the code from this repo
```

### 4. Run it forever with systemd

```bash
sudo cp discord-bot.service /etc/systemd/system/
sudo systemctl enable --now discord-bot
```

### 5. Verify

```bash
sudo systemctl status discord-bot
```

You should see `active (running)` and the bot online in Discord.

---

## 🔧 Troubleshooting

| Problem | Fix |
|---------|-----|
| Bot not coming online | Check the token in `Discord.txt` — regenerate it in the [Discord Developer Portal](https://discord.com/developers/applications) |
| `/ai` returns errors | Check the key in `AI.txt` — regenerate at [console.groq.com/keys](https://console.groq.com/keys) |
| Service keeps restarting | `journalctl -u discord-bot -n 50` to see the actual error |
| Slash commands missing | The bot syncs commands on startup — give it ~10 seconds after boot |

---

## 🧠 How it works

```
Discord ──slash command──▶ Pi 3 (systemd service)
                              │
                              ▼
                         Groq API (gpt-oss-20b)
                              │
                              ▼
                      instant reply ──▶ Discord
```

---

## 📜 License

MIT — do whatever you want with it.

<div align="center">

**Made with ❤️ and a Raspberry Pi**

</div>