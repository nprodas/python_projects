import csv
from dotenv import load_dotenv
from os import getenv
from discord.ext import commands

load_dotenv()
token = getenv("TOKEN")

bot = commands.Bot(command_prefix="!")

@bot.command()
async def llama(ctx, llama_number):
    with open('Llama_master.csv', 'r') as llamaFile:
        reader = csv.reader(llamaFile)

        for row in reader:
            if row[0] == llama_number:
                image = row[2]
                rarity = row[3]

    response = ':llama: **Llama #{} is {}!** :llama:\n'.format(llama_number, rarity)
    await ctx.channel.send(response)
    await ctx.channel.send(image)


bot.run(token)
