import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Bot is online')


@bot.event
async def on_message(ctx):   # проблема того, что сообщения чодержащие слово тоже удаляются
    file = open('cens.txt', 'r')
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    file.close()
    for i in lines:
        if i.lower() in ctx.content.split() or i.upper() in ctx.content.split():
            await ctx.delete()      # удаляет сообщение
    await bot.process_commands(ctx)             # позволяет обрабатывать команды


@bot.event
async def on_member_join(member):
    assist = ['Commands:',
              ' User:',
              '    !help_bot',
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
    await member.create_dm()
    await member.dm_channel.send(f'Привет, {member.mention}!, вот что я могу:')
    await member.dm_channel.send("\n".join(assist))

for file in os.listdir("data"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"data.{name}")

print('Введите токен')
bot.run(input())
