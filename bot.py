import discord
from discord.ext import commands
import asyncio
import logging

# Конфигурация бота
DISCORD_BOT_TOKEN = "MTEzMzE0MTk0MTg1NzU1MDUxNw.GIKXct.h04_HH3wv067mLqmF0DU5tdbD4rMIwoyYCJh8S"
MEMBER_ROLE_ID = 1424459150171045969

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiscordBot:
    def __init__(self):
        self.intents = self._setup_intents()
        self.bot = commands.Bot(
            command_prefix='', 
            help_command=None, 
            intents=self.intents
        )
        self._register_events()

    def _setup_intents(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.guilds = True
        intents.message_content = True
        return intents

    def _register_events(self):
        self.bot.event(self.on_ready)
        self.bot.event(self.on_member_join)

    async def on_ready(self):
        if self.bot.user is None:
            logger.error("Bot user is None - authentication failed")
            return

        logger.info(f"Bot {self.bot.user} started successfully")
        logger.info(f"Bot ID: {self.bot.user.id}")
        
        self.bot.loop.create_task(self._cycle_status_messages())
        logger.info("Status cycling task started")

    async def on_member_join(self, member):
        await self._assign_member_role(member)

    async def _cycle_status_messages(self):
        status_messages = [
            "free external soft on roblox", 
            "free cheat on roblox"
        ]
        
        while True:
            for status in status_messages:
                await self._update_bot_status(status)
                await asyncio.sleep(3)

    async def _update_bot_status(self, status_message):
        try:
            activity = discord.Game(name=status_message)
            await self.bot.change_presence(activity=activity)
        except Exception as error:
            logger.error(f"Failed to update status: {error}")

    async def _assign_member_role(self, member):
        role = self._get_member_role(member.guild)
        
        if role is None:
            logger.warning(f"Role {MEMBER_ROLE_ID} not found in guild {member.guild.name}")
            return

        await self._grant_role_to_member(member, role)

    def _get_member_role(self, guild):
        return guild.get_role(MEMBER_ROLE_ID)

    async def _grant_role_to_member(self, member, role):
        try:
            await member.add_roles(role)
            logger.info(
                f"Role '{role.name}' granted to {member.display_name} "
                f"({member.id}) in {member.guild.name}"
            )
        except discord.Forbidden:
            logger.error(
                f"Missing permissions to assign role '{role.name}' to {member.display_name}"
            )
        except discord.HTTPException as http_error:
            logger.error(f"HTTP error assigning role: {http_error}")
        except Exception as unexpected_error:
            logger.error(f"Unexpected error assigning role: {unexpected_error}")

    def run(self):
        try:
            self.bot.run(DISCORD_BOT_TOKEN)
        except discord.LoginFailure:
            logger.error("Invalid bot token provided")
        except Exception as startup_error:
            logger.error(f"Bot startup failed: {startup_error}")

if __name__ == '__main__':
    bot_instance = DiscordBot()
    bot_instance.run()
