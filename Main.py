import discord
from discord.ext import tasks, commands
from discord import app_commands
import groq
import psutil
import requests

# --- config ---
with open("Discord.txt", "r") as f:
    TOKEN = f.read().strip()
with open("AI.txt", "r") as f:
    GROQ_KEY = f.read().strip()
with open("webhook.txt", "r") as f:
    WEBHOOK_URL = f.read().strip()

# --- setup ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
client = groq.Groq(api_key=GROQ_KEY)

@tasks.loop(minutes=15)
async def status_report():
    ram = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)
    msg = f"**bot status**\nram: {ram.used // 1048576}mb / {ram.total // 1048576}mb\ncpu: {cpu}%\nnet: online ✅"
    requests.post(WEBHOOK_URL, json={"content": msg})

@bot.tree.command(name="ai", description="ask gpt-oss-20b")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def ai(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "answer in 1 sentence only. no caps. no emojis. no comfort. be direct."},
                {"role": "user", "content": prompt}
            ],
            model="openai/gpt-oss-20b",
        )
        await interaction.followup.send(chat_completion.choices[0].message.content)
    except Exception as e:
        await interaction.followup.send(f"⚠️ error: {e}")

@bot.event
async def on_ready():
    await bot.tree.sync()
    if not status_report.is_running():
        status_report.start()
    requests.post(WEBHOOK_URL, json={"content": "⚡ bot online (192.168.1.14)"})

bot.run(TOKEN)