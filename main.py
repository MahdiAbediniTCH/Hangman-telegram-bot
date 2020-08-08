from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, RegexHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode


def character_button(char):
    return InlineKeyboardButton(char, callback_data = char)

REPLIES = {'welcome': "به ربات بازی Hangman خوش اومدین.", 
          'language': "زبان بازی را انتخاب کنید",
          'farsi': "کلمه میخوای یا ضرب المثل",
          'invalid_answer': "لطفا از گزینه های داده شده انتخاب کنید",
          'game': "بازیکن: %s \n\
نوع بازی: %s \n\
",
           
          }

FILES = {'english': "wordset/english.txt",
         'farsi': "wordset/farsi.txt",
         'zarbolmasal': "wordset/zarbolmasal.txt",
        }

CHARACTERS = {'english': [
          [character_button('a'), character_button('b'), character_button('c'), character_button('d'), character_button('e'), character_button('f'), character_button('g'), character_button('h'), character_button('i'), character_button('j')],
          [character_button('k'), character_button('l'), character_button('m'), character_button('n'), character_button('o'), character_button('p'), character_button('q'), character_button('r'), character_button('s')],
          

TOKEN = "token"

def start(bot, update):
    keyboard = [['English', 'فارسی']]
    update.message.reply_text(REPLIES['welcome'])
    update.message.reply_text(REPLIES['language'], reply_markup=ReplyKeyboardMarkup(keyboard))
    return 'language'

def start_game(bot, update, wordset):
    file = open(FILES[wordset])
    lines = file.readlines()
    word = lines[randint(0, len(lines) - 1)][:-1]
    update.message.reply_text(REPLIES['game'] % ("folan", "folan"))

def select_language(bot, update):
    language = update.message.text
    if language == 'English':
        startgame(bot, update, 'english')
        return ConversationHandler.END
    else:
        keyboard = [['ضرب المثل', 'کلمه']]
        update.message.reply_text(REPLIES['farsi'], reply_markup=ReplyKeyboardMarkup(keyboard))
        return 'farsi'

def select_farsi(bot, update):
    farsi = update.message.text

def invalid_answer_language(bot, update):
    update.message.reply_text(REPLIES['invalid_answer_language'])
    return 'language'

def invalid_answer_farsi(bot, update):
    update.message.reply_text(REPLIES['invalid_answer'])
    return 'farsi'

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            "language" : [RegexHandler('^(English|فارسی)$', select_language),
                          MessageHandler(Filters.all, invalid_answer_language)
                          ],
            "farsi" : [RegexHandler('^(ضرب المثل|کلمه)$', select_farsi),
                       MessageHandler(Filters.all, invalid_answer_farsi)
                       ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    ))


if __name__ == '__main__':
    main()
