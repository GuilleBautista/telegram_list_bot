#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages.
This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from telegram.ext import CommandHandler, Updater
from time import sleep


update_id = None

def getlist(chat):
    #we try to open a previous list
    try:
        return open("lists/"+str(chat), 'r+' )
    except FileNotFoundError:
        #if we dont have a list for this chat we create it empty
        file=open("lists/"+str(chat), 'w' )
        file.write("")
        file.close()
        #then we return the file
        return open("lists/"+str(chat), 'r+' )

def start(update, context):
    chat_id=update.message.chat.id

    f = open("lists/"+str(chat_id), 'w')
    f.close()

'''adds an item to a file and returns the list string'''
def additem(l_file, text):
    #write the new list in the file
    lines=l_file.readlines()

    lines.append(text+"\n")
    print(lines)
    l_file.writelines(lines)

    #create a message to send
    '''send=''
    for i in l_file.readlines():
        send+=i'''
    
    return l_file.read()

def echo(update, context):
    message=update.message
    chat=update.message.chat.id

    #print( message.text[5:])
    if len(message.text[4:])==0:
        update.message.reply_text("to view the list use /show").message_id

    else:
        output=additem(getlist(chat), message.text[4:])
        print(output)
        #send list content back
        new_list_id = update.message.reply_text(output).message_id
        #pint the new list
        bot.pin_chat_message(chat, new_list_id)

        #save the list in an actual list
        #list_content=l_file.readlines()
        #append the new element
        #list_content.append(message.text+'\n')
            

def main():
    """Run the bot."""
    updater = Updater(open("token", "r").read(), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('add', echo))

    print('started succesfully')
    updater.start_polling()
    updater.idle()




if __name__ == '__main__':
    main()
