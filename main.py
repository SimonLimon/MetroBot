import metro
from datetime import datetime
from discord.ext import commands
from webserver import keep_alive

bot = commands.Bot(command_prefix="!")

metroToken = metro.generate_token()
lastTime = datetime.now()

def updateToken():
    global metroToken
    global lastTime
    now = datetime.now()
    print(now)
    if (lastTime != None and (now - lastTime).total_seconds() > 3600):
        metroToken = metro.generate_token()
        lastTime = now
    if (lastTime == None):
        lastTime = now
    print(metroToken)
    return metroToken


def isMetroOpen():
    now = datetime.now()
    return not (now.hour() <= 6 and now.hour() > 1)


@bot.event
async def on_start():
    print("Bot is online")


@bot.command()
async def info(ctx):
    res = ""
    stations_codes = metro.station_id_codes
    stations_names = metro.station_names
    for id in range(len(stations_codes)):
        res = res + stations_codes[id] + ": " + stations_names[id] + "\n"
    await ctx.send("commands\n" + "!getTrip `ID da estacao`\n" +
                   "All station ids: \n" + res)


@bot.command()
async def getTrip(ctx, arg1):
    if (isMetroOpen):
        await ctx.send(metro.request_time(arg1.upper(), updateToken()))
    else:
        await ctx.send("Metro is closed reopens at 6.30h")


@bot.command()
async def getToken(ctx):
    await ctx.send(updateToken())


keep_alive()

token = ("OTY3MTkzMTY0ODQ4OTg4MzAw.YmMu1A.SyN8CIJxhoBea0WOTSgVVLd5-aY")
bot.run(token)
