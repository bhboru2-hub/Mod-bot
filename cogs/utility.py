import discord
from discord.ext import commands
import datetime

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help='Check bot latency')
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(title='Pong!', description=f'Latency: {latency}ms', color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name='serverinfo', help='Get server information')
    async def serverinfo(self, ctx):
        embed = discord.Embed(title=f'{ctx.guild.name} Server Info', color=discord.Color.blurple())
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else '')
        embed.add_field(name='Server ID', value=ctx.guild.id)
        embed.add_field(name='Owner', value=ctx.guild.owner.mention)
        embed.add_field(name='Members', value=ctx.guild.member_count)
        embed.add_field(name='Channels', value=len(ctx.guild.channels))
        embed.add_field(name='Roles', value=len(ctx.guild.roles))
        embed.add_field(name='Created', value=ctx.guild.created_at.strftime('%d/%m/%Y'))
        await ctx.send(embed=embed)

    @commands.command(name='userinfo', help='Get user information')
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(title=f'{member.name} User Info', color=discord.Color.blurple())
        embed.set_thumbnail(url=member.avatar.url if member.avatar else '')
        embed.add_field(name='Username', value=member.name)
        embed.add_field(name='User ID', value=member.id)
        embed.add_field(name='Account Created', value=member.created_at.strftime('%d/%m/%Y'))
        embed.add_field(name='Server Joined', value=member.joined_at.strftime('%d/%m/%Y'))
        embed.add_field(name='Top Role', value=member.top_role.mention)
        embed.add_field(name='Roles', value=len(member.roles) - 1)
        await ctx.send(embed=embed)

    @commands.command(name='avatar', help='Get user avatar')
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(title=f'{member.name}\'s Avatar', color=discord.Color.blurple())
        embed.set_image(url=member.avatar.url if member.avatar else '')
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
