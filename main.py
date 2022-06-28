import discord
from discord.ext import commands, tasks
import csv
from pycoingecko import CoinGeckoAPI
import json
from itertools import cycle

class CustomHelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        await self.get_destination().send('''```
Main:
    abbriviation - Gives the meaning of common abbriviations used in crypto currency
    price - Returns the current price of a crypto currency
    trending - Returns information about the top 3 trending crypto currencies
Misc:
    learn - Links you to the best place to learn about trading crypto currencies
    donate - Links you to where you can support the developer of this bot.
    help - Sends this message

Type $.help command for more info on a specific command
For more help, contact me on twitter: @BO55_JSR```''')

    async def send_command_help(self, command):
        if command.name == "abbreviation":
            await self.get_destination().send('''```
Usage: $.abbreviation [abbreviation]
Example: $.abbreviation rr --> RR - Risk to reward```''')
        elif command.name == "price":
            await self.get_destination().send('''```
Usage: $.price [coin]
Example: $.price bitcoin --> bitcoin: usd: 35000```''')
        else:
            await self.get_destination().send("```This command does not have any required parameters.```")

cg = CoinGeckoAPI()
client = commands.Bot(command_prefix = "$.", help_command=CustomHelpCommand())
status = cycle(["Prefix is $.","Github: JaydenRA"])

@client.event
async def on_ready():
    change_status.start()
    print("Online")

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required arguments.")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command does not exist. Maybe check your spelling.")

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
async def trending(ctx):
    trending = cg.get_search_trending()

    app_json = json.dumps(trending)
    apps_json = json.loads(app_json)
    coins = apps_json["coins"]

    firstname = "Name: ", coins[0]["item"]["name"]
    firstsymbol = "Symbol", coins[0]["item"]["symbol"]
    firstrank = "Rank", coins[0]["item"]["market_cap_rank"]
    firstprice = "BTC Price", coins[0]["item"]["price_btc"]

    secondname = "Name: ", coins[1]["item"]["name"]
    secondsymbol = "Symbol", coins[1]["item"]["symbol"]
    secondrank = "Rank", coins[1]["item"]["market_cap_rank"]
    secondprice = "BTC Price", coins[1]["item"]["price_btc"]

    thirdname = "Name: ", coins[2]["item"]["name"]
    thirdsymbol = "Symbol", coins[2]["item"]["symbol"]
    thirdrank = "Rank", coins[2]["item"]["market_cap_rank"]
    thirdprice = "BTC Price", coins[2]["item"]["price_btc"]
    
    first = f"1) \n {firstname} \n {firstsymbol} \n {firstrank} \n {firstprice}"
    second = f"2) \n {secondname} \n {secondsymbol} \n {secondrank} \n {secondprice}"
    third = f"3) \n {thirdname} \n {thirdsymbol} \n {thirdrank} \n {thirdprice}"

    await ctx.send(first)
    await ctx.send(second)
    await ctx.send(third)
    
@client.command()
async def learn(ctx):
    await ctx.send("To learn from the best traders, join Crypto Goats!\nhttps://discord.gg/RnBsskz7Z9")

@client.command()
async def donate(ctx):
    await ctx.send("All donations are greatly appriciated can can be sent here:\nhttps://www.buymeacoffee.com/jaydenra")

client.run("OTkwNTc4MzkzNTIxMjEzNDcw.G0Jhtk.ROXDtS0ISE964Dk8RQO_UC4Nie-JoB1zbOrbqU")