import discord
from discord.ext import commands
import asyncio

import os
TOKEN = os.getenv("DISCORD_TOKEN")

NOTIFICATION_CHANNEL_ID = 1464767441178726639  # Replace with your channel ID

# ============== CUSTOMIZE YOUR EMBED HERE ==============
ROLE_NAME = 'Elite Supporter'
SUPPORTER_ROLE_NAME = 'Supporter'
SUPPORTER_EMBED_TITLE = "claimed the Supporter role ✅"
SUPPORTER_EMBED_THANKS = "Thanks for supporting us!"
SUPPORTER_EMBED_MESSAGE = "You received {role}!"
SUPPORTER_EMBED_PERKS = ["Exclusive role"]
SUPPORTER_EMBED_COLOR = 0x9B59B6
SUPPORTER_EMBED_IMAGE = "https://i.ytimg.com/vi/PCyQPRZqXgE/maxresdefault.jpg"
EMBED_TITLE = "put /otaku in their status ✅"
EMBED_THANKS = "Thanks for being an elite supporter!"
EMBED_MESSAGE = "You received {role}!"  # {role} will be replaced with role mention
EMBED_PERKS = ["2x Level XP", "Exclusive role"]  # List of perks
EMBED_COLOR = 0xFFD700  # Gold embed color
EMBED_THUMBNAIL = None  # Small image on the right (set to None to disable)
EMBED_IMAGE = "https://i.ytimg.com/vi/PCyQPRZqXgE/maxresdefault.jpg"  # Large image at the bottom
# =======================================================

# ============== WELCOME MESSAGE ==============
WELCOME_CHANNEL_ID = 1457842396636123197  # Replace with your welcome channel ID
WELCOME_TITLE = "Welcome to Otaku Paradise!"
WELCOME_MESSAGE = "{member}"  # {member} = mention
WELCOME_COLOR = 0xd85fee  # Purple-pink
WELCOME_IMAGE = "https://a.storyblok.com/f/178900/2880x1620/6f3b396854/bb03d5efdaccdd35e7781ac76bd3651d1681914997_main.jpg/m/filters:quality(95)format(webp)"
# =============================================

# ============== BOOSTER MESSAGE ==============
BOOSTER_CHANNEL_ID = 123456789012345678  # Replace with your booster channel ID
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


# ================== EMBED CREATOR ==================

class EmbedCreatorView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.embed_data = {
            'title': None,
            'description': None,
            'color': 0x9B59B6,
            'footer': None,
            'thumbnail': None,
            'image': None,
            'author_name': None,
            'author_icon': None,
            'fields': [],
        }
        self.target_channel = None

    def build_preview_embed(self):
        embed = discord.Embed(
            title=self.embed_data['title'] or 'No title set',
            description=self.embed_data['description'] or '*No description set*',
            color=self.embed_data['color']
        )
        if self.embed_data['footer']:
            embed.set_footer(text=self.embed_data['footer'])
        if self.embed_data['thumbnail']:
            embed.set_thumbnail(url=self.embed_data['thumbnail'])
        if self.embed_data['image']:
            embed.set_image(url=self.embed_data['image'])
        if self.embed_data['author_name']:
            embed.set_author(name=self.embed_data['author_name'], icon_url=self.embed_data['author_icon'])
        for field in self.embed_data['fields']:
            embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])
        return embed

    async def wait_for_response(self, prompt):
        await self.ctx.send(prompt)
        try:
            msg = await bot.wait_for(
                'message',
                check=lambda m: m.author == self.ctx.author and m.channel == self.ctx.channel,
                timeout=120
            )
            return msg.content
        except asyncio.TimeoutError:
            await self.ctx.send('⏰ Timed out. Use the buttons to continue.')
            return None

    @discord.ui.button(label='Title', style=discord.ButtonStyle.primary, emoji='📝', row=0)
    async def set_title(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        response = await self.wait_for_response('**📝 Enter the embed title** (or `none` to clear):')
        if response:
            self.embed_data['title'] = None if response.lower() == 'none' else response
            await self.ctx.send(f'✅ Title {"cleared" if response.lower() == "none" else "set"}!')

    @discord.ui.button(label='Description', style=discord.ButtonStyle.primary, emoji='📄', row=0)
    async def set_description(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        response = await self.wait_for_response('**📄 Enter the embed description** (supports Discord markdown, or `none` to clear):')
        if response:
            self.embed_data['description'] = None if response.lower() == 'none' else response
            await self.ctx.send(f'✅ Description {"cleared" if response.lower() == "none" else "set"}!')

    @discord.ui.button(label='Color', style=discord.ButtonStyle.primary, emoji='🎨', row=0)
    async def set_color(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        response = await self.wait_for_response('**🎨 Enter a hex color** (e.g. `#ff5733`, `ff5733`, or a name like `red`, `blue`, `green`):')
        if response:
            color_map = {
                'red': 0xFF0000, 'green': 0x00FF00, 'blue': 0x0000FF,
                'purple': 0x9B59B6, 'orange': 0xFF8C00, 'yellow': 0xFFD700,
                'pink': 0xFF69B4, 'cyan': 0x00FFFF, 'white': 0xFFFFFF,
                'black': 0x000001, 'gold': 0xFFD700, 'teal': 0x008080,
            }
            try:
                if response.lower() in color_map:
                    self.embed_data['color'] = color_map[response.lower()]
                else:
                    hex_str = response.strip('#').strip()
                    self.embed_data['color'] = int(hex_str, 16)
                await self.ctx.send(f'✅ Color set!')
            except ValueError:
                await self.ctx.send('❌ Invalid color. Use hex like `#ff5733` or a color name.')

    @discord.ui.button(label='Footer', style=discord.ButtonStyle.secondary, emoji='🔻', row=1)
    async def set_footer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        response = await self.wait_for_response('**🔻 Enter the footer text** (or `none` to clear):')
        if response:
            self.embed_data['footer'] = None if response.lower() == 'none' else response
            await self.ctx.send(f'✅ Footer {"cleared" if response.lower() == "none" else "set"}!')

    @discord.ui.button(label='Thumbnail', style=discord.ButtonStyle.secondary, emoji='🖼️', row=1)
    async def set_thumbnail(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        response = await self.wait_for_response('**🖼️ Enter the thumbnail URL** (small image on the right, or `none` to clear):')
        if response:
            self.embed_data['thumbnail'] = None if response.lower() == 'none' else response
            await self.ctx.send(f'✅ Thumbnail {"cleared" if response.lower() == "none" else "set"}!')

    @discord.ui.button(label='Image', style=discord.ButtonStyle.secondary, emoji='🏞️', row=1)
    async def set_image(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        response = await self.wait_for_response('**🏞️ Enter the image URL** (large image at bottom, or `none` to clear):')
        if response:
            self.embed_data['image'] = None if response.lower() == 'none' else response
            await self.ctx.send(f'✅ Image {"cleared" if response.lower() == "none" else "set"}!')

    @discord.ui.button(label='Author', style=discord.ButtonStyle.secondary, emoji='👤', row=1)
    async def set_author(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        response = await self.wait_for_response('**👤 Enter the author name** (or `none` to clear):')
        if response:
            if response.lower() == 'none':
                self.embed_data['author_name'] = None
                self.embed_data['author_icon'] = None
                await self.ctx.send('✅ Author cleared!')
            else:
                self.embed_data['author_name'] = response
                icon = await self.wait_for_response('**👤 Enter author icon URL** (or `none` to skip):')
                self.embed_data['author_icon'] = None if not icon or icon.lower() == 'none' else icon
                await self.ctx.send('✅ Author set!')

    @discord.ui.button(label='Add Field', style=discord.ButtonStyle.success, emoji='➕', row=2)
    async def add_field(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if len(self.embed_data['fields']) >= 25:
            await self.ctx.send('❌ Maximum 25 fields reached.')
            return
        name = await self.wait_for_response('**➕ Enter the field name:**')
        if not name:
            return
        value = await self.wait_for_response('**➕ Enter the field value:**')
        if not value:
            return
        inline_resp = await self.wait_for_response('**➕ Inline?** (`yes` or `no`):')
        inline = inline_resp and inline_resp.lower() in ('yes', 'y', 'true')
        self.embed_data['fields'].append({'name': name, 'value': value, 'inline': inline})
        await self.ctx.send(f'✅ Field added! ({len(self.embed_data["fields"])} total)')

    @discord.ui.button(label='Clear Fields', style=discord.ButtonStyle.danger, emoji='🗑️', row=2)
    async def clear_fields(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed_data['fields'] = []
        await interaction.response.send_message('✅ All fields cleared!', ephemeral=False)

    @discord.ui.button(label='Preview', style=discord.ButtonStyle.primary, emoji='👁️', row=3)
    async def preview(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.build_preview_embed()
        await interaction.response.send_message('**👁️ Embed Preview:**', embed=embed)

    @discord.ui.button(label='Send', style=discord.ButtonStyle.success, emoji='🚀', row=3)
    async def send_embed(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        response = await self.wait_for_response(
            '**🚀 Mention or enter the ID of the channel to send to** (e.g. #general or `123456789`):'
        )
        if not response:
            return

        channel = None
        if response.startswith('<#') and response.endswith('>'):
            try:
                channel_id = int(response[2:-1])
                channel = self.ctx.guild.get_channel(channel_id)
            except ValueError:
                pass
        if not channel:
            try:
                channel_id = int(response.strip())
                channel = self.ctx.guild.get_channel(channel_id)
            except ValueError:
                pass
        if not channel:
            channel = discord.utils.get(self.ctx.guild.text_channels, name=response.strip('#').strip())

        if not channel:
            await self.ctx.send('❌ Channel not found. Make sure the channel exists in this server.')
            return

        try:
            embed = self.build_preview_embed()
            if embed.title == 'No title set':
                embed.title = None
            if embed.description == '*No description set*':
                embed.description = None
            await channel.send(embed=embed)
            await self.ctx.send(f'✅ Embed sent to {channel.mention}!')
        except discord.Forbidden:
            await self.ctx.send(f'❌ I don\'t have permission to send messages in {channel.mention}.')
        except Exception as e:
            await self.ctx.send(f'❌ Error: {e}')

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.danger, emoji='✖️', row=3)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('❌ Embed creator cancelled.')
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message('❌ Only the command author can use these buttons.', ephemeral=True)
            return False
        return True

    async def on_timeout(self):
        await self.ctx.send('⏰ Embed creator timed out (5 minutes). Use `^embed` to start again.')


@bot.command(name='embed')
@commands.has_permissions(administrator=True)
async def embed_creator(ctx):
    """Interactive embed creator - build and send custom embeds to any channel."""
    view = EmbedCreatorView(ctx)

    instructions = discord.Embed(
        title='🔨 Embed Creator',
        description=(
            'Use the buttons below to build your custom embed.\n\n'
            '**Row 1** — Title, Description, Color\n'
            '**Row 2** — Footer, Thumbnail, Image, Author\n'
            '**Row 3** — Add/Clear Fields\n'
            '**Row 4** — Preview, Send, or Cancel\n\n'
            'Click a button, then type your response in chat.'
        ),
        color=0x9B59B6
    )

    await ctx.send(embed=instructions, view=view)


@bot.command(name='quickembed')
@commands.has_permissions(administrator=True)
async def quick_embed(ctx, channel: discord.TextChannel, title: str, *, description: str):
    """Quick embed send: ^quickembed #channel "Title" Description text here"""
    embed = discord.Embed(title=title, description=description, color=0x9B59B6)
    try:
        await channel.send(embed=embed)
        await ctx.send(f'✅ Embed sent to {channel.mention}!')
    except discord.Forbidden:
        await ctx.send(f'❌ Missing permissions for {channel.mention}.')


# ================== OTAKU STATUS TRACKING ==================

def has_otaku_status(member: discord.Member) -> bool:
    """Check if member has /otaku in any of their activities/status."""
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


async def get_or_create_role(guild: discord.Guild) -> discord.Role:
    """Get the role, or create it if it doesn't exist."""
    role = discord.utils.get(guild.roles, name=ROLE_NAME)

    if not role:
        role = await guild.create_role(
            name=ROLE_NAME,
            color=discord.Color.gold(),
            reason='Auto-created for /otaku status tracking'
        )
        print(f'Created role "{ROLE_NAME}" in {guild.name}')

    return role


async def send_role_notification(member: discord.Member, role: discord.Role):
    """Send an embed notification when a member receives the role."""
    try:
        channel = member.guild.get_channel(NOTIFICATION_CHANNEL_ID)
        if not channel:
            print(f'Notification channel not found: {NOTIFICATION_CHANNEL_ID}')
            return

        perks_str = "\n".join([f"`{perk}`" for perk in EMBED_PERKS])

        description = f"{member.mention} **{EMBED_TITLE}**\n\n"
        description += f"✨ {EMBED_THANKS}\n\n"
        description += f"{EMBED_MESSAGE.format(role=role.mention)}\n\n"
        description += f"**Perks:**\n{perks_str}"

        embed = discord.Embed(
            description=description,
            color=role.color if role.color != discord.Color.default() else EMBED_COLOR
        )

        if EMBED_THUMBNAIL:
            embed.set_thumbnail(url=EMBED_THUMBNAIL)
        if EMBED_IMAGE:
            embed.set_image(url=EMBED_IMAGE)

        await channel.send(embed=embed)
    except Exception as e:
        print(f'Error sending notification: {e}')


async def update_member_role(member: discord.Member):
    """Update a member's role based on their status."""
    if member.bot:
        return

    try:
        role = await get_or_create_role(member.guild)
        has_status = has_otaku_status(member)
        has_role = role in member.roles
        is_offline = member.status == discord.Status.offline

        if has_status and not has_role:
            await member.add_roles(role, reason='Has /otaku in status')
            await send_role_notification(member, role)
            print(f'Added {ROLE_NAME} to {member.name} in {member.guild.name}')
        elif not has_status and has_role and not is_offline:
            await member.remove_roles(role, reason='No longer has /otaku in status')
            print(f'Removed {ROLE_NAME} from {member.name} in {member.guild.name}')
    except discord.Forbidden:
        print(f'Missing permissions to manage roles for {member.name} in {member.guild.name}')
    except Exception as e:
        print(f'Error updating role for {member.name}: {e}')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print(f'Monitoring for "/otaku" in member statuses')
    print(f'Role name: {ROLE_NAME}')
    print('-' * 50)

    for guild in bot.guilds:
        print(f'Scanning members in {guild.name}...')
        for member in guild.members:
            await update_member_role(member)
        print(f'Finished scanning {guild.name}')


@bot.event
async def on_presence_update(before: discord.Member, after: discord.Member):
    await update_member_role(after)


@bot.event
async def on_member_join(member: discord.Member):
    await update_member_role(member)

    # Send welcome message
    try:
        channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title=WELCOME_TITLE,
                description=WELCOME_MESSAGE.format(member=member.mention),
                color=WELCOME_COLOR
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f'Member #{member.guild.member_count}')
            if WELCOME_IMAGE:
                embed.set_image(url=WELCOME_IMAGE)
            await channel.send(embed=embed)
    except Exception as e:
        print(f'Error sending welcome message: {e}')


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    # Detect new server boost
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


# ================== HELP COMMAND ==================

bot.remove_command('help')  # Remove default help command


@bot.command(name='help')
async def help_command(ctx):
    """Show all available commands."""
    embed = discord.Embed(
        title='📖 Commands',
        color=0x9B59B6
    )

    embed.add_field(
        name='🎭 Roles',
        value=(
            '`^tag` — Claim the Supporter role\n'
            '`^untag` — Remove the Supporter role'
        ),
        inline=False
    )

    embed.add_field(
        name='📨 Embeds (Admin)',
        value=(
            '`^embed` — Interactive embed creator\n'
            '`^quickembed #channel "Title" Description` — Quick embed send'
        ),
        inline=False
    )

    await ctx.send(embed=embed)


# ================== TAG COMMAND ==================

async def get_or_create_supporter_role(guild: discord.Guild) -> discord.Role:
    """Get the Supporter role, or create it if it doesn't exist."""
    role = discord.utils.get(guild.roles, name=SUPPORTER_ROLE_NAME)
    if not role:
        role = await guild.create_role(
            name=SUPPORTER_ROLE_NAME,
            color=discord.Color.from_rgb(255, 105, 180),
            reason='Auto-created for !tag command'
        )
        print(f'Created role "{SUPPORTER_ROLE_NAME}" in {guild.name}')
    return role


async def send_supporter_notification(member: discord.Member, role: discord.Role):
    """Send an embed notification when a member claims the Supporter role."""
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


@bot.command(name='tag')
async def tag_prefix(ctx):
    """Claim the Supporter role."""
    try:
        role = await get_or_create_supporter_role(ctx.guild)
        if role in ctx.author.roles:
            await ctx.send(f'{ctx.author.mention} You already have the **{role.name}** role! Use `^untag` to remove it.')
            return
        await ctx.author.add_roles(role, reason='User used !tag to claim role')
        await send_supporter_notification(ctx.author, role)
        await ctx.send(f'✅ {ctx.author.mention} You now have the **{role.name}** role!')
    except discord.Forbidden:
        await ctx.send('❌ I don\'t have permission to manage roles.')


@bot.command(name='untag')
async def untag_prefix(ctx):
    """Remove the Supporter role."""
    try:
        role = await get_or_create_supporter_role(ctx.guild)
        if role not in ctx.author.roles:
            await ctx.send(f'{ctx.author.mention} You don\'t have the **{role.name}** role.')
            return
        await ctx.author.remove_roles(role, reason='User used !untag to remove role')
        await ctx.send(f'❌ {ctx.author.mention} The **{role.name}** role has been removed.')
    except discord.Forbidden:
        await ctx.send('❌ I don\'t have permission to manage roles.')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('❌ You are not an Administrator.')
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        await ctx.send('❌ Command failed.')
        print(f'Command error: {error}')


if __name__ == '__main__':
    bot.run(TOKEN)
