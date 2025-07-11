import json
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

with open('config.json') as f:
    config = json.load(f)

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users[user_id] = {
        'start_time': datetime.now(),
        'referred_by': None,
        'referrals': []
    }
    keyboard = [
        [InlineKeyboardButton("💰 Stake", callback_data='stake')],
        [InlineKeyboardButton("📈 Balance", callback_data='balance')],
        [InlineKeyboardButton("👥 Refer", callback_data='refer')]
    ]
    await update.message.reply_text(
        "🌟 Welcome to Mintarc BTC Staking!\n\n🚀 Launching Staking Engine...\n⏳ Duration: 7 Days\n💰 Reward: 3x with referrals!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == 'stake':
        await query.edit_message_text(f"💵 Send minimum ${config['min_amount_usd']} BTC to:\n{config['wallet_address']}")
    elif query.data == 'balance':
        if user_id not in users:
            await query.edit_message_text("⚠️ You haven't started staking yet. Use /start")
            return
        start_time = users[user_id]['start_time']
        end_time = start_time + timedelta(days=config['countdown_days'])
        remaining = end_time - datetime.now()
        reward = config['reward_multiplier'] * config['min_amount_usd']
        await query.edit_message_text(
            f"⏳ Time Left: {remaining.days}d {remaining.seconds//3600}h {(remaining.seconds//60)%60}m\n💰 Estimated Reward: ${reward}"
        )
    elif query.data == 'refer':
        link = f"https://t.me/{context.bot.username}?start={user_id}"
        await query.edit_message_text(f"👥 Invite your friends!\nYour link: {link}")

# Run bot
BOT_TOKEN = "8092582657:AAEw5v4nre2g3_egYtE5k5ElAdPxU2OOMqc"

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("🚀 Bot is running...")
app.run_polling()
