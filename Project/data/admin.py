import discord
import time
import sys
import re
import asyncio
from discord.ext import commands
print('Admin')


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # проверка на адмиина
    @commands.command(name='admin')
    async def admin(self, ctx):
        if ctx.guild.owner_id == ctx.author.id:
            return await ctx.send(f"{ctx.author.name} be an administrator!")
        else:
            ctx.send(f"{ctx.author.name} be not an administrator!")

    # завершение работы  ???
    @commands.command(name='turn_off')
    @commands.check(commands.is_owner())
    async def turn_off(self, ctx):
        await ctx.send('The Dark_Bot is disbled')
        time.sleep(1)
        sys.exit(0)

    # запись цензуры
    @commands.command(name='cens_w')
    @commands.check(commands.is_owner())
    async def cens_w(self, ctx, *arg):
        file = open('cens.txt', 'a')
        for word in arg:
            file.write(word + '\n')
        file.close()
        await ctx.send('Added.')

    # чтение цензуры
    @commands.command(name='cens_r')
    @commands.check(commands.is_owner())
    async def cens_r(self, ctx):
        file = open('cens.txt', 'r')
        lines = file.readlines()
        lines = ' '.join(['⚫' + line for line in lines])
        file.close()
        await ctx.send(lines)


    # удаление цензуры
    @commands.command(name='cens_d')
    @commands.check(commands.is_owner())
    async def cens_d(self, ctx, *arg):
        words = arg
        file = open('cens.txt', 'r')
        lines = file.readlines()
        file.close()
        file = open('cens.txt', 'w')
        for line in lines:
            for word in words:
                if line != word + "\n":
                    file.write(line)
        file.close()
        await ctx.send('Changed.')

    @commands.command(name='ban')
    @commands.check(commands.is_owner())
    async def ban(self, ctx, member: discord.Member=None, reason=None):
        if member == None or member == ctx.message.author:
            await ctx.channel.send("You can't block yourself!")
            return
        if reason == None:
            reason = "No reason given."
        message = f"You have been banned from {ctx.guild.name} for {reason}"
        await member.send(message)
        await ctx.guild.ban(member, reason=reason)
        await ctx.channel.send(f"{member} is banned!")

    @commands.command(name='clear')
    @commands.check(commands.is_owner())
    async def clear(self, ctx, limit=100):
        await ctx.channel.purge(limit=limit + 1)


def setup(bot):
    bot.add_cog(Admin(bot))