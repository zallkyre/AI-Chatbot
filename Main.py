import discord
from discord.ext import commands
from discord import app_commands
import groq
import psutil
import time
import random
import json

# --- config ---
with open("Discord.txt", "r") as f:
    TOKEN = f.read().strip()
with open("AI.txt", "r") as f:
    GROQ_KEY = f.read().strip()

# --- setup ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
client = groq.Groq(api_key=GROQ_KEY)
START_TIME = time.time()

SYSTEM_PROMPT = "you are a discord bot running on a raspberry pi 3. you know you are a bot in discord. answer in 1 sentence only. no caps. no emojis. no comfort. be direct. don't be submissive: you have your own opinions and can push back. don't agree with everything or grovel."

# --- memory (small, per user) ---
MEMORY_FILE = "memory.json"
MAX_HISTORY = 20  # 10 exchanges per user
MAX_USERS = 100   # keep the file tiny


def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_memory(mem):
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(mem, f)
    except Exception:
        pass


def remember(user_id, user_msg, bot_msg):
    mem = load_memory()
    history = mem.get(str(user_id), [])
    history.append({"role": "user", "content": user_msg})
    history.append({"role": "assistant", "content": bot_msg})
    mem[str(user_id)] = history[-MAX_HISTORY:]
    if len(mem) > MAX_USERS:
        mem = dict(list(mem.items())[-MAX_USERS:])
    save_memory(mem)


def forget(user_id):
    mem = load_memory()
    mem.pop(str(user_id), None)
    save_memory(mem)


def uptime_str():
    secs = int(time.time() - START_TIME)
    h, m, s = secs // 3600, (secs % 3600) // 60, secs % 60
    return f"{h}h {m}m {s}s"


# --- commands ---
@bot.tree.command(name="ai", description="ask gpt-oss-20b")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def ai(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    try:
        history = load_memory().get(str(interaction.user.id), [])
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(history)
        messages.append({"role": "user", "content": prompt})
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="openai/gpt-oss-20b",
        )
        reply = chat_completion.choices[0].message.content
        remember(interaction.user.id, prompt, reply)
        await interaction.followup.send(reply)
    except Exception as e:
        await interaction.followup.send(f"error: {e}")


@bot.tree.command(name="forget", description="wipe your memory")
async def forget_cmd(interaction: discord.Interaction):
    forget(interaction.user.id)
    await interaction.response.send_message("memory wiped. i remember nothing.")


@bot.tree.command(name="ping", description="bot latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"pong! {round(bot.latency * 1000)}ms")


@bot.tree.command(name="stats", description="pi stats")
async def stats(interaction: discord.Interaction):
    ram = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)
    temp = None
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            temp = round(int(f.read().strip()) / 1000, 1)
    except Exception:
        pass
    msg = f"**pi stats**\nram: {ram.used // 1048576}mb / {ram.total // 1048576}mb\ncpu: {cpu}%\nuptime: {uptime_str()}"
    if temp:
        msg += f"\ntemp: {temp}c"
    await interaction.response.send_message(msg)


@bot.tree.command(name="roll", description="roll dice, e.g. /roll 2d6")
async def roll(interaction: discord.Interaction, dice: str = "1d6"):
    try:
        count, sides = dice.lower().split("d")
        count, sides = int(count), int(sides)
        if count < 1 or count > 100 or sides < 2 or sides > 1000:
            raise ValueError
        results = [random.randint(1, sides) for _ in range(count)]
        total = sum(results)
        await interaction.response.send_message(f"{dice} -> {results} = **{total}**")
    except Exception:
        await interaction.response.send_message("use format like 2d6")


@bot.tree.command(name="coin", description="flip a coin")
async def coin(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(["heads", "tails"]))


@bot.tree.command(name="8ball", description="ask the magic 8 ball")
async def eightball(interaction: discord.Interaction, question: str):
    answers = ["yes", "no", "maybe", "definitely", "absolutely not", "ask again later", "signs point to yes", "don't count on it"]
    await interaction.response.send_message(f"🎱 {random.choice(answers)}")


@bot.tree.command(name="joke", description="tell a joke")
async def joke(interaction: discord.Interaction):
    jokes = [
        "why did the programmer quit his job? because he didn't get arrays.",
        "there are 10 types of people: those who understand binary and those who don't.",
        "why do programmers prefer dark mode? because light attracts bugs.",
        "i told my pi a joke about udp... i'm not sure it got it.",
        "why did the raspberry pi go to therapy? it had too many unresolved issues.",
        "why do java developers wear glasses? because they can't see sharp.",
    ]
    await interaction.response.send_message(random.choice(jokes))


@bot.tree.command(name="uptime", description="how long the bot has been alive")
async def uptime(interaction: discord.Interaction):
    await interaction.response.send_message(f"alive for {uptime_str()}")


@bot.tree.command(name="avatar", description="get someone's avatar")
async def avatar(interaction: discord.Interaction, user: discord.User = None):
    user = user or interaction.user
    await interaction.response.send_message(user.display_avatar.url)


@bot.tree.command(name="serverinfo", description="server info")
async def serverinfo(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message("this is a dm, no server here")
        return
    g = interaction.guild
    await interaction.response.send_message(f"**{g.name}**\nmembers: {g.member_count}\ncreated: {g.created_at.date()}")


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"logged in as {bot.user}")


bot.run(TOKEN)