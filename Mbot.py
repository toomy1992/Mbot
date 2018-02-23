from __future__ import print_function
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import httplib2
import os
import asyncio
import chalk
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Mbot'

bot = commands.Bot(command_prefix='mbot!')

print (discord.__version__)

@bot.event
async def on_ready():
    print ("I am running on " + bot.user.name)
    print ("With the ID: " + bot.user.id)


@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(name="{}'s info".format(ctx.message.server.name), description="Here's what I could find.", color=0x00ff00)
    embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.server.members))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)

def EmoteSwicher(x):
    return {
        '1':':one:',
        '2':':two:',
        '3':':three:',
        '4':':four:',
        '5':':five:',
        '6':':six:',
    }[x]
def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'sheets.googleapis.com-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

def GetSheetResult(rangename):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    spreadsheetId = 'spreadsheetId'
    
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangename).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        return values

def Trimer(s):
    if s.endswith(">"): s = s[:-1]
    if s.startswith("<@!"): s = s[3:]
    if s.startswith("<@"): s = s[2:]
    return s
def EmbedCreator(Tit,Txt,Plutoon):
    
    if(Plutoon =="Top"): 
        embed=discord.Embed(title=Tit, description= Txt, color=0x3498db)

    if(Plutoon =="Middle"):
        embed=discord.Embed(title=Tit, description= Txt, color=0x2ecc71)

    if(Plutoon =="Bottom"):
         embed=discord.Embed(title=Tit, description= Txt, color=0xe74c3c)

    return embed

@bot.command(pass_context=True)
async def SendPlatoonOrders(ctx):
    DiscordRes = GetSheetResult("Discord!A2:B51")
    TbStateRes = GetSheetResult("Platoon!A2:B2")
    AirPlutoonRes = GetSheetResult("Platoon!C2:Y16")
    MidlePlutoonRes = GetSheetResult("Platoon!C20:Y34")
    BottomPlutoonRes = GetSheetResult("Platoon!C38:Y52")
    for row in TbStateRes:
        Phase = row[0]
        TbS =row[1]
    
    PlutonOrders =[]
    if (TbS == "Dark Side"):
        i = 0
        if (int(Phase) > 2):
            for row in AirPlutoonRes:
                PlutonOrders.insert(i,"Top" +"1;" + row[1] + ";" + row[2])
                i +=1
                PlutonOrders.insert(i,"Top;" + "2;" + row[5] + ";" + row[6])
                i +=1
                PlutonOrders.insert(i,"Top;" + "3;" + row[9] + ";" + row[10])
                i +=1
                PlutonOrders.insert(i,"Top;" + "4;" + row[13] + ";" + row[14])
                i +=1
                PlutonOrders.insert(i,"Top;" + "5;" + row[17] + ";" + row[18])
                i +=1
                PlutonOrders.insert(i,"Top;" + "6;" + row[21] + ";" + row[22])
                i +=1
        for row in MidlePlutoonRes:
            PlutonOrders.insert(i,"Middle;" + "1;" + row[1] + ";" + row[2])
            i +=1
            PlutonOrders.insert(i,"Middle;" + "2;" + row[5] + ";" + row[6])
            i +=1
            PlutonOrders.insert(i,"Middle;" + "3;" + row[9] + ";" + row[10])
            i +=1
            PlutonOrders.insert(i,"Middle;" + "4;" + row[13] + ";" + row[14])
            i +=1
            PlutonOrders.insert(i,"Middle;" + "5;" + row[17] + ";" + row[18])
            i +=1
            PlutonOrders.insert(i,"Middle;" + "6;" + row[21] + ";" + row[22])
            i +=1
        for row in BottomPlutoonRes:
            PlutonOrders.insert(i,"Bottom;" + "1;" + row[1] + ";" + row[2])
            i +=1
            PlutonOrders.insert(i,"Bottom;" + "2;" + row[5] + ";" + row[6])
            i +=1
            PlutonOrders.insert(i,"Bottom;" + "3;" + row[9] + ";" + row[10])
            i +=1
            PlutonOrders.insert(i,"Bottom;" + "4;" + row[13] + ";" + row[14])
            i +=1
            PlutonOrders.insert(i,"Bottom;" + "5;" + row[17] + ";" + row[18])
            i +=1
            PlutonOrders.insert(i,"Bottom;" + "6;" + row[21] + ";" + row[22])
            i +=1
    else:
        i = 0
        if (int(Phase) > 2):
            for row in AirPlutoonRes:
                PlutonOrders.insert(i,"Top;" + "1;" + row[1] + ";" + row[2])
                i +=1
                PlutonOrders.insert(i,"Top;" + "2;" + row[5] + ";" + row[6])
                i +=1
                PlutonOrders.insert(i,"Top;" + "3;" + row[9] + ";" + row[10])
                i +=1
                PlutonOrders.insert(i,"Top;" + "4;" + row[13] + ";" + row[14])
                i +=1
                PlutonOrders.insert(i,"Top;" + "5;" + row[17] + ";" + row[18])
                i +=1
                PlutonOrders.insert(i,"Top;" + "6;" + row[21] + ";" + row[22])
                i +=1
        for row in MidlePlutoonRes:
            PlutonOrders.insert(i,"Middle;" + "1;" + row[1] + ";" + row[2])
            i +=1
            PlutonOrders.insert(i,"Middle;" + "2;" + row[5] + ";" + row[6])
            i +=1
            PlutonOrders.insert(i,"Middle;" + "3;" + row[9] + ";" + row[10])
            i +=1
            PlutonOrders.insert(i,"Middle;" + "4;" + row[13] + ";" + row[14])
            i +=1
            PlutonOrders.insert(i,"Middle;" + "5;" + row[17] + ";" + row[18])
            i +=1
            PlutonOrders.insert(i,"Middle;" + "6;" + row[21] + ";" + row[22])
            i +=1
        if (int(Phase) > 1):
            for row in BottomPlutoonRes:
                PlutonOrders.insert(i,"Bottom;" + "1;" + row[1] + ";" + row[2])
                i +=1
                PlutonOrders.insert(i,"Bottom;" + "2;" + row[5] + ";" + row[6])
                i +=1
                PlutonOrders.insert(i,"Bottom;" + "3;" + row[9] + ";" + row[10])
                i +=1
                PlutonOrders.insert(i,"Bottom;" + "4;" + row[13] + ";" + row[14])
                i +=1
                PlutonOrders.insert(i,"Bottom;" + "5;" + row[17] + ";" + row[18])
                i +=1
                PlutonOrders.insert(i,"Bottom;" + "6;" + row[21] + ";" + row[22])
                i +=1
    for row1 in DiscordRes:
        if(row1[1] != ''):
            id = Trimer(row1[1])
            try:
                user = await bot.get_user_info(id)
            except ValueError:
                await bot.say("user: " + row1[1] + " is not in guild")
                continue
            for row2 in  PlutonOrders:
                string = row2.split(';')
                if(string[3]==row1[0]):     
                    EmoteString =EmoteSwicher(string[1])
                    em = EmbedCreator("Phase: " + Phase + " __Plutoon:" + string[0] + "__ Plutoon Number: "+  EmoteString, string[2], string[0])
                    try:
                        await bot.send_message(user,embed = em)
                    except Exception as inst:
                        await bot.say("user: " + row1[0] + " "+ str(inst))
                        break
        else:
            await bot.say('Request finished')

bot.run("Token")