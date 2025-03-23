from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, Reaction, User, Member
from typing import Union
import responses


# Loading Token
load_dotenv()
token_env = os.getenv('DISCORD_TOKEN')
if token_env is None:
    raise ValueError("DISCORD_TOKEN not found; Token is None")
TOKEN: Final[str] = token_env

# Bot Setup
intents: Intents = Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.guilds = True
client: Client = Client(intents=intents)

# Message Functionality
async def send_message(message: Message, user_message: str) -> None: # should return none like a void fucntion would
    if not user_message:
        print("(Message was empty because intents were not enabled probably)")
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = responses.get_response(user_message)
        bot_message: Message = await message.author.send(response) if is_private else await message.channel.send(response)
        
        if response == "Here's your card!":
            await bot_message.add_reaction("✅")
            await bot_message.add_reaction("🤷")
            await bot_message.add_reaction("❌")
            
            # this is after the message gets updated with the reactions
            # Note: message.channel is where the message was sent (doesn't matter DM or server text channel)
            
            # updated_bot_message = await message.channel.fetch_message(bot_message.id)

            # reaction_list: list[Reaction] = updated_bot_message.reactions

            # if reaction_list[0].count > 1:
            #     # react_response: Message = await message.channel.send(f"You reacted to the {reaction_list[0].emoji}")
            #     await message.channel.send(f"You reacted to the {reaction_list[0].emoji}")
            # elif reaction_list[1].count > 1:
            #     await message.channel.send(f"You reacted to the {reaction_list[1].emoji}")
            # elif reaction_list[2].count > 1:
            #     await message.channel.send(f"You reacted to the {reaction_list[2].emoji}")


    except Exception as e:
        print(e)

# Reaction Handling
@client.event
async def on_reaction_add(reaction: Reaction, user: Union[User, Member]):
    # Note: in guild contexts, user can be a Member and not just a User
    emoji = reaction.emoji
    if user.bot:
        return

    if emoji == "✅":
        await reaction.message.channel.send(f"{user.name} reacted with a {reaction} on message with id: {reaction.message.id}")
    elif emoji == "🤷":
        await reaction.message.channel.send(f"{user.name} reacted with a {reaction} on message with id: {reaction.message.id}")
    elif emoji == "❌":
        await reaction.message.channel.send(f"{user.name} reacted with a {reaction} on message with id: {reaction.message.id}")

# Startup Handling
@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running!")

# Incoming Message Handling
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

# Main Entry Point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()