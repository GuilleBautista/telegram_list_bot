#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from telegram.ext import CommandHandler, Updater
from time import sleep
import sys

update_id = None

'''
You need to get the path to the bot as an argument, by default it is ""
This is if you want to run a script when your system boots
'''

path_to_bot=''

if len(sys.argv)>1:
    path_to_bot=sys.argv[1]
    print(path_to_bot)

def main():
    """Run the bot."""
    updater = Updater(open(path_to_bot+"token", "r").read(), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('add', add))

    updater.start_polling()
    updater.idle()

def getlist(chat):
    #we try to open a previous list
    try:
        return open(path_to_bot+"lists/"+str(chat), 'r+' )
    except FileNotFoundError:
        #if we dont have a list for this chat we create it empty
        file=open(path_to_bot+"lists/"+str(chat), 'w' )
        file.write("")
        file.close()
        #then we return the file
        return open(path_to_bot+"lists/"+str(chat), 'r+' )

'''adds an item to a file and returns the list string'''

def add(update, context):
    """Echo the message the user sent."""
    #global update_id
    # Request updates after the last update_id
    #for update in bot.get_updates(offset=update_id, timeout=10):
        #update_id = update.update_id + 1

    message=update.message
    chat=update.message.chat.id
    text=message.text[4:]
    #print( message.text[5:])
    output=''
    if len(text)==0:
        output = "you cannot add an empty entry to the list"

    else:
        '''Open the file and save the contents in a variable'''
        list_file=open(path_to_bot+'lists/'+str(chat), 'r')
        list_content=list_file.readlines()
        list_file.close()

        '''Add the entry to the list '''
        list_content.append(text+"\n")
    
        list_file=open(path_to_bot+'lists/'+str(chat), 'w')

        for l in list_content:
            output+=l
            #print(l)
            list_file.write(l)


        list_file.close()
        list_content = []

    '''We send the output back to the user'''
    new_list_id = update.message.reply_text(output).message_id

    print(new_list_id)

    #pin the new list
    if len(message.text[4:])>0:
        if bot.pin_chat_message(chat, new_list_id):
            print('Pinned')
        print('AAAAAAAAAAAAAAAAA')

        #save the list in an actual list
        #list_content=l_file.readlines()
        #append the new element
        #list_content.append(message.text+'\n')
            

if __name__ == '__main__':
    main()
