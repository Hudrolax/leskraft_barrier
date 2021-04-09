import logging
from utility.logger_super import LoggerSuper
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

class Telegram_bot(LoggerSuper):
    logger = logging.getLogger('telebot')
    def __init__(self, token, barrier):
        self.logger.info('Запускаем телеграм бота')
        self.barrier = barrier
        self.updater = Updater(token)
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.button))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.get_text_message))

        # Start the Bot
        self.updater.start_polling()

    def get_text_message(update: Update, _: CallbackContext):
        keyboard = [
            [
                InlineKeyboardButton("Open", callback_data='open'),
                InlineKeyboardButton("Close", callback_data='close'),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Please choose:', reply_markup=reply_markup)

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
        self.logger.info(f'Получил команду "{query.data}"')
        answer = 'неизвестная команда'
        if query.data == 'open':
            answer = self.barrier.open()
        elif query.data == 'close':
            answer = self.barrier.close()

        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query.answer()

        query.edit_message_text(text=answer)