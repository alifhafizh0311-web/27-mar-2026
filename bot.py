import discord
from discord.ext import commands
import random
from groq import Groq

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

# API
client = Groq(api_key="api_groq")

@bot.event
async def on_ready():
    print("Bot aktif sebagai " + str(bot.user))


@bot.command()
async def help(ctx):
    await ctx.send("""
EcoBot

$help 
$tips 
$fakta 
$daurulang [barang] 
""")


@bot.command()
async def tips(ctx):
    tips_list = [
        "Coba bawa botol minum sendiri biar ga beli plastik terus ",
        "Kurangi plastik sekali pakai ya ",
        "Matikan listrik kalau tidak dipakai ",
        "Pakai tas kain kalau belanja "
    ]
    await ctx.send(random.choice(tips_list))


@bot.command()
async def fakta(ctx):
    fakta_list = [
        "Plastik bisa butuh ratusan tahun buat terurai ",
        "Sampah di laut bisa membahayakan hewan ",
        "Daur ulang itu bisa menghemat energi loo!"
    ]
    await ctx.send(random.choice(fakta_list))


@bot.command()
async def daurulang(ctx, *, barang):
    try:
        await ctx.send("Tunggu ya, lagi mikirin ide...")

        prompt = """
Kamu adalah orang yang suka bikin kerajinan dari barang bekas dan menjelaskan dengan santai seperti ke teman.
Barang yang digunakan: """ + barang + """
Kasih 1 ide daur ulang yang gampang dibuat di rumah.
Jawab dengan format sederhana:
Nama Kerajinan:
...
Bahan-bahan:
- ...
Alat:
- ...
Cara Membuat:
1. ...
2. ...
Tips:
- ...
Gunakan bahasa santai, tidak kaku, dan mudah dipahami.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=500,
            messages=[
                {
                    "role": "system",
                    "content": "Kamu adalah EcoBot yang ramah dan berbicara santai seperti teman."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        hasil = response.choices[0].message.content
        await ctx.send(hasil)

    except Exception as e:
        await ctx.send("Waduh error coba lagi nanti ya")
        print(e)


bot.run("tokenbot")
