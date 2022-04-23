import metro
from datetime import datetime
import discord
import math
from discord.ext import commands


bot = commands.Bot(command_prefix = "!")

metroToken = None
lastTime = datetime.now()


def updateToken():
  global metroToken
  metroToken = "821a30a8-47cd-3abc-a0df-286c933e2a7f";
  return metroToken

def updateToken2():
  global metroToken
  global lastTime 
  now = datetime.now()
  if(lastTime == None or (math.fabs((now - lastTime).total_seconds()) > 3600)):
    metroToken = metro.generate_token()
    lastTime = now
  return metroToken


@bot.event
async def on_start():
  print("Bot is online")


@bot.command()
async def info(ctx):
  res = ""
  await ctx.send("commands")
  await ctx.send("!getTrip `ID da estacao`")
  for id in metro.station_codes():
    res = res + id + ", "
  await ctx.send("info")
  await ctx.send("All station ids: " + res)


@bot.command()
async def getTrip(ctx, arg1):
  await ctx.send(metro.request_time(arg1, updateToken()))
  

@bot.command()
async def getToken(ctx):
  await ctx.send(updateToken())
  

token=("OTY3MTkzMTY0ODQ4OTg4MzAw.YmMu1A.HXH6eBV7P-NgLwvwcEQthaZy7WY")
bot.run(token)