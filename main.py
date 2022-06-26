import discord
from discord.ext import commands
import csv

client = commands.Bot(command_prefix = "$.")

@client.event
async def on_ready():
    print("Online")

@client.command()
async def abbriviation(ctx, question):
    csv_file = csv.reader(open("abbriviations.csv", "r"), delimiter=",")
    for row in csv_file:
        if question.upper() == row[0]:
            await ctx.send(row)

client.run("OTkwNTc4MzkzNTIxMjEzNDcw.G0Jhtk.ROXDtS0ISE964Dk8RQO_UC4Nie-JoB1zbOrbqU")