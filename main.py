import discord
import unidecode
import traceback
import time
import sys
import re
import os

if len(sys.argv) == 2:
    token = sys.argv[1]
elif os.environ.get('DISCORD_TOKEN'):
    token = os.environ.get('DISCORD_TOKEN')
else:
    print("no token provided")
    quit()

bot = discord.Bot(activity=discord.Activity(type=discord.ActivityType.competing,
                                            name="typing /faq"))

i = 0
users = {}

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    try:
        if not should_reply(message):
            return

        text = unidecode.unidecode(message.content).lower()

        # If the user has used the bot in the last 15 seconds, don't bother responing
        lookup = users.get(message.author.id)
        if lookup is not None and time.time() - lookup < 15:
            return
        elif lookup is not None:
            del users[message.author.id]

        response = get_response(text)
        if response != None:
             await reply_embed(message, response)
    except:
        traceback.print_exc()

@bot.command(description="Frequently asked BleachHack questions.") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def faq(ctx, question: discord.Option(required=False)):
    response = get_response("how can " + str(question))
    if response != None:
         await ctx.respond(embed=response)
    else:
        await ctx.respond(embed=create_embed(
            "BleachHack tech support",
            "Frequently asked questions.",
            """
            /faq install
            /faq gui
            /faq adfocus
            /faq bind
            /faq sliding
            /faq dupe
            """))

def get_response(text):
    if "how" in text and ("install" in text or "download" in text):
         return create_embed(
            "BleachHack tech support",
            "How do i install BleachHack?",
            """
            1. Download Fabric for Minecraft 1.19.2, look up a tutorial if you don't know how.
            2. Go to https://bleachhack.org/ and download the latest version.
            3. If you get redirected to the adfoc.us site, click the skip button in the top right to continue to the download.
            4. Put the jar you downloaded in your mods folder.
            5. Run the game, if the BleachHack main menu appears it loaded successfully.
            """)
    elif "open" in text and ("menu" in text or "gui" in text or "cheat" in text or "mod" in text):
         return create_embed(
            "BleachHack tech support",
            "How do i open the clickgui?",
            "Press **Right Shift** to open the clickgui.")
    elif "adfocus" in text or "adfoc.us" in text:
         return create_embed(
            "BleachHack tech support",
            "Can't download/adfoc.us refused to connect??",
            "Press the skip button in the top right to continue to the download.")
    elif ("how" in text or "can" in text) and "bind" in text:
         return create_embed(
            "BleachHack tech support",
            "How do i bind/rebind/unbind a module?",
            """
            To bind a module, go in the clickgui and press a key while hoving over its bind setting. (if you can't access the ingame clickgui, bind the clickgui to a key on the main menu clickgui)
            To remove a bind, press **Delete** while binding it.
            """)
    elif "autobuild" in text:
         return create_embed(
            "BleachHack tech support",
            "How can i add custom building to AutoBuild?",
            "It currently isn't possible to do so but it will be added in a future release.")
    elif "slide" in text or "sliding" in text or "on ice" in text or "slippery" in text:
         return create_embed(
            "BleachHack tech support",
            "Why am i sliding like i'm on ice when moving?",
            "Turn off AntiHunger.")
    elif ("possible" in text or "work" in text or "know" in text or "use" in text or "can" in text) and ("dupe" in text or "duplicat" in text):
         return create_embed(
            "BleachHack tech support",
            "How do i use ___ dupe?",
            """
            **__No support will be given for dupes__**
            If you don't know what a dupe is or how it works then you shouldn't be using it.
            """)
    else:
        return None

# Returns if its a pleb or if the bot was explicitly pinged
def should_reply(message):
    return message.channel.id == 620602433915322399 and message.author is not bot.user and isinstance(message.author, discord.Member) and (len(message.author.roles) <= 2 or bot.user in message.mentions)

def reply_embed(message, embedVar):
    global users
    users[message.author.id] = time.time()
    return message.reply(embed=embedVar)

def create_embed(title, title1, text1, title2=None, text2=None):
    global i
    i = i + 1
    embedVar = discord.Embed(title=title, color=0xe4bf47 if i % 2 == 0 else 0xebafcc)
    embedVar.add_field(name=title1, value=text1, inline=False)
    if title2 is not None and text2 is not None:
        embedVar.add_field(name=title2, value=text2, inline=False)

    return embedVar

bot.run(token)
