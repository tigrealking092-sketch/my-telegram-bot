import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

ADMIN_CHAT_ID = "7705333185"

# /start နှိပ်လိုက်ရင် ပေါ်လာမယ့် ပင်မမီနူး
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💎 Diamond ဈေးနှုန်းများ", callback_data="prices")],
        [InlineKeyboardButton("💳 ငွေလွှဲရန် အချက်အလက်", callback_data="payment")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎮💎 LEON_Diamond_Top-up Shop မှကြိုဆိုပါတယ်ဗျ\nအောက်ပါ မီနူးမှ လိုချင်တာကို ရွေးချယ်ပါ။",
        reply_markup=reply_markup
    )

# ခလုတ်နှိပ်သည့်အခါ လုပ်ဆောင်ချက်များ
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "prices":
        keyboard = [
            [InlineKeyboardButton("🔙 မီနူးသို့ ပြန်သွားရန်", callback_data="back_home")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = (
            "💎 **Diamond ဈေးနှုန်းစာရင်း** 💎\n\n"
            "• 11 💎 - 1000 ks\n"
            "• Weekly Pass - 7000 ks\n\n"
            "ဝယ်ယူလိုပါက **Game ID** နှင့် ငွေလွှဲပြေစာပုံ ပို့ပေးပါ။"
        )
        await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")
        
    elif data == "payment":
        keyboard = [
            [InlineKeyboardButton("🔙 မီနူးသို့ ပြန်သွားရန်", callback_data="back_home")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = (
            "💳 **ငွေလွှဲရန် အချက်အလက်** 💳\n\n"
            "(လောလောဆယ် AYA Pay နဲ့ UAB Pay သာ ရသေးပါသည်)\n\n"
            "• AYA Pay / UAB Pay\n"
            "• ဖုန်းနံပါတ်: `09697476259`\n"
            "• Pay Name: **SWE HAN**\n\n"
            "ငွေလွှဲပြီးပါက ငွေလွှဲပြေစာပုံနှင့် Game ID ပို့ပေးပါ။"
        )
        await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")
        
    elif data == "back_home":
        keyboard = [
            [InlineKeyboardButton("💎 Diamond ဈေးနှုန်းများ", callback_data="prices")],
            [InlineKeyboardButton("💳 ငွေလွှဲရန် အချက်အလက်", callback_data="payment")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = "ပင်မမီနူးသို့ ပြန်ရောက်ပါပြီ။ လိုချင်တာကို ထပ်မံရွေးချယ်ပါ။"
        await query.edit_message_text(text=text, reply_markup=reply_markup)
        
    # Admin က "✅ ဖြည့်ပြီးပါပြီ" ခလုတ်ကို နှိပ်လိုက်ရင်
    elif data.startswith("done_"):
        customer_id = data.split("_")[1]
        try:
            await context.bot.send_message(
                chat_id=customer_id,
                text="🎉 သင့်ရဲ့ Diamond များကို ဖြည့်သွင်းပေးပြီးပါပြီခင်ဗျ။ ယုံကြည်စိတ်ချစွာ အသုံးပြုသည့်အတွက် ကျေးဇူးတင်ပါတယ်။ 🙏"
            )
            await query.edit_message_caption(
                caption=query.message.caption + "\n\n✅ **[အခြေအနေ: ဖြည့်ပြီးပါပြီ]**",
                parse_mode="Markdown"
            )
        except Exception as e:
            await query.answer(text="ဖောက်သည်ဆီ စာပို့၍ မရပါ။", show_alert=True)

# ဖောက်သည်ဆီက စာသား သို့မဟုတ် ပုံ (သို့) ပုံနှင့်စာတွဲလျက် ပို့လာခြင်းကို လက်ခံရန်
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # ဖောက်သည်မှာ Username ရှိမရှိ စစ်ဆေးရန် (မရှိရင် "မရှိပါ" လို့ ပြမယ်)
    username_str = f"@{user.username}" if user.username else "Username မရှိပါ"
    
    # 1. ဖောက်သည်က ပုံ (ငွေလွှဲပြေစာ) နဲ့ Game ID (Caption) ကို တစ်ခါတည်း တွဲပို့လိုက်ရင်
    if update.message.photo:
        await update.message.reply_text("ငွေလွှဲပြေစာပုံနှင့် Game ID ကို လက်ခံရရှိပါပြီခင်ဗျ။ စစ်ဆေးပြီး ချက်ချင်း ဖြည့်သွင်းပေးပါမည်။")
        
        customer_caption = update.message.caption if update.message.caption else "စာသားမပါပါ"
        
        caption = (
            f"💰 ငွေလွှဲပြေစာ နှင့် အချက်အလက်အသစ်!\n"
            f"👤 ပို့သူ: {user.first_name}\n"
            f"🔗 Username: {username_str}\n"
            f"🆔 User ID: {user.id}\n"
            f"💬 Game ID / အချက်အလက်: {customer_caption}"
        )
        photo_file_id = update.message.photo[-1].file_id
        
        keyboard = [
            [InlineKeyboardButton("✅ ဖြည့်ပြီးပါပြီ (ဖောက်သည်ဆီ အကြောင်းကြားရန်)", callback_data=f"done_{user.id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_photo(
            chat_id=ADMIN_CHAT_ID, 
            photo=photo_file_id, 
            caption=caption, 
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    # 2. ဖောက်သည်က စာသား (Game ID သို့မဟုတ် အခြားစာများ) သက်သက် ပို့လာရင်
    elif update.message.text:
        user_message = update.message.text
        await update.message.reply_text("သင့်ရဲ့ Game ID နဲ့ အချက်အလက်များကို လက်ခံရရှိပါပြီ။ ငွေလွှဲပြေစာပုံ ပို့ပေးပါခင်ဗျ။")
        
        alert_text = (
            f"🚨 ဖောက်သည်ထံမှ စာရောက်ပါပြီ!\n"
            f"👤 အမည်: {user.first_name}\n"
            f"🔗 Username: {username_str}\n"
            f"🆔 User ID: {user.id}\n"
            f"💬 စာသား: {user_message}"
        )
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=alert_text, parse_mode="Markdown")

if __name__ == '__main__':
    TOKEN = "9179780665:AAGi5v6QlCPtmBUw7SrbxNYcglnzYhqjA-c"
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler((filters.TEXT | filters.PHOTO) & (~filters.COMMAND), handle_message))
    
    print("Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    application.run_polling()
  
