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
import sqlite3

from sqlite3 import Error

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

def sql_connection():
    try:
        conn = sqlite3.connect('mydatabase.db', check_same_thread=False)
        return conn

    except Error:

        print(Error)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    global mylistAnswer,gameIsplay, listGamePlay,listPlayer
    """Send a message when the command /start is issued."""
    cursorObj = con.cursor()
    sql_get_group_start = 'SELECT group_id FROM group_start WHERE group_id = "'+str(update.effective_chat.id)+'"'
    cursorObj.execute(sql_get_group_start)
    check = cursorObj.fetchall()
    print(sql_get_group_start,len (check))

    if len (check) == 0 :
        cursorObj.execute("INSERT INTO group_start (group_id) VALUES('"+str(update.effective_chat.id)+"')")
        context.bot.send_message(update.effective_chat.id,"game telah terbuat, dalam 30 detik game akan dimulai")
        con.commit()
        set_timer_start(update, context)


    # if gameIsplay == False :
    #     gameIsplay = True
    #     random_image = random.choice(file_path_type)
    #     mylistAnswer.clear()
    #     mylistAnswer.append("Memenya kurang lucu")

    #     send_image_user(update, context, random_image)
    # set_timer(update, context)


def join(update, context):
    global mylistAnswer,gameIsplay, listGamePlay,listPlayer
    """Send a message when the command /start is issued."""
    cursorObj = con.cursor()
    cursorObj.execute('SELECT group_id FROM group_start WHERE group_id = "'+str(update.effective_chat.id)+'"')
    check = cursorObj.fetchall()

    if len (check) > 0 :
        cursorObj.execute('SELECT group_id,user_id FROM group_join WHERE group_id = "'+str(update.effective_chat.id)+'" and user_id = "'+str(update.effective_user.id)+'"')
        check_join = cursorObj.fetchall()
        if len (check_join) == 0 :
            cursorObj.execute("INSERT INTO group_join (group_id,user_id) VALUES('"+str(update.effective_chat.id)+"','"+str(update.effective_user.id)+"')")
            context.bot.send_message(update.effective_chat.id,"kamu telah join")
            con.commit()
    else:
        context.bot.send_message(update.effective_chat.id,"game tidak ada")

def send_image_user(update, context, random_image):
    context.bot.send_photo(update.effective_chat.id,random_image)
    context.bot.send_message(update.effective_chat.id,"tuliskan jawaban kesan kamu melihat foto ini, dan beri jawaban di bot")
    context.bot.send_photo(update.effective_user.id,random_image)
    context.bot.send_message(update.effective_user.id,"/jawab <ketik jawaban mu> atau /j <ketik jawaban mu>")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def poll(update, context, listAnswer):
    global mylistAnswer,gameIsplay
    """Sends a predefined poll"""
    questions = listAnswer
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

def remove_job_if_exists(name, context):
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def set_timer_start(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = 30
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        job_removed = remove_job_if_exists(str(chat_id)+'str', context)

        context.job_queue.run_once(do_send_to_all_user, due, context=[update,context], name=str(chat_id))

    except (IndexError, ValueError):
        update.message.reply_text('Usage: jam tidak terseteksi')

def set_timer_poll(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = 15
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        job_removed = remove_job_if_exists(str(chat_id)+'poll', context)

        context.job_queue.run_once(do_poll, due, context=[update,context], name=str(chat_id))

    except (IndexError, ValueError):
        update.message.reply_text('Usage: jam tidak terseteksi')


def set_jawab(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        chat_text = " ".join(context.args)

        cursorObj = con.cursor()
        cursorObj.execute('SELECT id FROM group_join WHERE user_id = "'+str(update.effective_user.id)+'"')
        rows_user = cursorObj.fetchone()
        if rows_user:
            cursorObj.execute('UPDATE group_join SET jawaban = "'+chat_text+'" where user_id = "'+str(update.effective_user.id)+'"')
            con.commit()
        else:
            context.bot.send_message(update.effective_user.id,"kamu tidak ada dalam game")
            pass

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set_jawab <message>')

def do_send_to_all_user(context):
    """Send the alarm message."""
    job = context.job
    # context.bot.send_message(job.context, text='Beep!')

    random_image = random.choice(file_path_type)
    cursorObj = con.cursor()

    cursorObj.execute('SELECT group_id,user_id FROM group_join WHERE group_id = "'+str(job.context[0].effective_chat.id)+'"')
    rows_join = cursorObj.fetchall()
    if len(rows_join) > 1:
        cursorObj.execute('SELECT group_id FROM group_start WHERE group_id = "'+str(job.context[0].effective_chat.id)+'"')
        rows_group = cursorObj.fetchall()
        for row in rows_group:
            context.bot.send_photo(row[0],random_image)
            context.bot.send_message(row[0],"tuliskan jawaban kesan kamu melihat foto ini, dan beri jawaban di bot, dalam 15 detik")

        for row in rows_join:
            context.bot.send_photo(row[1],random_image)
            context.bot.send_message(row[1],"/jawab <ketik jawaban mu dalam 15 detik akan di hitung> atau /j <ketik jawaban mu>")

        set_timer_poll(job.context[0],job.context[1])
    else:
        context.bot.send_message(row[0],"game diberhetikan karna kurang dari 2 pemain")
        pass


def do_poll(context):
    """Send the alarm message."""
    job = context.job
    # context.bot.send_message(job.context, text='Beep!')
    # print("hi five")
    # print(job)
    listPoll = []

    cursorObj = con.cursor()
    cursorObj.execute('SELECT jawaban FROM group_join WHERE group_id = "'+str(job.context[0].effective_chat.id)+'"')
    rows_group = cursorObj.fetchall()
    for row in rows_join:
        listPoll.append(row[0])
        
    if len(listPoll) > 1:
        poll(job.context[0],job.context[1],listPoll)
    else:
        pass

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
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("join", join))
    dp.add_handler(CommandHandler("help", help))
    # dp.add_handler(CommandHandler("poll", poll))
    # dp.add_handler(PollAnswerHandler(receive_poll_answer))
    # dp.add_handler(CommandHandler("set", set_timer))
    dp.add_handler(CommandHandler("jawab", set_jawab))
    dp.add_handler(CommandHandler("j", set_jawab))

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
    con = sql_connection()
    main()