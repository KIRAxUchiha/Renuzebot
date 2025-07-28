from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Contact,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Visible token (as requested)
BOT_TOKEN = "8437832383:AAHlvPShQagJgWFKfwT0QxALwlGKcy8gTug"
ADMIN_ID = 958975018  # Qurbonov Asilbek

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_button = [[KeyboardButton("📞 Raqamni yuborish", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(contact_button, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "👋 Assalomu alaykum!\n\n"
        "*Renuze Premium* botiga xush kelibsiz.\n"
        "Davom etish uchun telefon raqamingizni yuboring 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Handle contact
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    contact: Contact = update.message.contact
    context.user_data["phone_number"] = contact.phone_number

    # Send contact to admin
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"📥 *Yangi foydalanuvchi kontakt yubordi!*\n"
            f"👤 Ism: {contact.first_name} {contact.last_name or ''}\n"
            f"📞 Tel: {contact.phone_number}\n"
            f"🆔 ID: {user.id}\n"
            f"👤 Username: @{user.username or 'username yo‘q'}"
        ),
        parse_mode="Markdown"
    )

    # Show buy options
    buttons = [
        [InlineKeyboardButton("🛒 1 oy – 45,000 so'm", callback_data="buy_1month")],
        [InlineKeyboardButton("🛒 12 oy – 330,000 so'm", callback_data="buy_12months")],
        [InlineKeyboardButton("👨‍💼 Admin bilan bog‘lanish", url="https://t.me/RENUZE")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        "✅ Raqamingiz qabul qilindi!\n\n"
        "Quyidagi tugmalardan birini tanlab Telegram Premium xarid qiling 👇",
        reply_markup=keyboard
    )

# Handle button callbacks
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy_1month":
        text = (
            "🛒 *1 oylik Telegram Premium*\n"
            "💳 Narxi: 45,000 so'm\n\n"
            "To‘lovni ushbu karta raqamiga amalga oshiring:\n"
            "`9860 1966 0153 6598`\n"
            "👤 Qurbonov Asilbek\n\n"
            "✅ To‘lovdan so‘ng chekingizni shu yerga yuboring.\n"
            "Admin: @RENUZE"
        )
        await query.edit_message_text(text, parse_mode="Markdown")

    elif query.data == "buy_12months":
        text = (
            "🛒 *12 oylik Telegram Premium*\n"
            "💳 Narxi: 330,000 so'm\n\n"
            "To‘lovni ushbu karta raqamiga amalga oshiring:\n"
            "`9860 1966 0153 6598`\n"
            "👤 Qurbonov Asilbek\n\n"
            "✅ To‘lovdan so‘ng chekingizni shu yerga yuboring.\n"
            "Admin: @RENUZE"
        )
        await query.edit_message_text(text, parse_mode="Markdown")

# Handle payment screenshot
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    phone_number = context.user_data.get("phone_number", "raqam yuborilmagan")
    photo = update.message.photo[-1].file_id

    caption = (
        f"📥 *Yangi to‘lov cheki!*\n"
        f"👤 Foydalanuvchi: @{user.username or 'username yo‘q'}\n"
        f"🆔 ID: {user.id}\n"
        f"📞 Tel: {phone_number}\n\n"
        f"📎 Quyida chek:"
    )

    await context.bot.send_photo(chat_id=ADMIN_ID, photo=photo, caption=caption, parse_mode="Markdown")
    await update.message.reply_text("✅ Chekingiz yuborildi. Tez orada admin siz bilan bog‘lanadi.")

# Launch bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    import logging
    logging.basicConfig(level=logging.INFO)
    logging.info("Bot is running...")
    
    app.run_polling()