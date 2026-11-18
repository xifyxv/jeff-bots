import discord
from discord.ext import commands
import os

# ==================== CONFIG ====================
TOKEN = os.getenv("TOKEN")
GUILD_ID = 1464708562046419172
WELCOME_CHANNEL_ID = 1566176136151441499

PREFIX = "!"

# ==================== BOT SETUP ====================
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# ==================== EVENTS ====================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Welcome Bot is online!")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="for new members"),
        status=discord.Status.online
    )

@bot.event
async def on_member_join(member):
    if member.guild.id != GUILD_ID:
        return

    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        print("ERROR: Welcome channel not found!")
        return

    member_count = member.guild.member_count
    ordinal = get_ordinal(member_count)

    embed = discord.Embed(
        title="Welcome to Jeff Tweaks!",
        description=f"Welcome {member.mention} to **Jeff Tweaks**!\nYou are the **{ordinal}** member!",
        color=0xFFD700
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text="Jeff Tweaks", icon_url=member.guild.icon.url if member.guild.icon else None)
    embed.timestamp = discord.utils.utcnow()

    try:
        await channel.send(embed=embed)
        print(f"Welcomed {member} (#{member_count})")
    except Exception as e:
        print(f"Failed to send welcome: {e}")

def get_ordinal(n):
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

# ==================== COMMANDS ====================
@bot.command(name="testwelcome")
@commands.has_permissions(administrator=True)
async def test_welcome(ctx):
    await on_member_join(ctx.author)
    await ctx.send("Test welcome sent!", delete_after=5)

# ==================== RUN ====================
if __name__ == "__main__":
    if not TOKEN:
        print("ERROR: TOKEN environment variable not set!")
    else:
        bot.run(TOKEN)
