"""
Simple Bot to reply to Telegram messages taken from the python-telegram-bot examples.
Deployed using heroku.
Author: liuhh02 https://medium.com/@liuhh02
"""

import logging
from telegram import Poll, ParseMode, KeyboardButton, KeyboardButtonPollType, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PollAnswerHandler
import os
import listOfimage
import glob, random

file_path_type = listOfimage.listFile
PORT = int(os.environ.get('PORT', 13027))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '5193312699:AAFR2YS7nWYchZkztUDqjP-L5j0j13lIqA0'
mylistAnswer = ["Option 1"]
listGamePlay = []
listPlayer = [];
gameIsplay = False

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    global mylistAnswer,gameIsplay, listGamePlay,listPlayer
    """Send a message when the command /start is issued."""
    # index = next((i for i, item in enumerate(listGamePlay) if item.player == 'specific_id'), -1)


    # listGamePlay[update.effective_chat.id] = update.effective_user.id
    # if listGamePlay[update.effective_chat.id]:
    #     listGamePlay[update.effective_chat.id]['player'].append(update.effective_user.id)
    # else:
    #     listGamePlay[update.effective_chat.id]['play'] = False
    #     listGamePlay[update.effective_chat.id]['player'] = []
    #     listGamePlay[update.effective_chat.id]['player'].append(update.effective_user.id)

    # print(listGamePlay)
    if gameIsplay == False :
        gameIsplay = True
        random_image = random.choice(file_path_type)
        mylistAnswer.clear()
        mylistAnswer.append("Memenya kurang lucu")

        send_image_user(update, context, random_image)
        set_timer(update, context)

def send_image_user(update, context, random_image):
    context.bot.send_photo(update.effective_chat.id,random_image)
    context.bot.send_message(update.effective_chat.id,"tuliskan jawaban kesan kamu melihat foto ini, dan beri jawaban di bot")
    context.bot.send_photo(update.effective_user.id,random_image)
    context.bot.send_message(update.effective_user.id,"/jawab <ketik jawaban mu>")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def poll(update, context):
    global mylistAnswer,gameIsplay
    """Sends a predefined poll"""
    questions = mylistAnswer
    message = context.bot.send_poll(
        update.effective_chat.id,
        "Manakah yang paling lucu?",
        questions,
        is_anonymous=True
    )
    # Save some info about the poll the bot_data for later use in receive_poll_answer
    payload = {
        message.poll.id: {
            "questions": questions,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
            "answers": 0,
        }
    }
    context.bot_data.update(payload)
    gameIsplay = False

# def receive_poll_answer(update, context) :
#     """Summarize a users poll vote"""
#     answer = update.poll_answer
#     poll_id = answer.poll_id
#     try:
#         questions = context.bot_data[poll_id]["questions"]
#     # this means this poll answer update is from an old poll, we can't do our answering then
#     except KeyError:
#         return
#     selected_options = answer.option_ids
#     answer_string = ""
#     for question_id in selected_options:
#         if question_id != selected_options[-1]:
#             answer_string += questions[question_id] + " and "
#         else:
#             answer_string += questions[question_id]
#     context.bot.send_message(
#         context.bot_data[poll_id]["chat_id"],
#         f"{update.effective_user.mention_html()} feels {answer_string}!",
#         parse_mode=ParseMode.HTML,
#     )
#     context.bot_data[poll_id]["answers"] += 1
#     # Close poll after three participants voted
#     if context.bot_data[poll_id]["answers"] == 3:
#         context.bot.stop_poll(
#             context.bot_data[poll_id]["chat_id"], context.bot_data[poll_id]["message_id"]
#         )

def preview(update, context):
    """Ask user to create a poll and display a preview of it"""
    # using this without a type lets the user chooses what he wants (quiz or poll)
    button = [[KeyboardButton("Press me!", request_poll=KeyboardButtonPollType())]]
    message = "Press the button to let the bot generate a preview for your poll"
    # using one_time_keyboard to hide the keyboard
    update.effective_message.reply_text(
        message, reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True)
    )


def remove_job_if_exists(name, context):
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def set_timer(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = 10
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        job_removed = remove_job_if_exists(str(chat_id), context)


        context.job_queue.run_once(alarm, due, context=[update,context], name=str(chat_id))
        # text = ''
        # if job_removed:
        #     text += ' Old one was removed.'
        # update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def set_jawab(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        chat_text = " ".join(context.args)
        mylistAnswer.append(chat_text)
        # context.bot.send_message(chat_id,chat_text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set_jawab <message>')


def alarm(context):
    """Send the alarm message."""
    job = context.job
    # context.bot.send_message(job.context, text='Beep!')
    print("hi five")
    print(job)
    poll(job.context[0],job.context[1])

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("poll", poll))
    # dp.add_handler(PollAnswerHandler(receive_poll_answer))
    dp.add_handler(CommandHandler('preview', preview))
    dp.add_handler(CommandHandler("set", set_timer))
    dp.add_handler(CommandHandler("jawab", set_jawab))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=TOKEN)
    # updater.bot.setWebhook('https://apakahkamumeme.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()