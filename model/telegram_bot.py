import logging
from utility.logger_super import LoggerSuper
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

class Telegram_bot(LoggerSuper):
    logger = logging.getLogger('telebot')
    def __init__(self, token, barrier, admins):
        self.admins = admins.split(',')
        for admin in self.admins:
            admin = admin.replace(' ', '')
        self.barrier = barrier
        self.updater = Updater(token)
        self.updater.dispatcher.add_handler(CommandHandler('start', self._proc))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.button))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self._proc))

        # Start the Bot
        self.updater.start_polling()
        self.logger.info(f'Запустил телеграм бота. Админы {self.admins}')

    def _proc(self, update: Update, _: CallbackContext):
        if update.message.from_user.id in self.admins:
            keyboard = [
                [
                    InlineKeyboardButton("Open", callback_data='open'),
                    InlineKeyboardButton("Close", callback_data='close'),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Please choose:', reply_markup=reply_markup)
        else:
            update.message.reply_text(f'Кто ты чудовище? Твой ID {update.message.from_user.id}')

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