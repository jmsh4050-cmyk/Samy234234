import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator

# أمر البداية /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك! أرسل لي أي نص وسأقوم بترجمته تلقائياً إلى العربية.\n"
        "للترجمة إلى اللغات الأخرى، أرسل النص مع رمز اللغة (مثال: /tr en مرحبا)"
    )

# ترجمة الرسائل العادية تلقائياً إلى العربية
async def translate_auto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_to_translate = update.message.text
    try:
        translated = GoogleTranslator(source='auto', target='ar').translate(text_to_translate)
        await update.message.reply_text(translated)
    except Exception as e:
        await update.message.reply_text("حدث خطأ أثناء الترجمة، يرجى المحاولة لاحقاً.")

# أمر ترجمة مخصص /tr [language_code] [text]
async def translate_custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("طريقة الاستخدام: /tr [رمز_اللغة] [النص]\nمثال: /tr en مرحبا")
        return
    
    target_lang = context.args[0]
    text_to_translate = " ".join(context.args[1:])
    
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text_to_translate)
        await update.message.reply_text(translated)
    except Exception as e:
        await update.message.reply_text(f"خطأ: تأكد من رمز اللغة المكتوب ({target_lang}).")

if __name__ == '__main__':
    # التوكن المدمج للبوت
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7924093069:AAGjjy7SomYnfUWSWu1xGY337aIYzT42tCA")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tr", translate_custom))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), translate_auto))

    print("البوت يعمل الآن...")
    app.run_polling()
  
