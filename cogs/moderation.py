import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Check if user has moderation permissions
    async def check_mod_permissions(self, ctx):
        if not ctx.author.guild_permissions.administrator and not any(role.name.lower() in ['mod', 'moderator', 'admin'] for role in ctx.author.roles):
            await ctx.send(f'{ctx.author.mention} You do not have permission to use this command.')
            return False
        return True

    @commands.command(name='kick', help='Kick a member from the server')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason='No reason provided'):
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.send(f'{ctx.author.mention} You cannot kick this member.')
            return
        
        await member.kick(reason=reason)
        embed = discord.Embed(title='Member Kicked', color=discord.Color.red())
        embed.add_field(name='Member', value=member.mention)
        embed.add_field(name='Reason', value=reason)
        embed.add_field(name='Moderator', value=ctx.author.mention)
        embed.set_thumbnail(url=member.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name='ban', help='Ban a member from the server')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason='No reason provided'):
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.send(f'{ctx.author.mention} You cannot ban this member.')
            return
        
        await member.ban(reason=reason)
        embed = discord.Embed(title='Member Banned', color=discord.Color.red())
        embed.add_field(name='Member', value=member.mention)
        embed.add_field(name='Reason', value=reason)
        embed.add_field(name='Moderator', value=ctx.author.mention)
        embed.set_thumbnail(url=member.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name='unban', help='Unban a member from the server')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: str, *, reason='No reason provided'):
        banned_users = [ban_entry async for ban_entry in ctx.guild.bans()]
        member_name, member_discriminator = user.split('#')
        
        for ban_entry in banned_users:
            user_obj = ban_entry.user
            if (user_obj.name, user_obj.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user_obj, reason=reason)
                embed = discord.Embed(title='Member Unbanned', color=discord.Color.green())
                embed.add_field(name='Member', value=user_obj.mention)
                embed.add_field(name='Reason', value=reason)
                embed.add_field(name='Moderator', value=ctx.author.mention)
                await ctx.send(embed=embed)
                return
        
        await ctx.send(f'{ctx.author.mention} Could not find that user in the ban list.')

    @commands.command(name='mute', help='Mute a member')
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, duration: int = None, *, reason='No reason provided'):
        muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
        
        if not muted_role:
            muted_role = await ctx.guild.create_role(name='Muted')
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False)
        
        await member.add_roles(muted_role, reason=reason)
        embed = discord.Embed(title='Member Muted', color=discord.Color.orange())
        embed.add_field(name='Member', value=member.mention)
        embed.add_field(name='Reason', value=reason)
        embed.add_field(name='Moderator', value=ctx.author.mention)
        if duration:
            embed.add_field(name='Duration', value=f'{duration} seconds')
        await ctx.send(embed=embed)
        
        if duration:
            await asyncio.sleep(duration)
            await member.remove_roles(muted_role)
            await ctx.send(f'{member.mention} has been unmuted.')

    @commands.command(name='unmute', help='Unmute a member')
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason='No reason provided'):
        muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
        
        if not muted_role:
            await ctx.send(f'{ctx.author.mention} Muted role does not exist.')
            return
        
        await member.remove_roles(muted_role, reason=reason)
        embed = discord.Embed(title='Member Unmuted', color=discord.Color.green())
        embed.add_field(name='Member', value=member.mention)
        embed.add_field(name='Reason', value=reason)
        embed.add_field(name='Moderator', value=ctx.author.mention)
        await ctx.send(embed=embed)

    @commands.command(name='warn', help='Warn a member')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason='No reason provided'):
        embed = discord.Embed(title='Member Warned', color=discord.Color.yellow())
        embed.add_field(name='Member', value=member.mention)
        embed.add_field(name='Reason', value=reason)
        embed.add_field(name='Moderator', value=ctx.author.mention)
        embed.set_thumbnail(url=member.avatar.url)
        await ctx.send(embed=embed)
        
        try:
            await member.send(f'You have been warned in {ctx.guild.name} for: {reason}')
        except discord.Forbidden:
            pass

    @commands.command(name='purge', help='Delete messages from a channel')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = 10):
        if amount > 100:
            await ctx.send(f'{ctx.author.mention} Cannot delete more than 100 messages at a time.')
            return
        
        deleted = await ctx.channel.purge(limit=amount)
        embed = discord.Embed(title='Messages Purged', color=discord.Color.blurple())
        embed.add_field(name='Amount', value=len(deleted))
        embed.add_field(name='Channel', value=ctx.channel.mention)
        embed.add_field(name='Moderator', value=ctx.author.mention)
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(name='clear', help='Clear messages (alias for purge)')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):
        await self.purge(ctx, amount)

    @commands.command(name='slowmode', help='Set slowmode for a channel')
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int = 0):
        await ctx.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await ctx.send(f'{ctx.author.mention} Slowmode disabled.')
        else:
            await ctx.send(f'{ctx.author.mention} Slowmode set to {seconds} seconds.')

    @commands.command(name='lock', help='Lock a channel')
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed = discord.Embed(title='Channel Locked', color=discord.Color.red())
        embed.add_field(name='Channel', value=ctx.channel.mention)
        embed.add_field(name='Moderator', value=ctx.author.mention)
        await ctx.send(embed=embed)

    @commands.command(name='unlock', help='Unlock a channel')
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        embed = discord.Embed(title='Channel Unlocked', color=discord.Color.green())
        embed.add_field(name='Channel', value=ctx.channel.mention)
        embed.add_field(name='Moderator', value=ctx.author.mention)
        await ctx.send(embed=embed)

    @commands.command(name='timeout', help='Timeout a member (mute in Discord)')
    @commands.has_permissions(manage_guild=True)
    async def timeout(self, ctx, member: discord.Member, duration: int, *, reason='No reason provided'):
        timeout_duration = timedelta(seconds=duration)
        await member.timeout(timeout_duration, reason=reason)
        embed = discord.Embed(title='Member Timed Out', color=discord.Color.orange())
        embed.add_field(name='Member', value=member.mention)
        embed.add_field(name='Duration', value=f'{duration} seconds')
        embed.add_field(name='Reason', value=reason)
        embed.add_field(name='Moderator', value=ctx.author.mention)
        await ctx.send(embed=embed)

    @commands.command(name='untimeout', help='Remove timeout from a member')
    @commands.has_permissions(manage_guild=True)
    async def untimeout(self, ctx, member: discord.Member, *, reason='No reason provided'):
        await member.timeout(None, reason=reason)
        embed = discord.Embed(title='Member Timeout Removed', color=discord.Color.green())
        embed.add_field(name='Member', value=member.mention)
        embed.add_field(name='Reason', value=reason)
        embed.add_field(name='Moderator', value=ctx.author.mention)
        await ctx.send(embed=embed)

    @commands.command(name='nickname', help='Change a member\'s nickname')
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: discord.Member, *, nickname=None):
        await member.edit(nick=nickname)
        if nickname:
            await ctx.send(f'{member.mention} nickname changed to **{nickname}**')
        else:
            await ctx.send(f'{member.mention} nickname reset.')

    @commands.command(name='modhelp', help='Show moderation commands')
    async def modhelp(self, ctx):
        embed = discord.Embed(title='Moderation Commands', color=discord.Color.blurple())
        embed.add_field(name='!kick <member> [reason]', value='Kick a member', inline=False)
        embed.add_field(name='!ban <member> [reason]', value='Ban a member', inline=False)
        embed.add_field(name='!unban <user#discriminator> [reason]', value='Unban a user', inline=False)
        embed.add_field(name='!mute <member> [duration] [reason]', value='Mute a member', inline=False)
        embed.add_field(name='!unmute <member> [reason]', value='Unmute a member', inline=False)
        embed.add_field(name='!warn <member> [reason]', value='Warn a member', inline=False)
        embed.add_field(name='!purge [amount]', value='Delete messages', inline=False)
        embed.add_field(name='!slowmode [seconds]', value='Set channel slowmode', inline=False)
        embed.add_field(name='!lock', value='Lock a channel', inline=False)
        embed.add_field(name='!unlock', value='Unlock a channel', inline=False)
        embed.add_field(name='!timeout <member> <duration> [reason]', value='Timeout a member', inline=False)
        embed.add_field(name='!untimeout <member> [reason]', value='Remove timeout', inline=False)
        embed.add_field(name='!nickname <member> [nickname]', value='Change member nickname', inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
