import asyncio

from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.helpers.aiohttp_helper import AioHttp
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command(["define", "dict"], ".") & filters.me)
async def define(bot: UserBot, message: Message):
    """Thank you Poki!!"""
    cmd = message.command

    input_string = ""
    if len(cmd) > 1:
        input_string = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        input_string = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`Can't pass to the void.`")
        await asyncio.sleep(2)
        await message.delete()
        return

    def combine(meaning):
        w_word = f"**__{meaning.get('partOfSpeech', 'word').title()}__**\n"
        for i in meaning.get("definitions", []):
            w_word += f"\n**Definition**\n`{i.get('definition', '')}`"
            if i.get("example"):
                w_word += f"\n**Example**\n`{i['example']}`"
            if i.get("synonyms"):
                w_word += f"\n**Synonyms:** `{', '.join(i['synonyms'])}`"
            if i.get("antonyms"):
                w_word += f"\n**Antonyms:** `{', '.join(i['antonyms'])}`"
        w_word += "\n\n"
        return w_word

    def out_print(word1):
        out = ""
        for meaning in word1.get("meanings", []):
            out += combine(meaning)
        if "title" in list(word1):
            out += (
                "**__Error Note__**\n\n▪️`"
                + word1["title"]
                + "\n\n▪️"
                + word1["message"]
                + "\n\n▪️<i>"
                + word1["resolution"]
                + "</i>`"
            )
        return out

    if not input_string:
        await message.edit("`Plz enter word to search‼️`")
    else:
        word = input_string
        try:
            r_dec = await AioHttp().get_json(
                f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            )
        except Exception as e:
            print(e)
            await message.edit(
                "`The dictionary API is unreachable right now. Try again later.`"
            )
            return

        v_word = input_string
        if isinstance(r_dec, list):
            r_dec = r_dec[0]
            v_word = r_dec["word"]
        last_output = out_print(r_dec)
        if last_output:
            await message.edit(
                "`Search result for   `" + f" {v_word}\n\n" + last_output
            )
        else:
            await message.edit("`No result found from the database.`")


# Command help section
add_command_help(
    "dictionary",
    [
        [".define | .dict", "Define the word you send or reply to."],
    ],
)
