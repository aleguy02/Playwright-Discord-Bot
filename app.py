# Need to figure out how to merge branch

import discord # type: ignore
import os
import asyncio
from dotenv import load_dotenv
from test_openArticleFromHome import get_article_data
from ai import create_summary
from parseResponse import parse_response

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
        try:
            await message.channel.send("Making your report...")
            # Fetch article data
            url = "https://apnews.com/politics"
            article_data = await get_article_data(url)

            # if getting the article data raises a timeout error then don't even try to make a summary, just send a message saying there was an
            if (article_data != 0):
                # Generate summary and list
                print("working")
                response = create_summary(article_data)
                summary, key_terms = parse_response(response)

                # Send summary and URL to the Discord channel
                await message.channel.send(f"**Headline:**\n{article_data['headline']}")
                await message.channel.send(f"**Summary:**\n{summary}")
                await message.channel.send(f"**Key Political Terms and Concepts:**\n{key_terms}")
                await message.channel.send(f"**Read more:**\n{article_data['url']}")
            else:
                await message.channel.send("Timeout error occurred. Check your connection and try again later.")
        except Exception as e:
            print(f"Error occured: {e}")
            

client.run(os.getenv("DISCORD_BOT_TOKEN"))