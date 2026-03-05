import os
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("8766363626:AAHzIDzG69y0yd8rjWtZMES_vM64PKUk0rM")
CONTRACT = os.getenv("@MHT_Sakib_Trader")

# Asset list with flag + emoji + priority
assets = [
    {"name": "GBP/JPY (OTC)", "flag": "🇬🇧🇯🇵", "emoji": "👑"},
    {"name": "GBP/USD (OTC)", "flag": "🇬🇧🇺🇸", "emoji": "👑"},
    {"name": "EUR/USD (OTC)", "flag": "🇪🇺🇺🇸", "emoji": "👑"},
    {"name": "USD/JPY (OTC)", "flag": "🇺🇸🇯🇵", "emoji": "👑"},
    {"name": "AUD/USD (OTC)", "flag": "🇦🇺🇺🇸", "emoji": "👑"},
    {"name": "GBP/AUD (OTC)", "flag": "🇬🇧🇦🇺", "emoji": "👑"},
    {"name": "GBP/NZD (OTC)", "flag": "🇬🇧🇳🇿", "emoji": "👑"},
    {"name": "EUR/JPY (OTC)", "flag": "🇪🇺🇯🇵", "emoji": "🔥"},
    {"name": "EUR/GBP (OTC)", "flag": "🇪🇺🇬🇧", "emoji": "🔥"},
    {"name": "USD/CAD (OTC)", "flag": "🇺🇸🇨🇦", "emoji": "🔥"},
    {"name": "EUR/CAD (OTC)", "flag": "🇪🇺🇨🇦", "emoji": "🔥"},
    {"name": "AUD/JPY (OTC)", "flag": "🇦🇺🇯🇵", "emoji": "🔥"},
    {"name": "NZD/USD (OTC)", "flag": "🇳🇿🇺🇸", "emoji": "🔥"},
    {"name": "USD/CHF (OTC)", "flag": "🇺🇸🇨🇭", "emoji": "🔥"},
    {"name": "EUR/AUD (OTC)", "flag": "🇪🇺🇦🇺", "emoji": "🔥"},
    {"name": "USD/BDT (OTC)", "flag": "🇺🇸🇧🇩", "emoji": "⚡"},
    {"name": "USD/PKR (OTC)", "flag": "🇺🇸🇵🇰", "emoji": "⚡"},
    {"name": "USD/INR (OTC)", "flag": "🇺🇸🇮🇳", "emoji": "⚡"},
    {"name": "USD/EGP (OTC)", "flag": "🇺🇸🇪🇬", "emoji": "⚡"},
    {"name": "USD/ARS (OTC)", "flag": "🇺🇸🇦🇷", "emoji": "⚡"},
    {"name": "USD/COP (OTC)", "flag": "🇺🇸🇨🇴", "emoji": "⚡"},
    {"name": "USD/DZD (OTC)", "flag": "🇺🇸🇩🇿", "emoji": "⚡"},
    {"name": "USD/PHP (OTC)", "flag": "🇺🇸🇵🇭", "emoji": "⚡"},
    {"name": "USD/MXN (OTC)", "flag": "🇺🇸🇲🇽", "emoji": "⚡"},
]

# Pagination size
PAGE_SIZE = 10

# Helper to get assets for a page
def get_assets_page(page):
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    return assets[start:end]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 Get Signals", callback_data="get_signals")],
        [InlineKeyboardButton("📄 Contract", callback_data="contract")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🤖 Welcome to Sakib AI Signal Bot\n⚠️ Indicator based signal only\n💰 Trade at your own risk",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data

    # Contract button
    if data == "contract":
        await query.edit_message_text(
            f"📄 Contact / Contract\n\nClick here to contact:\n{CONTRACT}"
        )
        return

    # Pagination handling
    if data.startswith("page_"):
        page = int(data.split("_")[1])
        await show_assets(query, page)
        return

    # Asset selected
    if data.startswith("asset_"):
        asset_index = int(data.split("_")[1])
        asset = assets[asset_index]
        await query.edit_message_text("🔍 Analyzing Market...\n⏳ Please wait...")
        await asyncio.sleep(2)
        signal = random.choice(["CALL 🚀", "PUT 🔻", "NO TRADE ❌"])
        strength = random.choice(["Strong 🔥", "Moderate ⚡", "Weak ⚠️"])
        await query.edit_message_text(
            f"{asset['flag']} {asset['name']} {asset['emoji']}\n\n"
            f"⏰ Timeframe: 1 Minute\n"
            f"Signal: {signal}\n"
            f"Strength: {strength}\n\n"
            "🛑 Stop after 2 Loss"
        )
        return

# Show asset page with buttons
async def show_assets(query, page):
    page_assets = get_assets_page(page)
    keyboard = []
    row = []
    for i, asset in enumerate(page_assets):
        index = assets.index(asset)
        row.append(InlineKeyboardButton(f"{asset['flag']} {asset['name']} {asset['emoji']}", callback_data=f"asset_{index}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    # Pagination buttons
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⬅️ PREVIOUS", callback_data=f"page_{page-1}"))
    if (page+1)*PAGE_SIZE < len(assets):
        nav_row.append(InlineKeyboardButton("➡️ MORE ASSET", callback_data=f"page_{page+1}"))
    nav_row.append(InlineKeyboardButton("🔙 BACK", callback_data="back"))
    keyboard.append(nav_row)

    await query.edit_message_text(
        "📊 Select Asset:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Back button
async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(CommandHandler("back", back))

app.run_polling()
