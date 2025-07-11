import asyncio
import logging
import os

# ==============================================================================
# 1. KUTUBXONALARNI IMPORT QILISH
# ==============================================================================

# Telethon kutubxonasi (Spammer uchun)
from telethon import TelegramClient, events

# Python-telegram-bot kutubxonasi (Bot uchun)
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ConversationHandler, ContextTypes
)

# ==============================================================================
# 2. SPAMMER UCHUN SOZLAMALAR
# ==============================================================================
# 1-AKKAUNT
account1_config = {
    'session_name': 'session_account1',
    'api_id': 28876123,
    'api_hash': '9af5cd6dca1c1c8b4cd33b6b38871f6b',
    'phone_number': '+998936910996',
    'target_groups': ['https://t.me/+olbmfJIa5QJmMjdi']
}

# 2-AKKAUNT
account2_config = {
    'session_name': 'session_account2',
    'api_id': 25078976,
    'api_hash': '3730a5dd2466755d0c275d0207446708',
    'phone_number': '+998912006889',
    'target_groups': ['https://t.me/+4Xhl5D-BR2IwM2Zi']
}

# KALIT SO'ZLAR
def generate_keywords():
    base_keywords = [
        'odam bor', 'pochta bor', 'taksi kerak', 'mashina kerak',
        'kishi bor', 'ketish kerak', 'taxi kerak', 'одам бор', 
        'почта бор', 'такси керак', 'машина керак', 'киши бор', 'кетиш керак'
    ]
    return list(set([k.lower() for k in base_keywords]))

KEYWORDS = generate_keywords()

# ==============================================================================
# 3. BOT UCHUN SOZLAMALAR
# ==============================================================================
BOT_TOKEN = "8169464930:AAFFwZ25lB7FfYN4ZXSKRpL2PtO4uTBYzM8"
ADMIN_USER_ID = 213806260  # O'zingizning Telegram user ID'ingizni yozing

# Guruh linklari (global o'zgaruvchi sifatida)
PASSENGERS_GROUP_LINKS = [
    "https://t.me/Uchkoprik_Toshkent_taksi_77", 
    "https://t.me/Buvayda_Toshkent_taksi_77", 
    "https://t.me/Bogdod_Toshkent_taksi_77", 
    "https://t.me/Rishton_Toshkent_taksi_77"
]

# Holatlar uchun steyte'lar
(CHOOSING, PASSENGER_INFO) = range(2)

# Tugmalar
main_keyboard = ReplyKeyboardMarkup([["🚖 Taksi kerak"]], resize_keyboard=True)
cancel_keyboard = ReplyKeyboardMarkup([["Bekor qilish"]], resize_keyboard=True)

WELCOME_GROUPS_TEXT = (
    "🚕 Toshkent yo'nalishidagi eng faol taksi guruhlari!\n"
    "Quyidagi guruhlarga qo'shiling va kerakli yo'nalishda tez va oson taksi toping yoki haydovchi bo'ling:\n\n"
    "🔗 <a href='https://t.me/Uchkoprik_Toshkent_taksi_77'>Uchko'prik - Toshkent</a>\n\n"
    "🔗 <a href='https://t.me/Buvayda_Toshkent_taksi_77'>Buvayda - Toshkent</a>\n\n"
    "🔗 <a href='https://t.me/Bogdod_Toshkent_taksi_77'>Bog'dod - Toshkent</a>\n\n"
    "🔗 <a href='https://t.me/Rishton_Toshkent_taksi_77'>Rishton - Toshkent</a>\n\n"
    "Guruhga qo'shiling va yo'lda qolmang! 🚖\n\n"
    "ℹ️ Savollar bo'lsa, +998770805090 bilan bog'laning."
)


# ==============================================================================
# 4. SPAMMER FUNKSIYALARI (Telethon)
# ==============================================================================

async def add_spammer_event_handler(client, config):
    phone = config['phone_number']
    print(f"🎧 [SPAMMER - {phone}] Barcha guruh/kanallardan xabarlarni kuzatishni boshladi.")

    @client.on(events.NewMessage)
    async def handler(event):
        if event.is_private or not event.raw_text or not event.is_group or (event.sender and event.sender.bot):
            return
            
        message_text = event.raw_text.lower()
        if any(keyword in message_text for keyword in KEYWORDS):
            sender = await event.get_sender()
            if not sender: return

            user_link = f"@{sender.username}" if sender.username else f"[{sender.first_name}](tg://user?id={sender.id})"
            
            chat = await event.get_chat()
            group_link = f"https://t.me/{chat.username}/{event.message.id}" if hasattr(chat, 'username') and chat.username else f"https://t.me/c/{chat.id}/{event.message.id}"

            message_to_forward = (
                f"**❗️ Yangi e'lon topildi!**\n\n"
                f"**👤 Foydalanuvchi:** {user_link}\n"
                f"**📍 Guruhdan:** [Xabarga o'tish]({group_link})\n\n"
                f"**Original xabar:**\n`{event.raw_text}`"
            )

            for target_group in config['target_groups']:
                try:
                    await client.send_message(target_group, message_to_forward, parse_mode='md', link_preview=False)
                except Exception as e:
                    print(f"XATOLIK [SPAMMER - {phone} -> {target_group}]: {e}")
            
            print(f"✅ [SPAMMER - {phone}] xabar yubordi: {event.raw_text[:30]}...")

async def run_telethon_client(config):
    client = TelegramClient(config['session_name'], config['api_id'], config['api_hash'])
    
    print(f"\n>>> [SPAMMER] {config['phone_number']} akkauntiga ulanmoqda...")
    await client.start(phone=config['phone_number'])
    print(f"✅ [SPAMMER] {config['phone_number']} muvaffaqiyatli ulandi!")

    await add_spammer_event_handler(client, config)
    await client.run_until_disconnected()

async def run_spammer():
    """Telethon qismini ishga tushuruvchi asosiy funksiya."""
    print("\n🚀 SPAMMER QISMI ISHGA TUSHMOQDA...")
    tasks = [
        run_telethon_client(account1_config),
        run_telethon_client(account2_config)
    ]
    await asyncio.gather(*tasks)

# ==============================================================================
# 5. BOT FUNKSIYALARI (python-telegram-bot)
# ==============================================================================

async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Foydalanuvchiga matn, guruh linklari va tugmalarni ko'rsatadi."""
    user = update.effective_user
    caption = (
        f"Assalomu alaykum, {user.first_name}!\nXush kelibsiz!\n\n"
        f"📍 Toshkent - Bog'dod yo'nalishi uchun taksi xizmatini tez va oson toping!\n\n"
        f"🚖 Taksi kerak: Agar sizga taksi kerak bo'lsa, o'z ma'lumotlaringizni qoldiring va haydovchilar siz bilan bog'lanishadi.\n\n"
        f"{WELCOME_GROUPS_TEXT}"
    )
    # >>> O'ZGARTIRILGAN QISM: Rasm yuborish olib tashlandi. Faqat matn yuboriladi.
    await update.message.reply_text(caption, parse_mode='HTML', reply_markup=main_keyboard, disable_web_page_preview=True)
    return CHOOSING

async def choose_bot_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Foydalanuvchi tugma tanlaganda mos jarayonni boshlaydi."""
    if update.message.text == "🚖 Taksi kerak":
        await update.message.reply_text(
            "Ismingiz va telefon raqamingizni kiriting:\n(Masalan: Ali 998901234567)",
            reply_markup=cancel_keyboard
        )
        return PASSENGER_INFO
    else:
        await update.message.reply_text("Iltimos, quyidagi tugmalardan birini tanlang.", reply_markup=main_keyboard)
        return CHOOSING

async def get_passenger_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Yo'lovchi ism va telefonini oladi va guruhlarga yuboradi."""
    data = update.message.text.strip()
    parts = data.split()
    name = ' '.join(parts[:-1]) if len(parts) > 1 else data
    phone = parts[-1] if len(parts) > 1 else "-"
    
    # Barcha yo'lovchilar guruhlariga xabar yuborish
    for group_link in PASSENGERS_GROUP_LINKS:
        try:
            # Linkdan to'g'ri @username yoki -100... ID olish
            chat_identifier = group_link.split('/')[-1]
            if not chat_identifier.startswith('t.me/+'):
                chat_identifier = '@' + chat_identifier

            await context.bot.send_message(
                chat_id=chat_identifier,
                text=f"🧾 Yangi yo'lovchi:\n👤 Ismi: {name}\n📞 Tel: {phone}",
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"XATOLIK [BOT -> {group_link}]: {e}")
            await update.message.reply_text(f"'{group_link}' guruhiga yuborishda xatolik yuz berdi. Iltimos, admin bilan bog'laning.")
            continue
    
    await update.message.reply_text("Ma'lumotlaringiz tegishli guruhlarga yuborildi!", reply_markup=main_keyboard)
    return CHOOSING

async def cancel_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Foydalanuvchi dialogni bekor qilsa, boshlang'ich menyuga qaytaradi."""
    await update.message.reply_text("Asosiy menyuga qaytdingiz.", reply_markup=main_keyboard)
    return ConversationHandler.END

async def run_bot():
    """PTB bot qismini ishga tushuruvchi asosiy funksiya."""
    print("\n🚀 BOT QISMI ISHGA TUSHMOQDA...")
    
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_bot)],
        states={
            CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_bot_action)],
            PASSENGER_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_passenger_info)],
        },
        fallbacks=[MessageHandler(filters.Regex("^Bekor qilish$"), cancel_bot), CommandHandler('cancel', cancel_bot)],
        allow_reentry=True
    )

    application.add_handler(conv_handler)
    
    # Botni asyncio event loop'iga moslab, bloklamaydigan rejimda ishga tushirish
    try:
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        print("✅ BOT muvaffaqiyatli ishga tushdi.")
    except Exception as e:
        print(f"XATOLIK [BOT]: Botni ishga tushirishda muammo: {e}")


# ==============================================================================
# 6. ASOSIY ISHGA TUSHIRISH FUNKSIYASI
# ==============================================================================

async def main():
    """Ikkala dasturni (Spammer va Bot) bir vaqtda ishga tushiradi."""
    
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    
    print("="*50)
    print("Dastur ishga tushdi...")
    print(f"Qidirilayotgan kalit so'zlar: {KEYWORDS}")
    print("="*50)

    # Spammer va Botni bir vaqtda ishga tushirish uchun vazifalar yaratamiz
    spammer_task = asyncio.create_task(run_spammer())
    bot_task = asyncio.create_task(run_bot())

    # Ikkala vazifani parallel ravishda kutamiz
    await asyncio.gather(spammer_task, bot_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n👋 Dastur to'xtatildi.")
    except Exception as e:
        print(f"\nKUTILMAGAN UMUMIY XATOLIK: {e}")