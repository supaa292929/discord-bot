import discord
from discord.ext import commands
import asyncio

import os
TOKEN = os.getenv("DISCORD_TOKEN")
NOTIFICATION_CHANNEL_ID = 1464767441178726639

# ============== CUSTOMIZE YOUR EMBED HERE ==============
SUPPORTER_ROLE_NAME = 'Supporter'
SUPPORTER_EMBED_TITLE = "claimed the Supporter role ✅"
SUPPORTER_EMBED_THANKS = "Thanks for supporting us!"
SUPPORTER_EMBED_MESSAGE = "You received {role} role!"
SUPPORTER_EMBED_PERKS = ["Exclusive role", "2x Level XP"]
SUPPORTER_EMBED_COLOR = 0x9B59B6
SUPPORTER_EMBED_IMAGE = "https://i.ytimg.com/vi/PCyQPRZqXgE/maxresdefault.jpg"
# =======================================================

# ============== WELCOME MESSAGE ==============
WELCOME_CHANNEL_ID = 1455918158719221994
WELCOME_COLOR = 0xD85FEE
WELCOME_GIF = "https://cdn.discordapp.com/attachments/1062077673569726564/1169025501000536104/welcome.gif"
DIVIDER_URL = "https://cdn.discordapp.com/attachments/1469626641205694593/1473012403485671485/imageedit_1_7691336082.gif?ex=6994a934&is=699357b4&hm=0ed473eb495af3d61e5ce671c1d4a5fc3c096de95b441aa3c46c7a2ae3d04736"
# =============================================

# ============== BOOSTER MESSAGE ==============
BOOSTER_CHANNEL_ID = 1464767441178726639  # Replace with your booster channel ID
BOOSTER_TITLE = "New Server Boost! 🚀"
BOOSTER_MESSAGE = "{member} just boosted the server! Thank you! 💜"  # {member} = mention
BOOSTER_COLOR = 0xF47FFF  # Pink/boost color
BOOSTER_IMAGE = None  # Set to a URL or None
# =============================================

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True

bot = commands.Bot(command_prefix='^', intents=intents)
bot.remove_command('help')


# ================== WELCOME BUTTON ==================

class WelcomeView(discord.ui.View):
    def __init__(self, new_member_id):
        super().__init__(timeout=None)
        self.new_member_id = new_member_id
        self.welcomed_users = set()

    @discord.ui.button(label='Welcome!', style=discord.ButtonStyle.secondary, emoji='\U0001F44B')
    async def welcome_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.new_member_id:
            await interaction.response.send_message("You can't welcome yourself silly \U0001F60A", ephemeral=True)
            return

        if interaction.user.id in self.welcomed_users:
            await interaction.response.send_message("You already welcomed them! \U0001F49C", ephemeral=True)
            return

        self.welcomed_users.add(interaction.user.id)
        new_member = interaction.guild.get_member(self.new_member_id)
        member_mention = new_member.mention if new_member else "the new member"
        await interaction.response.send_message(
            f"**{interaction.user.display_name}** welcomed {member_mention} to the server! \U0001F44B",
        )


# ================== OTAKU STATUS TRACKING ==================

def has_otaku_status(member: discord.Member) -> bool:
    """Check if member has /otaku in their custom status."""
    if not member.activities:
        return False

    for activity in member.activities:
        if isinstance(activity, discord.CustomActivity):
            if activity.name and '/otaku' in activity.name.lower():
                return True
        if hasattr(activity, 'name') and activity.name:
            if '/otaku' in activity.name.lower():
                return True
        if hasattr(activity, 'state') and activity.state:
            if '/otaku' in activity.state.lower():
                return True

    return False


def get_supporter_role(guild: discord.Guild) -> discord.Role:
    """Get the Supporter role. Returns None if it doesn't exist."""
    return discord.utils.get(guild.roles, name=SUPPORTER_ROLE_NAME)


async def send_supporter_notification(member: discord.Member, role: discord.Role):
    """Send an embed notification when a member receives the Supporter role."""
    try:
        channel = member.guild.get_channel(NOTIFICATION_CHANNEL_ID)
        if not channel:
            return

        perks_str = "\n".join([f"`{perk}`" for perk in SUPPORTER_EMBED_PERKS])

        description = f"{member.mention} **{SUPPORTER_EMBED_TITLE}**\n\n"
        description += f"✨ {SUPPORTER_EMBED_THANKS}\n\n"
        description += f"{SUPPORTER_EMBED_MESSAGE.format(role=role.mention)}\n\n"
        description += f"**Perks:**\n{perks_str}"

        embed = discord.Embed(
            description=description,
            color=role.color if role.color != discord.Color.default() else SUPPORTER_EMBED_COLOR
        )

        if SUPPORTER_EMBED_IMAGE:
            embed.set_image(url=SUPPORTER_EMBED_IMAGE)

        await channel.send(embed=embed)
    except Exception as e:
        print(f'Error sending supporter notification: {e}')


async def update_member_role(member: discord.Member, allow_remove: bool = False):
    """Update a member's Supporter role based on their /otaku status.
    Only adds roles by default. Set allow_remove=True to also remove roles."""
    if member.bot:
        return

    try:
        role = get_supporter_role(member.guild)
        if not role:
            return

        has_status = has_otaku_status(member)
        has_role = role in member.roles

        if has_status and not has_role:
            await member.add_roles(role, reason='Has /otaku in status')
            await send_supporter_notification(member, role)
            print(f'Added {SUPPORTER_ROLE_NAME} to {member.name} in {member.guild.name}')
        elif not has_status and has_role and allow_remove:
            await member.remove_roles(role, reason='No longer has /otaku in status')
            print(f'Removed {SUPPORTER_ROLE_NAME} from {member.name} in {member.guild.name}')
    except discord.Forbidden:
        print(f'Missing permissions to manage roles for {member.name} in {member.guild.name}')
    except Exception as e:
        print(f'Error updating role for {member.name}: {e}')


# ================== EVENTS ==================

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print(f'Monitoring for "/otaku" in member statuses')
    print(f'Role name: {SUPPORTER_ROLE_NAME}')
    print('-' * 50)

    for guild in bot.guilds:
        print(f'Scanning members in {guild.name}...')
        for member in guild.members:
            await update_member_role(member)
        print(f'Finished scanning {guild.name}')


@bot.event
async def on_presence_update(before: discord.Member, after: discord.Member):
    is_online = after.status in (discord.Status.online, discord.Status.idle, discord.Status.dnd)
    await update_member_role(after, allow_remove=is_online)


@bot.event
async def on_member_join(member: discord.Member):
    await update_member_role(member)

    # Send welcome message
    try:
        channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                description=(
                    f"# Welcome to {member.guild.name}!\n"
                    f"\u200B\n"
                    f"We're so happy you're here\n"
                    f"\u200B\n"
                    f"\U0001F4CC **Get started:**\n"
                    f"> <#{1464671783889141872}> \u2014 Read the rules\n"
                    f"> <#{1457842618116473146}> \u2014 Make an intro\n"
                    f"> <#{1457842396636123197}> \u2014 Start chatting!"
                ),
                color=WELCOME_COLOR
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_image(url=DIVIDER_URL)

            view = WelcomeView(member.id)
            await channel.send(content=f"{member.mention}", embed=embed, view=view)
    except Exception as e:
        print(f'Error sending welcome message: {e}')


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if before.premium_since is None and after.premium_since is not None:
        try:
            channel = after.guild.get_channel(BOOSTER_CHANNEL_ID)
            if channel:
                embed = discord.Embed(
                    title=BOOSTER_TITLE,
                    description=BOOSTER_MESSAGE.format(member=after.mention),
                    color=BOOSTER_COLOR
                )
                embed.set_thumbnail(url=after.display_avatar.url)
                embed.set_footer(text=f'Server now has {after.guild.premium_subscription_count} boosts!')
                if BOOSTER_IMAGE:
                    embed.set_image(url=BOOSTER_IMAGE)
                await channel.send(embed=embed)
        except Exception as e:
            print(f'Error sending booster message: {e}')


@bot.event
async def on_command_error(ctx, error):
    pass


if __name__ == '__main__':
    bot.run(TOKEN)
