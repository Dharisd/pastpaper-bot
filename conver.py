#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from pp_db import *
import urllib.parse

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

# Enable logging
logging.basicConfig(filename="logfile2.log",format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

START, UNIT, YEAR, SESSION, SENDFILE = range(5)




def split(arr, size):
     arrs = []
     while len(arr) > size:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
     arrs.append(arr)
     return arrs

#used to generate names for files
def genName(filenameArray,subject):
    name = subject +" "
    name += " ".join(str(x) for x in filenameArray)
    return name

def start(update, context):
    user = update.message.from_user
    subjects = getSubjects()
    reply_keyboard =  split(subjects,3)


    update.message.reply_text(
        'Hi! im pastpaper bot .\n' 
        'what subject are you looking for?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return UNIT


def unit(update, context):
    user = update.message.from_user
    context.user_data["subject"] = update.message.text
    units = getUnits(update.message.text)
    print(units,update.message.text)
    reply_keyboard = split(units,3)
    update.message.reply_text('I see! What unit are you looking for?',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return YEAR


def year(update, context):
    context.user_data["unit"] = update.message.text
    user = update.message.from_user
    
    years = getYears(context.user_data["subject"],context.user_data["unit"])

    #only try to send years if  the years list isnt empty
    if len(years) > 0:
        reply_keyboard = split(years,3)
        update.message.reply_text('What year are you looking for?',
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return SESSION
    else:
        #no pappers found for this unit
        update.message.reply_text('Sorry, No papers were found for this unit.\nTry again with a /start')
        return ConversationHandler.END



def session(update, context):
    context.user_data["year"] = update.message.text
    user = update.message.from_user
    
    session = getSessions(context.user_data["subject"],context.user_data["year"],context.user_data["unit"])


    print(session)

    reply_keyboard = [session]
    update.message.reply_text('What session are you looking for?',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SENDFILE


def sendFile(update, context):
    context.user_data["session"] = update.message.text
    user = update.message.from_user

    file_data = getFile(context.user_data["subject"],context.user_data["year"],context.user_data["session"],context.user_data["unit"])
    logger.info("%s %s %s %s %s",context.user_data["subject"],context.user_data["year"],context.user_data["session"],context.user_data["unit"],user.first_name) 


    for x in file_data:
        #link = urllib.parse.quote(x["url"])[10:] # this is very inefficient
        subject = x["subject"]
        filenameArray = x["filename"]
        #file_type = x["type"]

        file_name = genName(filenameArray,subject)
        file_dir = "files/" + file_name
        print(file_dir)

        context.bot.send_document(chat_id=update.message.chat_id, document=open(file_dir,"rb"))


        print(x["url"])


    update.message.reply_text('Thank You! If you want get more pastpapers send a /start.')



    return ConversationHandler.END




def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("INSERT YOUR API key", use_context=True)




    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            START: [MessageHandler(Filters.text, start)],

            UNIT: [MessageHandler(Filters.text, unit)],

            YEAR: [MessageHandler(Filters.text, year)], #use regex for year

            SESSION: [MessageHandler(Filters.text, session)],

            SENDFILE: [MessageHandler(Filters.text, sendFile)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
