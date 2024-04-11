import logging
import json
import random
from telegram import Update , InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, filters

with open('rockets.json') as rfp:
    rockets_count = int(json.load(rfp))
tokenfp = open('token.json','r')
token = json.load(tokenfp)
tokenfp.close()

# TODO:
# Major - rewrite on AioGRAM
# - add todolist
# - interface: LLM to specify commands; add questions to specify is commands correct
# - distribute message to group of people
# - monitoring 
# - set name assotiations to user
# - notification
# - happybirthday test
# - saving sketches (verify by user id to not junk up harddrive)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def dice_roll(number:int, amount:int =None):
    if amount is None:
        return [random.randint(1,number)]
    for i in range(1, amount):
        return [random.randint(1,number) for i in range(amount)]
#------------#

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Howdy, I'm your assistant bot. Currently I'm capable of... nothing. You can roll a dice or get your user_id and user_name")

async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Pee-pee poo-poo, imma stoopid bot")

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=str(update.message.from_user.first_name)+" "+str(update.message.from_user.id))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=str(update.effective_chat))

#------------#

async def echo(update: Update, context):
    user_says = " ".join(context.args)
    await context.bot.send_message(chat_id=update.effective_chat.id, text= "You said: "+user_says)

async def dice(update: Update, context):
    if len(context.args) == 0 :
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You forgor to add number \n Command example: '''/dice 20'''")
    else:
        dice = int(context.args[0])
        result =  random.randint(1, dice)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You rolled: "+str(result))

async def todo_show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == 737928817:
        global application
        # json.dump(rockets_count, rfp)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Adios B-|")
        # rfp.close()
        application.stop_running()
        await application.stop()
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="How about u?")

async def rockets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global rockets_count
    rockets_count= rockets_count + 1
    json.dump(rockets_count, rfp)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="You've sent "+str(rockets_count)+" rockets to Afrika")

async def dice_select( update: Update, context: ContextTypes.DEFAULT_TYPE):
    list_test = ['Dice 20', 'Dice 12', 'Dice 10', 'Dice 6', 'Dice 4']
    if len(context.args) != 0:
        print(context.args)
        if context.args[0].isdigit():
            dice_result = dice_roll(int(context.args[0]), (int(context.args[1]) if (len(context.args) == 2) else None))
            print(str(dice_result))
            drs = ' '.join(str(d) for d in dice_result)
            avg = 0
            sum = 0
            for d in dice_result:
                sum+=d
                avg+=d
            avg = avg/dice_result.__len__()
            await context.bot.send_message(chat_id=update.effective_chat.id , text=f"You rolled {drs} on {context.args[0]}\nAvarage: {avg}\nSum: {sum}", reply_to_message_id=update.effective_message.id)
            return
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="You shall send number, not somewhat junk гwг \nCommand example: '''/dice 20'''")
            return
    button_list =[]
    for each in list_test:
        button_list.append([InlineKeyboardButton(text=each, callback_data=each)])
    reply_markup=InlineKeyboardMarkup(button_list)

    await context.bot.send_message(text="Choose dice to roll", chat_id=update.effective_chat.id, reply_markup=reply_markup)

async def keyboard_callback( update:Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    print('query.data: ', query.data)
    print(query.data[0:4])
    reply_text= str()
    if query.data[0:4] == 'Dice':
        dr = dice_roll(int(query.data[5:]))
        drs = ' '.join(str(d) for d in dr)
        reply_text=f'@{query.from_user.username }, you rolled: {drs} on {int(query.data[5:])}'
    else:
        reply_text='Pee-pee poo-poo, imma stooopid, tell my creator to fix me ,w,'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)
    await query.answer(text=reply_text)

async def whostoopid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    print("Blep")
    print(update.message.chat.type)
    if msg == "Who is stoopid":
        if update.message.from_user.id == 737928817:
            await context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.effective_message.id, text="Imma stoopid .w.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.effective_message.id, text="YOU BOZO ^w^")


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    about_handler = CommandHandler('about', about_cmd)
    whoami_handler = CommandHandler('whoami', whoami)
    echo_handler = CommandHandler('echo', echo)
    dice_handler= CommandHandler('dice', dice_select)
    rocket_handler = CommandHandler('rocket', rockets)
    kill_handler = CommandHandler('kys', kill)
   # button_handler = CommandHandler('button_test', dice_select)
    
    stoopid_handler = MessageHandler(filters= filters.TEXT & (~filters.COMMAND),callback= whostoopid)

    application.add_handler(start_handler)
    application.add_handler(about_handler)
    application.add_handler(whoami_handler)
    application.add_handler(echo_handler)
    application.add_handler(dice_handler)
    application.add_handler(rocket_handler)
    application.add_handler(kill_handler)
    application.add_handler(stoopid_handler)
    application.add_handler(CallbackQueryHandler(keyboard_callback))

    application.run_polling()
