# -*- coding: utf-8 -*-
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

# Глобальная переменная для отслеживания состояния
bot_state = None
AWAITING_MESSAGE = 1

def load_questions():
    with open('questions.json', 'r', encoding='utf-8') as file:
        return json.load(file)

questions = load_questions()

def restart(update, context):
    update.message.reply_text("Перезапуск бота...")
    start(update, context)
    
def start(update, context, is_callback=False):
    chat_id = update.effective_chat.id if is_callback else update.message.chat_id
    first_question = questions[0]
    keyboard = [[InlineKeyboardButton(option, callback_data=option)] for option in first_question['options']]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=chat_id, text=first_question['question'], reply_markup=reply_markup)
    



def button(update, context):
    global bot_state
    query = update.callback_query
    query.answer()
    selected_option = query.data

    # Обработка нажатия кнопки "Перезапустить"
    if selected_option == 'restart':
        return start(update, context, is_callback=True)
    
    # Обработка "Да, отправляю"
    if selected_option == "Да, отправляю":
        query.edit_message_text("Пожалуйста, напишите всю информацию в сообщении")
        bot_state = AWAITING_MESSAGE
        return  # Возвращаемся без изменения состояния в ConversationHandler
    if selected_option == "Да.":
        query.edit_message_text("Пожалуйста, напишите ваш ник TG для связи")
        bot_state = AWAITING_MESSAGE
        return  # Возвращаемся без изменения состояния в ConversationHandler
 
    # Определяем следующий шаг на основе выбранного ответа
    next_step = None
    for question in questions:
        if 'next' in question and selected_option in question['next']:
            next_step = question['next'][selected_option]
            break

    # Если следующий шаг - это ID вопроса
    if isinstance(next_step, int):
        next_question = next((q for q in questions if q.get('id') == next_step), None)
        if next_question and 'options' in next_question:
            keyboard = [[InlineKeyboardButton(option, callback_data=option)] for option in next_question['options']]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(text=next_question['question'], reply_markup=reply_markup)
        elif next_question and 'response' in next_question:
            keyboard = [[InlineKeyboardButton("Перезапустить", callback_data='restart')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(text=next_question['response'], reply_markup=reply_markup)
        else:
            query.edit_message_text("Ошибка: вопрос или ответ не найден.")
    # Если следующий шаг - это прямой ответ
    elif isinstance(next_step, str):
        keyboard = [[InlineKeyboardButton("Перезапустить", callback_data='restart')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text=next_step, reply_markup=reply_markup)
    else:
        query.edit_message_text("Ошибка: ответ не найден.")

def handle_text_message(update, context):
    global bot_state
    
        # Создаем клавиатуру для перезапуска
    keyboard = [[InlineKeyboardButton("Перезапустить", callback_data='restart')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    
    if bot_state == AWAITING_MESSAGE:
        # Обработка текстового сообщения
        received_text = update.message.text
        chat_id = update.message.chat_id
        
        # Здесь вы можете обработать полученное сообщение или сохранить его
        # Например, отправляем текст определенному пользователю
        target_chat_id = 'ВВЕДИТЕ_ВАШ_ИД_ЧАТА_СЮДА'  # Замените на реальный ID чата
        context.bot.send_message(chat_id=target_chat_id, text=received_text)

        update.message.reply_text("Спасибо, ваше сообщение получено!", reply_markup=reply_markup)
        bot_state = None  # Сброс состояния
    else:
        # Обработка обычных текстовых сообщений
        update.message.reply_text("К сожалению, я не знаю, что Вам ответить :(", reply_markup=reply_markup) 

def main():
    global bot_state
    updater = Updater("ВВЕДИТЕ_ВАШ_ТОКЕН_СЮДА")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text, handle_text_message))

    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()