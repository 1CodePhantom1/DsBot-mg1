import discord
from discord.ext import commands, tasks
import time
import requests
#pip install googletrans==3.1.0a0
from googletrans import Translator
from discord import app_commands
import fake_useragent
import keep_alive
import shutil
import os

nwords = [
  "негр", "негры", "пидр", "пидор", "хуй", "хуесос", "нахуй", "пизда",
  "пиздец", "еблан", "уебище", "идиот", "лох", "лошара", "сука", "нeгр",
  "негp", "нeгp", "пидp", "пидоp", "пидoр", "пидop", "xуй", "хyй", "xyй",
  "eблaноид", "ахуел", "пидорасы", "сперма", "пиздa", "ЕБАНОЕ", "ПИЗДА"
]
bot = commands.Bot(intents=discord.Intents.all(), command_prefix="/")

def AIcreate(prompt):
  ua = fake_useragent.UserAgent()
  s = requests.Session()
  headers = {'User-agent': ua.ie}
  data = {
    "action": "createAIImages",
    "returnUrl": "/",
    "searchType": "aiPrompt",
    "aiPrompt": prompt,
    "numPerPage": "12",
    "currentPage": "1"
  }
  ans1 = s.post(
    "https://freeimagegenerator.com/queries/queryCreateAIImagesFromTextPrompt.php?server=1",
    data=data,
    headers=headers)
  id = ans1.text[ans1.text.find("/replicate.delivery\\/pbxt\\") +
                 27:ans1.text.find(",\"mimeType\":") - 12]
  time.sleep(8)
  url = f"https://replicate.delivery/pbxt/{id}/out-0.png"
  r = requests.get(url, stream=True)
  print("generated")
  r.raise_for_status()
  r.raw.decode_content = True
  with open('picture.png', 'wb') as file:
    shutil.copyfileobj(r.raw, file)

@bot.event
async def on_ready():
  print("Online")
  await bot.tree.sync()

@bot.tree.command(name="test")
async def test(interaction: discord.Interaction):
  await interaction.followup.send("Привет")
  await interaction.followup.send(
    f"https://i.pinimg.com/originals/e3/63/e3/e363e38ceffaece60e00b87ee4286e08.gif"
  )

@bot.tree.command(name="relise")
async def test(self):
  channel = bot.get_channel(os.environ.get("chan_ID"))
  await channel.send("Внимание бот обновлён до новой версиии")

@bot.tree.command(name="gen")
@app_commands.describe(prompt="prompt")
async def _gen(interaction: discord.Interaction, prompt: str):
  await interaction.response.defer()
  translator = Translator()
  translated = translator.translate(prompt).text
  try:
    AIcreate(translated)
    await interaction.followup.send(file=discord.File("picture.png"))
  except Exception:
    await interaction.followup.send("Failed")


@bot.event
async def on_message(message):
  ph = message.content.split(" ")
  for i in nwords:
    for x in ph:
      if x == i or x == i.title() or x == i.upper():
        auth = message.author.name
        print(auth)
        if auth == os.environ.get("bot_name"):
          continue
        await message.reply("А ТЫ НЕ АХУЕЛ МАТЕРИТЬСЯ В МОЕМ ЧАТЕ")
  await bot.process_commands(message)

keep_alive.keep_alive()
bot.run(os.environ.get("TOKEN"), reconnect=True)
