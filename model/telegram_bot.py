import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

class Telegram_bot:
    def __init__(self, token):
        updater = Updater(token)
        updater.dispatcher.add_handler(CommandHandler('start', self.start))
        updater.dispatcher.add_handler(CallbackQueryHandler(self.button))

        # Start the Bot
        updater.start_polling()


    def start(self, update: Update, _: CallbackContext) -> None:
        keyboard = [
            [
                InlineKeyboardButton("Open", callback_data='open'),
                InlineKeyboardButton("Close", callback_data='close'),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Please choose:', reply_markup=reply_markup)

    def button(self, update: Update, _: CallbackContext):
        query = update.callback_query

        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query.answer()

        query.edit_message_text(text=f"Selected option: {query.data}")

if __name__ == '__main__':
    bot = Telegram_bot("1720229809:AAFY0SD55xQQR_p-pUdfwvzK2SxD4TsMhWo")
    print('ggg')