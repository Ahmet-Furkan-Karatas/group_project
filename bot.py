import discord
from discord.ext import commands
from config import TOKEN, DATABASE
from logic import DatabaseManager

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

db = DatabaseManager(DATABASE)

@bot.command()
async def günlük(ctx, işlem=None, *, veri=None):
    user_id = ctx.author.id

    if işlem == "yaz" and veri:
        db.add_entry(user_id, veri)
        await ctx.send("✅ Günlük kaydedildi.")
    
    elif işlem == "liste":
        entries = db.get_entries(user_id)
        if entries:
            msg = "\n".join([f"{i[0]}. [{i[2]}] {i[1]}" for i in entries])
            await ctx.send(f"📘 Günlüklerin:\n{msg}")
        else:
            await ctx.send("Hiç günlük yok.")
    
    elif işlem == "sil" and veri:
        try:
            db.delete_entry(user_id, int(veri))
            await ctx.send("🗑️ Günlük silindi.")
        except:
            await ctx.send("Geçersiz ID.")
    
    elif işlem == "ara" and veri:
        results = db.search_entries(user_id, veri)
        if results:
            msg = "\n".join([f"{i[0]}. [{i[2]}] {i[1]}" for i in results])
            await ctx.send(f"🔍 Arama sonuçları:\n{msg}")
        else:
            await ctx.send("Sonuç bulunamadı.")
    
    elif işlem == "düzenle" and veri:
        try:
            entry_id, new_content = veri.split(" ", 1)
            db.update_entry(user_id, int(entry_id), new_content)
            await ctx.send("✏️ Günlük güncellendi.")
        except:
            await ctx.send("Geçersiz format. `!günlük düzenle <id> <yeni metin>` şeklinde kullan.")

    else:
        await ctx.send("Komut hatalı. Kullanım:\n"
                       "`!günlük yaz <metin>`\n"
                       "`!günlük liste`\n"
                       "`!günlük sil <id>`\n"
                       "`!günlük ara <kelime>`\n"
                       "`!günlük düzenle <id> <yeni metin>`")

bot.run(TOKEN)
