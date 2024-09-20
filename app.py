import discord # type: ignore
import os
import asyncio
from dotenv import load_dotenv
from test_openArticleFromHome import get_article_data
from ai import create_summary

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$report'):
        await message.channel.send("Making your report...")
        # Fetch article data
        url = "https://apnews.com/politics"
        article_data = await get_article_data(url)

        # Generate summary
        summary = create_summary(article_data)

        # Send summary and URL to the Discord channel
        await message.channel.send(f"**Headline:**\n{article_data['headline']}\n\n"
                                  f"**Info:**\n{summary}\n\n"
                                  f"**Read more:**\n{article_data['url']}")

client.run(os.getenv("DISCORD_BOT_TOKEN"))