# AI Chatbot

this is a lightweight discord ai bot designed to live 24/7 on a raspberry pi 3. it is built to be fast, stable, and completely hands-off once it is ran.

## features
* **immortality**: uses `systemd` to auto-restart if it crashes or if the pi reboots.
* **speed**: runs on the groq api for instant gpt-style responses (gpt-oss-20b).
* **low power**: optimized specifically for the 1gb ram limit of the raspberry pi 3.
* **global reach**: supports slash commands in servers and personal dms.
* **10 commands**: ai, ping, stats, roll, coin, 8ball, joke, uptime, avatar, serverinfo.

## commands
| command | what it does |
|---------|-------------|
| `/ai <prompt>` | ask gpt-oss-20b anything |
| `/ping` | bot latency |
| `/stats` | pi ram, cpu, uptime, temp |
| `/roll 2d6` | roll dice |
| `/coin` | flip a coin |
| `/8ball <question>` | magic 8 ball |
| `/joke` | random joke |
| `/uptime` | how long the bot has been alive |
| `/avatar [user]` | get someone's avatar |
| `/serverinfo` | server info |

## prerequisites
- raspberry pi 3 with raspberry pi 64 lite on it.
- python 3.10+.
- a groq api key.
- a discord bot token.

## installation

### 1. prepare the pi
ssh into your raspberry pi and create the project folder:

mkdir discord_bot && cd discord_bot
pip install discord.py groq psutil requests

### 2. setup secret keys

the bot reads credentials from separate text files so you don't leak them in your code. create these two files in your folder:

    Discord.txt: paste your discord bot token here.

    AI.txt: paste your groq api key here.

### 3. the main script (Main.py)

create the file with nano Main.py and paste the code in this repository.

### 4. make it run in the background

create a service file so the bot runs 24/7 without needing an open terminal:

sudo cp discord-bot.service /etc/systemd/system/
sudo systemctl enable --now discord-bot

### 5. check it's alive

sudo systemctl status discord-bot

###Congrats! it should work now.