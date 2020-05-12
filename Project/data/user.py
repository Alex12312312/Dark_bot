import discord
import random
import requests
import asyncio
from discord.ext import commands
print('User')


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help_bot')
    @commands.guild_only()
    async def help_bot(self, ctx):
        assist = ['Commands:',
                  ' User:',
                  '    !help',
                  '    !random_n - (min, max, quantity=1) рандомное число',
                  '    !random_answer - рандомный ответ да/нет',
                  '    !cat - рандомная картинка ',
                  '    !dog - рандомная картинка ',
                  '    !bird - рандомная картинка ',
                  ' Admin:',
                  '    !admin - владелец сервера',
                  '    !turn_off - отключение бота',
                  '    !cens_w - (*arg) добавление цензуры',
                  '    !cens_r - чтение цензуры',
                  '    !cens_d - (*arg) удаление цензуры',
                  '    !ban - (member)бан уастника сервера',
                  '    !clear -(limit=100) удаляет сообщения в чате'
                  ' Music:',
                  '    !search.music (название_аудиозаписи) - Найти аудиозапись',
                  '    !add_to_playlist - Добавить аудиозапись в плейлист(сначала нужно найти аудиозапись)',
                  '    !playlistshow - Показать плейлист',
                  '    !playlist.clear - Очистить плейлист',
                  '    !playlist.clear.one (название_аудиозаписи) - Удалить одну аудиозапись из плейлиста']
        await ctx.send("\n".join(assist))



    @commands.command(name='random_n')
    @commands.guild_only()
    async def random_n(self, ctx, min=0, max=100, q=1):
        string = ''
        for _ in range(q):
            string = string + ' | ' + str(random.randint(int(min), int(max))) + ' | '
        await ctx.send(string)

    @commands.command(name='random_answer')
    @commands.guild_only()
    async def random_answer(self, ctx):
        num = random.randint(0, 1)
        if num == 0:
            answer = 'no'
        if num == 1:
            answer = 'yes'
        await ctx.send(answer)

    @commands.command(name='cat')
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.member)
    async def cat(self, ctx):
        req = requests.request(url='https://api.thecatapi.com/v1/images/search', method='GET')
        await ctx.channel.send(req.json()[0]['url'])

    @commands.command(name='dog')
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.member)
    async def dog(self, ctx):
        req = requests.request(url='https://dog.ceo/api/breeds/image/random', method='GET')
        await ctx.channel.send(req.json()['message'])

    @commands.command(name='bird')
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.member)
    async def bird(self, ctx):
        req = requests.request(url='https://api.alexflipnote.dev/birb', method='GET')
        await ctx.channel.send(req.json()['file'])


def setup(bot):
    bot.add_cog(User(bot))