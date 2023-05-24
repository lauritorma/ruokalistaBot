import requests
import config
from datetime import date
from datetime import datetime
from telegram.ext import Updater, CommandHandler

def ruokalista(update, context):
    response = requests.get('https://www.compass-group.fi/menuapi/feed/json?costNumber=0083&language=fi')
    data = response.json()

    menus_for_days = data['MenusForDays']
    today = date.today()
    today_formatted = today.strftime("%d.%m.%Y")
  
    for menu in menus_for_days:
        menu_date = datetime.fromisoformat(menu['Date'].split('T')[0]).date()
        if menu_date == today:
            set_menus = menu['SetMenus']
            menu_text = f"\nRuokalista Pääraide {today_formatted} 🥘\n_______________________________"
          
            for set_menu in set_menus:
                components = set_menu['Components']
                menu_text += f" {' | '.join(components)}\n\n"
          
            context.bot.send_message(chat_id=update.effective_chat.id, text=menu_text)
            return
  
    context.bot.send_message(chat_id=update.effective_chat.id, text="No menu available for today.")

updater = Updater(token=config.API_KEY, use_context=True)
dispatcher = updater.dispatcher

ruokalista_handler = CommandHandler('ruokalista', ruokalista)
dispatcher.add_handler(ruokalista_handler)

updater.start_polling()
updater.idle()
