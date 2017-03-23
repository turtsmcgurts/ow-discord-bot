import discord
from discord.ext import commands;
import asyncio
import gaycode #where we store the bots token, so it isn't publicly displayed on github

client = discord.Client()

supportList = [] #list of discord members signed up to support mixes
commandString = '!join !quit (admin !reset !shutdown)'
infoString = 'People waiting to play\n-----------'
#channelID = '288490815200821259' #channel.id identifier for the channel
channelID = '288537682538266625' #testsupport
#channelID = '288497909522104323' #test1
modRole = 'ow-support-admin'

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await allowChatPermissions()
    await printWelcomeMessage()

@client.event
async def on_message(message):
    #only worry about messages from a specific channel
    if message.channel.id == channelID:
        if message.content.startswith('!join'):
            if message.author not in supportList:
                supportList.append(message.author)
                await printPlayerList(message.channel)
                
        elif message.content.startswith('!quit'):
            if message.author in supportList:
                supportList.remove(message.author)
                #await client.send_message(message.channel, '{} quit'.format(message.author.name))
                await printPlayerList(message.channel)
            else:
                await client.delete_message(message)
                
        elif message.content.startswith('!list'):
            await printPlayerList(message.channel)
            
        elif message.content.startswith('!channels'):
            await client.delete_message(message)
            if checkIfRole(message.author, modRole):
                channels = client.get_all_channels()
                for c in channels:
                    print('Channel \'{}\' has ID \'{}\' on server \'{}\''.format(c.name, c.id, c.server.name))
                
        elif message.content.startswith('!reset'):
            await client.delete_message(message)
            if checkIfRole(message.author, modRole):
                supportList[:] = []
                await printPlayerList(message.channel)
                
        elif message.content.startswith('!shutdown'):
            if checkIfRole(message.author, modRole):
                await purgeChannel(message.channel)
                await printOfflineMessage(message.channel)
                await removeChatPermissions()
                await client.logout()
                
        elif message.content.startswith('!clear'):
            await purgeChannel(message.channel)

        else:
            if message.author != client.user:
                #print('deleting message from {}'.format(message.author.name))
                await client.delete_message(message)

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
    #look for channel via ID
    channels = client.get_all_channels()
    for c in channels:
        if c.id == channelID:
            #make a list of users in the channel and set can_send_messages to True
            users = client.get_all_members()
            for u in users:
                await client.set_channel_permissions(channel, u, allow.can_send_messages = True)
                break
        break
            
async def removeChatPermissions():
    #look for channel via ID
    channels = client.get_all_channels()
    for c in channels:
        if c.id == channelID:
            #make a list of users in the channel and set can_send_messages to False
            users = client.get_all_members()
            for u in users:
                await client.set_channel_permissions(channel, u, deny.can_send_messages = True)
                break
        break
        
def checkIfRole(user, role):
    role = discord.utils.find(lambda r: r.name == role, user.roles)
    #print('role {}'.format(role))
    return role is not None

client.run(gaycode.token)
