import discord
import asyncio
import sqlite3
import os
import time
import requests
from pydeezer import Deezer
from discord import opus
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord import FFmpegPCMAudio
from discord.utils import get
from pydeezer.constants import track_formats
from discord.utils import get

print('Music')
download_dir = "Way to project file"
arl = "Deezer arl"
deezer = Deezer(arl=arl)
user_info = deezer.user
OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll','libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']


def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        print('Opus was loaded')
        return True

    for opus_lib in opus_libs:
            try:
                opus.load_opus(opus_lib)
                return
            except OSError:
                pass

    raise RuntimeError('Could not load an opus lib. Tried %s' %(', '.join(opus_libs)))


load_opus_lib()


url = "https://deezerdevs-deezer.p.rapidapi.com/search"
headers = {
    'x-rapidapi-host': "deezerdevs-deezer.p.rapidapi.com",
    'x-rapidapi-key': "08feec074fmshea6c1b5cf32caeap1d2e17jsn7732297ec066"
    }


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.con = sqlite3.connect("playlists.db")
        self.cur = self.con.cursor()
        self.music = None
        self.playm = False
        self.ider = 0

    @commands.command(name='playlist.add')
    async def playlist(self, ctx):
        id_zapros = ctx.author.id
        res = self.cur.execute(f"""CREATE table IF NOT EXISTS "{str(id_zapros)}" (
                    'title' TEXT,
                     'way' TEXT)""")
        if self.music != None:
            response = self.cur.execute(f'SELECT title from "{str(id_zapros)}"').fetchall()
            response1 = self.cur.execute(f'SELECT title from "{str(id_zapros)}" WHERE title = ?',
                                         (str(self.title),)).fetchall()
            if len(response1) == 0 and len(response) < 5:
                res1 = self.cur.execute(f'INSERT INTO "{id_zapros}"(title, way) VALUES(?, ?)',
                                        (str(self.title), str(self.music)))
                self.con.commit()
                await ctx.send('Аудиозапись добавлена')
            elif len(response) >= 5:
                await ctx.send('Достигнут лимит на количество аудиозаписей в плейлисте')
            elif len(response1) > 0:
                await ctx.send('Аудиозапись уже в плейлисте')
        else:
            await ctx.send('Аудиозапись не выбрана')

    @commands.command(name='playlist.show')
    async def playlistshow(self, ctx):
        id_zapros = ctx.author.id
        res = self.cur.execute(
            f"""CREATE table IF NOT EXISTS "{str(id_zapros)}" (
                                'title' TEXT,
                                 'way' TEXT)""")
        res1 = self.cur.execute(f'SELECT * FROM "{str(id_zapros)}" ').fetchall()
        if len(res1) != 0:
            for lines in res1:
                for elem in lines:
                    await ctx.send(elem)
        else:
            await ctx.send('Плейлист пуст')

    @commands.command(name='search')
    async def music(self, ctx, *name):
        if bool(name):
            name1 = ''
            for i in name:
                name1 = name1 + ' ' + i
            querystring = {"q": name1}
            response = requests.request("GET", url, headers=headers, params=querystring)
            if response.json()['data'] != []:
                self.title = response.json()['data'][0]['title']
                self.music = response.json()['data'][0]['link']
                self.id = response.json()['data'][0]['id']
                await ctx.send(self.music)
            else:
                await ctx.send('Аудиозапись не найдена')
        else:
            await ctx.send('Повторите попытку и введите название аудиозаписи')

    async def connect(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client:
            voice_client.stop()
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if not channel:
                await ctx.send("You are not connected to a voice channel")
                return
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()

    @commands.command(name='play')
    async def player(self, ctx):
        if self.playm is True:
            self.playm = False
        if self.music is not None:
            voice_client = get(self.bot.voice_clients, guild=ctx.guild)
            if voice_client:
                await ctx.send('Аудиозапись уже запущена')
            if ctx.author.voice:
                await Music.connect(self, ctx)
                await ctx.send('Ожидайте')
                for file in os.listdir('./'):
                    try:
                        if file.endswith('.mp3') or file.endswith('.lrc'):
                            os.remove(file)
                    except PermissionError:
                        pass
                track_id = self.id
                track = deezer.get_track(track_id)
                track["download"](download_dir, quality=track_formats.MP3_320)
                for file in os.listdir('./'):
                    try:
                        if file.endswith('.mp3'):
                            os.rename(file, 'music.mp3')
                    except PermissionError:
                        pass
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('music.mp3'))
                ctx.voice_client.play(source, after=None)
            else:
                await ctx.send('Вы не в звуковом канале')
        else:
            await ctx.send('Аудиозапись не выбрана')

    def play1(self, ctx):
        if self.playm is True:
            self.con = sqlite3.connect("playlists.db")
            self.cur = self.con.cursor()
            id_zapros = ctx.author.id
            res1 = self.cur.execute(f'SELECT * FROM "{str(id_zapros)}" ').fetchall()
            if len(res1) != 0:
                if self.ider + 1 > len(res1):
                    self.ider = 0
                else:
                    pass
                name = res1[self.ider][0]

                voice = get(self.bot.voice_clients, guild=ctx.guild)
                querystring = {"q": name}
                response = requests.request("GET", url, headers=headers, params=querystring)
                for file in os.listdir('./'):
                    try:
                        if file.endswith('.mp3') or file.endswith('.lrc'):
                            os.remove(file)
                    except PermissionError:
                        print('Warning')
                if response.json()['data'] != []:
                    self.id = response.json()['data'][0]['id']
                    track_id = self.id
                    track = deezer.get_track(track_id)
                    track["download"](download_dir, quality=track_formats.MP3_320)
                for file in os.listdir('./'):
                    try:
                        if file.endswith('.mp3'):
                            os.rename(file, 'music.mp3')
                    except PermissionError:
                        pass
                self.ider += 1
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('music.mp3'))
                ctx.voice_client.play(source, after=lambda s: Music.play1(self, ctx))

    @commands.command(name='playlist.go')
    async def plgo(self, ctx):
        if ctx.author.voice:
            if self.playm is False:
                voice_client = get(self.bot.voice_clients, guild=ctx.guild)
                if voice_client and voice_client.is_paused() is False:
                    voice_client.stop()
                id_zapros = ctx.author.id
                res = self.cur.execute(
                    f"""CREATE table IF NOT EXISTS "{str(id_zapros)}" (
                                                                    'title' TEXT,
                                                                     'way' TEXT)""")
                self.playm = True
                self.ider = 0
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                await Music.connect(self, ctx)
                Music.play1(self, ctx)
            else:
                await ctx.send('Плейлист уже запущен')
        else:
            await ctx.send('Вы не в звуковом канале')

    @commands.command(name='playlist.stop')
    async def plstop(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if self.playm is True:
            self.playm = False
        if voice_client and voice_client.is_paused() is False:
            voice_client.stop()

    @commands.command(name='pause')
    async def pause(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_paused() is False:
            voice_client.pause()

    @commands.command(name='resume')
    async def resume(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_paused() is True:
            voice_client.resume()

    @commands.command(name='stop')
    async def stop(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_paused() is False:
            voice_client.stop()
            await ctx.send('Остановлено')

    @commands.command(name='playlist.clear')
    async def clear(self, ctx):
        self.con = sqlite3.connect("playlists.db")
        self.cur = self.con.cursor()
        id_zapros = ctx.author.id
        res = self.cur.execute(
            f"""CREATE table IF NOT EXISTS "{str(id_zapros)}" (
                                        'title' TEXT,
                                         'way' TEXT)""")
        res1 = self.cur.execute(f'DELETE FROM "{str(id_zapros)}"')
        await ctx.send('Плейлист очищен')
        self.con.commit()

    @commands.command(name='playlist.clearone')
    async def clearone(self, ctx, *title):
        id_zapros = ctx.author.id
        self.con = sqlite3.connect("playlists.db")
        self.cur = self.con.cursor()
        if bool(title):
            name1 = ''
            for i in title:
                name1 = name1 + ' ' + i
                querystring = {"q": name1}
                response = requests.request("GET", url, headers=headers, params=querystring)
                if response.json()['data'] != []:
                    self.music = response.json()['data'][0]['link']
                    res1 = self.cur.execute(f'DELETE FROM "{str(id_zapros)}" WHERE way = "{self.music}"')
                    self.con.commit()


    @commands.command(name='help.music')
    async def help_music(self, ctx):
        messages = ['!music.search (название_аудиозаписи) - Найти и выбрать аудиозапись',
                    '!playlist.addm - Добавить аудиозапись в плейлист(сначала нужно найти аудиозапись)',
                    '!playlist.show - Показать плейлист',
                    '!playlist.clear - Очистить плейлист',
                    '!playlist.clearone (название_аудиозаписи) - Удалить одну аудиозапись из плейлиста',
                    '!help.player - Команды плеера']
        for message in messages:
            await ctx.send(message)

    @commands.command(name='help.player')
    async def help_player(self, ctx):
        await ctx.send('!skip - Пропустить аудиозапись')
        await ctx.send('!pause - Остановить аудиозапись')
        await ctx.send('!resume - Продолжить аудиозапись')

    @commands.command(name='инструкция')
    async def instuction(self, ctx):
        await ctx.send('1) Находите аудиозапись с помощью команды !search')
        await ctx.send('2) Запускаете плеер с помощью команды !play')
        await ctx.send('2.1) Чтобы остановить аудиозапись используйте команду !pause')
        await ctx.send('2.2) Чтобы продолжить аудиозапись используйте команду !resume')
        await ctx.send('2.2) Чтобы прервать аудиозапись используйте команду !stop')
        await ctx.send('3) Добавьте вашу аудиозапись в ваш плейлист командой !playlist.addmusic')
        await ctx.send('3.1) Покажите ваш плейлист командой !playlist.show')
        await ctx.send('3.2) Очистите ваш плейлист командой !playlist.clear')
        await ctx.send('3.2.1) Удалите аудиозапись из плейлиста командой !playlist.clearone')
        await ctx.send('3.3) Чтобы запустить плейлист используйте команду !playlist.go')
        await ctx.send('3.3.1) Чтобы прервать плейлист используйте команду !playlist.stop')


def setup(bot):
    bot.add_cog(Music(bot))
