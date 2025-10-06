import discord
from discord.ext import commands
import asyncio

# Укажите токен бота и ID роли
DISCORD_BOT_TOKEN = "MTEzMzE0MTk0MTg1NzU1MDUxNw.GGbGd0.mnnqy-XyfAX55ph4h-tCFADaU-NfnWAI5BafPM"
MEMBER_ROLE_ID = 1424459150171045969

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True  # Включаем memessagentent intent

bot = commands.Bot(command_prefix='', help_command=None, intents=intents)


async def change_status_periodically():
    statuses = ["free external soft on roblox", "free cheat on roblox"]
    while True:
        for status in statuses:
            await bot.change_presence(activity=discord.Game(name=status))
            await asyncio.sleep(3)  # менять каждые 3 секунды


@bot.event
async def on_ready():
    if bot.user is not None:
        print(f'Бот {bot.user} успешно запущен!')
        print(f'ID бота: {bot.user.id}')
        bot.loop.create_task(change_status_periodically())
    else:
        print('Ошибка: bot.user равен None')
    print('------')


@bot.event
async def on_member_join(member):
    role = member.guild.get_role(MEMBER_ROLE_ID)
    if role is None:
        print(
            f'Ошибка: роль с ID {MEMBER_ROLE_ID} не найдена на сервере {member.guild.name}'
        )
        return
    try:
        await member.add_roles(role)
        print(
            f'✓ Роль "{role.name}" выдана участнику {member.name} ({member.id}) на сервере {member.guild.name}'
        )
    except discord.Forbidden:
        print(
            f'Ошибка: у бота нет прав для выдачи роли "{role.name}" участнику {member.name}'
        )
    except discord.HTTPException as e:
        print(f'Ошибка HTTP при выдаче роли: {e}')
    except Exception as e:
        print(f'Неожиданная ошибка при выдаче роли: {e}')


if __name__ == '__main__':
    try:
        bot.run(DISCORD_BOT_TOKEN)
    except discord.LoginFailure:
        print('Ошибка: неверный токен бота.')
    except Exception as e:
        print(f'Ошибка при запуске бота: {e}')
