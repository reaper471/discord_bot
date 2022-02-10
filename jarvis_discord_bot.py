import discord
from discord.abc import Messageable
import io
import aiohttp

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

admin_id = "" #admin id for DM and stuff
guild_id = "" #server_id as this is a static bot
greeting_channel = "" #the channel where greetings and exiting messages will show up
guild = client.get_guild(guild_id) 
global channel_id

channel_id = "" #the channel ID where it would message "Online and Ready..." when started as well as read all the commands.

@client.event
async def on_ready():

    
    channel = client.get_channel(channel_id)
    await channel.send("Online and Ready...")


@client.event
async def on_message(message):

    message_str = str(message.content)

#    message.content = message.content.lower() # its not necessary but it would change the entire message to lower case for simplicity.

    print(str(message.author)+' in channel "'+ str(message.channel) +'" : '+message.content)
  
    if message.author == client.user:
        return
    
    if "Direct Message" in str(message.channel):

        user = await client.fetch_user(admin_id)

        if "$imp$" in message_str:
            
            await message.channel.send("Message sent as Important.:file_cabinet:")

        channel = await user.create_dm()

        try:
            url = message.attachments[0].url
            print(url)

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        return await channel.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    await channel.send(file=discord.File(data, 'image.png'))
        except:
            pass

        await channel.send(f'DM from "{str(message.author)}"\n{message_str}')

    
    if str(message.author) == "Xeklev#8522" or str(message.author) == "Zenso#9551": #put admin names here as this bot will only reply to their commands.

        
        if str(message.channel.id) == channel_id                :
            command_channel = message.channel

            if "help$" in message_str:
                embed = discord.Embed(title = "COMMANDS",description ="" , color=0x05152D)           
                embed.add_field(name = "{channel}say${message}" , value = "To send a **message** in a **channel**. Default channel would be the one in which **you are messaging**" , inline = False)
                embed.add_field(name = "{channel}clear${clear count}" , value = "To clear messages in a channel")

                await command_channel.send(embed = embed)


            if "say$" in message_str:

                message_lst = message_str.split("say$")

                say_message = message_lst[1]

                if "#" in message_str and "<" in message_str:

                    say_channel = message_lst[0]
                    say_channel = client.get_channel(int(say_channel[int(say_channel.find("#"))+1:int(say_channel.find(">"))]))
                    await say_channel.send(say_message)

                else:
                    await command_channel.purge(limit=1)
                    await command_channel.send(say_message)


            if "clear$" in message_str:

                clr_temp = str(message.content).split("clear$")

                clr_count = clr_temp[1]
                clr_temp_channel = clr_temp[0]

                if "#" in message_str and "<" in message_str:

                    clr_channel =  client.get_channel(int(clr_temp_channel[int(clr_temp_channel.find("#"))+1:int(clr_temp_channel.find(">"))]))
                
                else:
                    clr_channel = command_channel
  
                await clr_channel.purge(limit=int(clr_count))
                await clr_channel.send("messages cleared! :grin:")

            if message.content.startswith("hello <@!852935455162236958>"):
                await command_channel.send("Hello "+ message.author.mention +"")

            if message.content.startswith(":rofl:"):
                await command_channel.send(":rofl:")

            if message.content.startswith("how are you <@!852935455162236958>"):
                await command_channel.send("I'm fine, What about you")

            if message.content.startswith("right <@!852935455162236958>"):
                await command_channel.send("yep")

            
            if message.content.startswith("member info"):
                guild = client.get_guild(guild_id)
                await command_channel.send(guild)   
                member_count = 0       
                for members in guild.members:
                    member_count = member_count + 1
                    await command_channel.send("member no."+ str(member_count)+ "   " +str(members))
                
                await command_channel.send("-------------------------------------")
                await command_channel.send("Completed"+ message.author.mention)
                await command_channel.send("Total Members="+str(member_count))
            
@client.event
async def on_member_remove(member):
    member_av = member.avatar_url
    await client.wait_until_ready()
    
    channel = client.get_channel(greeting_channel)
    embedVar = discord.Embed(title= "Member Left!", description=f"**Sadly** {member.mention} left the **{client.get_guild(guild_id).name}!**", color=0x05152D)
    embedVar.set_thumbnail(url=member_av)
    await channel.send(embed=embedVar)


@client.event
async def on_member_join(member):
    member_av = member.avatar_url
    await client.wait_until_ready()

    
    
    channel = client.get_channel(greeting_channel)
    embedVar = discord.Embed(title= "Member Joined!", description=f"**Hello!** {member.mention} and **Welcome** to the **{client.get_guild(guild_id).name}!**\nHope you like it here. :grin:", color=0x05152D)
    embedVar.set_image(url=member_av)
    await channel.send(embed=embedVar)

print("Online and Ready...")

bot_code_file = open("token.txt","r")
token = bot_code_file.readline()
client.run(token,bot=True) #create a token.txt and add your discord bot token in it 




