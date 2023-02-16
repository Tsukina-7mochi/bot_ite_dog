from generate import generate
import sys
from typing import Optional
import discord
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("token")
    parser.add_argument("--sync-command", action="store_true")
    parser.add_argument("--ngram-n", type=int, default=3)
    args = parser.parse_args()

    token = args.token
    input_file = args.input_file
    ngram_n = args.ngram_n

    print(f"input file: {input_file}")

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)
    tree = discord.app_commands.CommandTree(client)

    @tree.command(name="botdog", description="let the dog mutter")
    @discord.app_commands.describe(first_word="first word")
    async def bot_dog_command(interaction, first_word: Optional[str]):
        if first_word == None:
            generated = generate("", input_file, ngram_n, "^", "$")
        else:
            generated = generate(first_word, input_file, ngram_n, "^", "$")

        print(f"{first_word} -> {generated}")

        await interaction.response.send_message(generated)

    @client.event
    async def on_ready():
        print(f"Logged on as {client.user}")

        if args.sync_command:
            print("Syncing slash commands...", end="")
            await tree.sync()
            print("complete")

    client.run(token)

if __name__ == "__main__":
    main()
