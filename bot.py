# bot.py
import discord
from discord.ext import commands
from logic import DatabaseManager
from config import TOKEN

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
db = DatabaseManager()
db.create_tables()  # Tabloları başta oluştur

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı!')

@bot.command()
async def gunluk(ctx, *, entry):
    db.add_user(ctx.author.id, ctx.author.name)
    db.add_entry(ctx.author.id, entry)
    await ctx.send("📔 Günlüğün veritabanına kaydedildi!")

@bot.command()
async def gunluklarim(ctx):
    entries = db.get_entries(ctx.author.id)
    if not entries:
        await ctx.send("Henüz bir günlük yazmadın.")
    else:
        mesaj = "\n\n".join([f"{tarih}: {icerik}" for tarih, icerik in entries])
        if len(mesaj) > 1900:
            mesaj = mesaj[:1900] + "\n... (devamı var)"
        await ctx.send(f"📚 Günlüklerin:\n```\n{mesaj}\n```")

bot.run(TOKEN)
