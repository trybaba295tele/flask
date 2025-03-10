import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "8146049624:AAHhVjoT767TYipnUMyFVC0oCtR2IXqh9Ks"

# YOURLS API Configuration
YOURLS_API_URL = "http://l.digitallyfruol.in/yourls-api.php"
YOURLS_SIGNATURE = "88529f4bf9"

# Affiliate tags replacements
FLIPKART_TAG = "&affid=admitad&affExtParam1=2223887&affExtParam2=103ac4051ab838b3fb26eee00f52b37e"
SHOPSY_TAG = "&affid=inf_6e40e7e5-43b9-4037-80a2-03a2fc92d0a0&cmpid=product.share.pp&_refId=PP.5bdb9e12-cab1-4a42-b03c-c33477cef0f6.WCKG6C8Y6GZUFTYR&_appId=org.telegram.me"

def replace_affiliate_tag(url):
    pattern = r"&affid=.*"
    if "flipkart.com" in url:
        return re.sub(pattern, FLIPKART_TAG, url)
    elif "shopsy.in" in url:
        return re.sub(pattern, SHOPSY_TAG, url)
    else:
        return url

def shorten_url(long_url):
    params = {
        'signature': YOURLS_SIGNATURE,
        'action': 'shorturl',
        'format': 'json',
        'url': long_url
    }
    response = requests.get(YOURLS_API_URL, params=params).json()
    if response.get('status') == 'success':
        return response['shorturl']
    else:
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    original_url = update.message.text.strip()
    modified_url = replace_affiliate_tag(original_url)
    short_url = shorten_url(modified_url)
    
    if short_url:
        await update.message.reply_text(f"🔗 Shortened URL:\n{short_url}")
    else:
        await update.message.reply_text("Failed to shorten URL. Please check the link and try again.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("🤖 Bot is running...")
    app.run_polling()
