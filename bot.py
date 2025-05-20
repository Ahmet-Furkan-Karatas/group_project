import discord
from discord.ext import commands
from config import TOKEN, DATABASE
from logic import DatabaseManager
import openai

# Bot ayarları
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Veritabanı yöneticisi
db = DatabaseManager(DATABASE)

@bot.command()
async def info(ctx):
    await ctx.send("""
!günlük yaz\n
!günlük liste\n
!günlük sil <id>\n
!günlük ara <kelime>\n
!günlük düzenle <id> <yeni metin>\n
!günlük rapor <id>        
""")

@bot.command()
async def günlük(ctx, işlem=None, *, veri=None):
    user_id = ctx.author.id

    if işlem == "yaz":
        await ctx.send("📅 Lütfen günlüğünüz için tarihi girin (örnek: 2025-05-13):")
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        date_message = await bot.wait_for('message', check=check)
        date_str = date_message.content.strip()

        await ctx.send("📝 Lütfen günlüğünüzü yazın:")
        content_message = await bot.wait_for('message', check=check)
        content = content_message.content.strip()

        db.add_entry(user_id, content, date_str)
        await ctx.send(f"✅ Günlük kaydedildi. Tarih: {date_str}")

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

    elif işlem == "rapor" and veri:
        entry_id = int(veri)
        entry = db.get_entry(user_id, entry_id)

        if entry:
            text = entry[1]
            response = openai.Completion.create(
                model="gpt-4.1",
                prompt=f"Bu metni analiz et ve yazan kişinin ruh hali hakkında kısa bir psikolojik rapor oluştur:\n\n'{text}'",
                max_tokens=150,
                temperature=0.7
            )
            report = response.choices[0].text.strip()
            await ctx.send(f"📜 **Psikolojik Rapor** (Günlük ID: {entry_id}):\n{report}")
        else:
            await ctx.send("Geçersiz günlük ID'si.")
    
    else:
        await ctx.send("Komut hatalı. Kullanım:\n"
                       "`!günlük yaz`\n"
                       "`!günlük liste`\n"
                       "`!günlük sil <id>`\n"
                       "`!günlük ara <kelime>`\n"
                       "`!günlük düzenle <id> <yeni metin>`\n"
                       "`!günlük rapor <id>`")

bot.run(TOKEN)
