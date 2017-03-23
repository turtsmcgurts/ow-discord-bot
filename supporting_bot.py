import discord
from discord.ext import commands;
import asyncio
import gaycode #where we store the bots token, so it isn't publicly displayed on github
import time

client = discord.Client()

supportList = [] #list of discord members signed up to support mixes
commandString = '!join !quit (admin !reset !shutdown)'
infoString = 'People waiting to play\n-----------'
#channelID = '288490815200821259' #channel.id identifier for the channel
channelID = '288537682538266625' #golden_support
#channelID = '288497909522104323' #test1
serverID = '212352899135569920' #goldens server
modRole = 'ow-support-admin'

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await initialStartupClear()
    await allowChatPermissions()
    time.sleep(1)
    await printWelcomeMessage()

@client.event
async def on_message(message):
    #try:
    #only worry about messages from a specific channel
    if message.channel.id == channelID:
        msg = message.content.lower()
    
        if msg.startswith('!join'):
            if message.author not in supportList:
                supportList.append(message.author)
                await printPlayerList(message.channel)
                
        elif msg.startswith('!quit'):
            if message.author in supportList:
                supportList.remove(message.author)
                #await client.send_message(message.channel, '{} quit'.format(message.author.name))
                await printPlayerList(message.channel)
            else:
                await client.delete_message(message)
                
        elif msg.startswith('!list'):
            await printPlayerList(message.channel)
            
        elif msg.startswith('!channels'):
            await client.delete_message(message)
            if checkIfRole(message.author, modRole):
                channels = client.get_all_channels()
                for c in channels:
                    print('Channel \'{}\' has ID \'{}\' on server \'{}\''.format(c.name, c.id, c.server.name))
                
        elif msg.startswith('!reset'):
            await client.delete_message(message)
            if checkIfRole(message.author, modRole):
                supportList[:] = []
                await printPlayerList(message.channel)
                
        elif msg.startswith('!shutdown'):
            if checkIfRole(message.author, modRole):
                await purgeChannel(message.channel)
                time.sleep(1)
                await printOfflineMessage()
                await removeChatPermissions(message.channel)
                time.sleep(1)
                await client.logout()
                
        elif msg.startswith('!clear'):
            await purgeChannel(message.channel)

        elif msg.startswith('!t'):
            await removeChatPermissions(message.channel)
            
        else:
            if message.author != client.user:
                #print('deleting message from {}'.format(message.author.name))
                await client.delete_message(message)
    #except:
    #    print('error')

async def initialStartupClear():
    channels = client.get_all_channels()
    for c in channels:
        if c.id == channelID:
            await purgeChannel(c)
            break
    
async def printPlayerList(channel):
    await purgeChannel(channel)
    
    str = ''
    count = 1
    for member in supportList:
        str += '{}. {}\n'.format(count, member.name)
        count = count + 1
    
    #await client.send_message(channel, commandString)
    #await client.send_message(channel, 'People waiting to play ({})'.format(len(supportList)))
    #await client.send_message(channel, '----------')
    
    #for member in supportList:
    #    await client.send_message(channel, '{}. {}'.format(count, member.name))
    #    count = count + 1
    
    await client.send_message(channel, '```{}\n\n{}\n{}```'.format(commandString, infoString, str))

async def purgeChannel(channel):
    await client.purge_from(channel, limit=500, check=None)

async def printWelcomeMessage():
    #look for channel via ID
    channels = client.get_all_channels()
    for c in channels:
        if c.id == channelID:
            await client.send_message(c, '```{}\n\n{}```'.format(commandString, infoString))
            break

async def printOfflineMessage():
    #look for channel via ID
    channels = client.get_all_channels()
    for c in channels:
        if c.id == channelID:
            await client.send_message(c, '```Bot is currently offline.```')
            break
            
async def allowChatPermissions():
    try:
        serv = client.get_server('212352899135569920')
        roles = serv.role_hierarchy
        
        channels = client.get_all_channels()
        for c in channels:
            if c.id == channelID:
                for role in roles:
                    #print('{} + {}'.format(ro.name, ro.id))
                    if (role.id == '263329758828298262'):
                        #print('role: {}'.format(role.name))
                        overwrite = discord.PermissionOverwrite()
                        overwrite.send_messages = True
                        overwrite.read_messages = True
                        
                        await client.edit_channel_permissions(c, role, overwrite)
                        break
    except:
        print ('allowChatPermissions error')
            
async def removeChatPermissions(channel):
    try:
        serv = client.get_server('212352899135569920')
        roles = serv.role_hierarchy
        
        for role in roles:
            #print('{} + {}'.format(ro.name, ro.id))
            if (role.id == '263329758828298262'):
                print('role: {}'.format(role.name))
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = False
                overwrite.read_messages = True
                
                await client.edit_channel_permissions(channel, role, overwrite)
                break
    except:
        print ('removeChatPermissions error')
                    
def checkIfRole(user, role):
    role = discord.utils.find(lambda r: r.name == role, user.roles)
    #print('role {}'.format(role))
    return role is not None

client.run(gaycode.token)
