import metro
from datetime import datetime
import discord
from discord.ext import commands


bot = commands.Bot(command_prefix = "!")

metroToken = metro.generate_token()
lastTime = datetime.now()

def updateToken():
  global metroToken
  global lastTime 
  now = datetime.now()
  print(now)
  if(lastTime != None and (now - lastTime).total_seconds() > 3600):
    metroToken = metro.generate_token()
    lastTime = now
  if(lastTime == None):
    lastTime = now
  print(metroToken)
  return metroToken
  

def isMetroOpen():
  return True


@bot.event
async def on_start():
  print("Bot is online")


@bot.command()
async def info(ctx):
  res = ""
  for id in metro.station_codes():
    res = res + id + ", "
  await ctx.send("commands\n" + "!getTrip `ID da estacao`" + 
                 "info" + "All station ids: " + res)


@bot.command()
async def getTrip(ctx, arg1):
  if(isMetroOpen):
    await ctx.send(metro.request_time(arg1, updateToken()))
  else:
    await ctx.send("Metro is closed reopens at 6.30h")


@bot.command()
async def getToken(ctx):
  await ctx.send(updateToken())
  

token=("OTY3MTkzMTY0ODQ4OTg4MzAw.YmMu1A.WpmuVSHnR4vGzMjYAU8SrAB_ORI")
bot.run(token)