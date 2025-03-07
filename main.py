import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Список обязательных каналов
REQUIRED_CHANNELS = ['@Channel1', '@Channel2', '@Channel3', '@Channel4', '@Channel5']

# Функция для старта
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Чтобы писать в чат, вы должны быть подписаны на все каналы: ' + ', '.join(REQUIRED_CHANNELS))

# Функция для проверки подписки и обработки сообщений
def check_subscription(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    try:
        chat_member = context.bot.get_chat_member(update.effective_chat.id, user_id)

        if chat_member.status == 'left':
            # Проверка подписок на обязательные каналы
            not_subscribed = []
            for channel in REQUIRED_CHANNELS:
                member_status = context.bot.get_chat_member(channel, user_id)
                if member_status.status == 'left':
                    not_subscribed.append(channel)

            if not_subscribed:
                update.message.delete()
                update.message.reply_text('Чтобы писать в чат, вы должны быть подписаны на все каналы: ' + ', '.join(not_subscribed))
                return

            # Если пользователь подписан на все каналы
            update.message.reply_text('Ваша заявка на подписку принята! Ваша ссылка: https://t.me/addlist/5WeB5Vtjt7AyMmIy')
        else:
            # Если пользователь уже в группе, просто проверяем подписки
            not_subscribed = []
            for channel in REQUIRED_CHANNELS:
                member_status = context.bot.get_chat_member(channel, user_id)
                if member_status.status == 'left':
                    not_subscribed.append(channel)

            if not_subscribed:
                update.message.delete()
                update.message.reply_text('Чтобы писать в чат, вы должны быть подписаны на все каналы: ' + ', '.join(not_subscribed))
                return

    except Exception as e:
        logger.error(f"Ошибка при проверке подписки: {e}")
        update.message.reply_text('Произошла ошибка при проверке подписки. Пожалуйста, попробуйте позже.')

def main() -> None:
    # Получаем токен из переменной окружения
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not TOKEN:
        logger.error("Токен не найден! Убедитесь, что вы добавили его в файл .env")
        return

    updater = Updater(TOKEN)

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Команды
    dispatcher.add_handler(CommandHandler("start", start))

    # Обработка сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_subscription))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
  
