# AI Chatbot

this is a lightweight discord ai bot designed to live 24/7 on a raspberry pi 3. it is built to be fast, stable, and completely hands-off once it is ran.

## features
* **immortality**: uses `systemd` to auto-restart if it crashes or if the pi reboots.
* **speed**: runs on the groq api for instant gpt-style responses (gpt-oss-20b).
* **low power**: optimized specifically for the 1gb ram limit of the raspberry pi 3.
* **health checks**: pings a discord webhook every 15 minutes with cpu, ram, and network status.
* **global reach**: supports slash commands in servers and personal dms.

## prerequisites
- raspberry pi 3 with raspberry pi 64 lite on it.
- python 3.10+.
- a groq api key.
- a discord bot token.
- a discord channel webhook

## installation

### 1. prepare the pi
ssh into your raspberry pi and create the project folder:

mkdir discord_bot && cd discord_bot
pip install discord.py groq psutil requests

### 2. setup secret keys

the bot reads credentials from separate text files so you don't leak them in your code. create these three files in your folder:

    Discord.txt: paste your discord bot token here.

    AI.txt: paste your groq api key here.

    webhook.txt: paste your discord channel webhook url here.

### 3. the main script (Main.py)

create the file with nano Main.py and paste the code in this repository.

### 4. make it run in the background

create a service file so the bot runs 24/7 without needing an open terminal:

sudo nano /etc/systemd/system/discordbot.service

paste this in:

[Unit]
Description=Discord AI Chatbot
After=network-online.target

[Service]
User=zallkyre
WorkingDirectory=/home/zallkyre/discord_bot
ExecStart=/usr/bin/python3 /home/zallkyre/discord_bot/Main.py
Restart=always

[Install]
WantedBy=multi-user.target

### 5. start & enable

sudo systemctl daemon-reload

sudo systemctl enable discordbot.service

sudo systemctl start discordbot.service

###Congrats! it should work now.
