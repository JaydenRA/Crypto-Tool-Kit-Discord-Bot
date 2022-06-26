import discord
from discord.ext import commands
import csv
from pycoingecko import CoinGeckoAPI

client = commands.Bot(command_prefix = "$.")
cg = CoinGeckoAPI()

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Prefix is $."))
    print("Online")

@client.command()
async def abbreviation(ctx, question):
    csv_file = csv.reader(open("abbreviations.csv", "r"), delimiter=",")
    for row in csv_file:
        if question.upper() == row[0]:
            await ctx.send(f"{row[0]} - {row[1]}")

@client.command()
async def price(ctx, coin):
    price = cg.get_price(coin, 'usd')
    price = str(price)
    price = price.replace("{", "")
    price = price.replace("}", "")
    price = price.replace("'", "")
    await ctx.send(price)

@client.command()
async def learn(ctx):
    await ctx.send("To learn from the best traders, Crypto Goats is the place for you!\nhttps://discord.gg/RnBsskz7Z9")

client.run("OTkwNTc4MzkzNTIxMjEzNDcw.G0Jhtk.ROXDtS0ISE964Dk8RQO_UC4Nie-JoB1zbOrbqU")