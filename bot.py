from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response


# Loading Token
load_dotenv()
token_env = os.getenv('DISCORD_TOKEN')
if token_env is None:
    raise ValueError("DISCORD_TOKEN not found; Token is None")
TOKEN: Final[str] = token_env

# Bot Setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Message Functionality
async def send_message(message: Message, user_message: str) -> None: # should return none like a void fucntion would
    if not user_message:
        print("(Message was empty because intents were not enabled probably)")
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

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