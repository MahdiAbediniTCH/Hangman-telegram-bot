
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, RegexHandler, CallbackQueryHanler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from random import randint

class HangMan:
    def __init__(self, wordset, word, n_tries, word_guessed):
	self.wordset = wordset
	self.word = word
	self.n_tries = n_tries
	self.word_guessed = word_guessed
	self.letters_guessed = list()
    def new_guess(self, char):
	if char in self.letters_guessed:
	    return False
	self.letters_guessed.append(char)
	return True
def character_button(char):
    return InlineKeyboardButton(char, callback_data=char)

HANGMANPICS = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

REPLIES = {'welcome': "به ربات بازی Hangman خوش اومدین.", 
          'language': "زبان بازی را انتخاب کنید",
          'farsi': "کلمه میخوای یا ضرب المثل",
          'invalid_answer': "لطفا از گزینه های داده شده انتخاب کنید",
          'game': """بازیکن: %s
          نوع بازی: %s 
تعداد حدس باقیمانده: %d

%s

%s
""",
           
          }

FILES = {'english': "wordset/english.txt",
         'persian': "wordset/persian.txt",
         'proverb': "wordset/persian_proverbs.txt",
        }

GAMEMODES = {'english': "انگلیسی - کلمه",
             'persian': "فارسی - کلمه",
             'proverb': "فارسی - ضرب المثل",
            }

CHARACTERS = {'english': [
            [character_button('a'), character_button('b'), character_button('c'), character_button('d'), character_button('e'), character_button('f'), character_button('g'), character_button('h')],
            [character_button('i'), character_button('j'), character_button('k'), character_button('l'), character_button('m'), character_button('n'), character_button('o')],
            [character_button('p'), character_button('q'), character_button('r'), character_button('s'), character_button('t'), character_button('u')],
            [character_button('v'), character_button('w'), character_button('x'), character_button('y'), character_button('z')]
            	],
          'persian': [
            [character_button('ا'), character_button('ب'), character_button('پ'), character_button('ت'), character_button('ث'), character_button('ج'), character_button('چ'), character_button('ح')],
			[character_button('خ'), character_button('د'), character_button('ذ'), character_button('ر'), character_button('ز'), character_button('ژ'), character_button('س'), character_button('ش')],        
            [character_button('ص'), character_button('ض'), character_button('ط'), character_button('ظ'), character_button('ع'), character_button('غ'), character_button('ف'), character_button('ق')],
            [character_button('ک'), character_button('گ'), character_button('ل'), character_button('م'), character_button('ن'), character_button('و'), character_button('ه'), character_button('ی')]
          		]}

TOKEN = "1341319205:AAGnpvwy1rqPdfFBQkHLu9LVUuTrLLAsilI"

data = {}

def start(bot, update):
    keyboard = [['English', 'فارسی']]
    update.message.reply_text(REPLIES['welcome'])
    update.message.reply_text(REPLIES['language'], reply_markup=ReplyKeyboardMarkup(keyboard))
    return 'language'

def start_game(bot, update, wordset):
    
    file = open(FILES[wordset])
    lines = file.readlines()
    word = lines[randint(0, len(lines) - 1)][:-1]
    n_tries = 6
    word_placeholders = ""
    word_guessed = []
    for i in word:
    	if i == ' ':
    		word_placeholders += "   "
    	else:
        	word_placeholders += "__ "
            word_guessed.append('_')
    language = wordset
    if wordset == "proverb":
    	language = "persian"
    update.message.reply_text('بازی شروع شد', reply_markup = ReplyKeyboardRemove())
    update.message.reply_text(REPLIES['game'] % (update.message.from_user.full_name, GAMEMODES[wordset], n_tries, HANGMANPICS[0], word_placeholders), reply_markup = InlineKeyboardMarkup(CHARACTERS[language]))
    data[update.message.from_user.id] = {'type': wordset, 'word': word, 'tries_left': n_tries, 'letters_guessed': [], 'word_guessed': word_guessed}

def play(bot, update):
    callback = update.callback_query
    char = callback.data
    
  
def select_language(bot, update):
    language = update.message.text
    if language == 'English':
        start_game(bot, update, 'english')
        return 'play'
    else:
        keyboard = [['ضرب المثل', 'کلمه']]
        update.message.reply_text(REPLIES['farsi'], reply_markup=ReplyKeyboardMarkup(keyboard))
        return 'persian'

def select_farsi(bot, update):
    farsi = update.message.text
    if farsi == 'کلمه':
        start_game(bot, update, 'persian')
    else:
        start_game(bot, update, 'proverb')
    return 'play'

def invalid_answer_language(bot, update):
    update.message.reply_text(REPLIES['invalid_answer'])
    return 'language'

def invalid_answer_farsi(bot, update):
    update.message.reply_text(REPLIES['invalid_answer'])
    return 'farsi'

def cancel(bot, update):
  	return ConversationHandler.END
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            "language" : [RegexHandler('^(English|فارسی)$', select_language),
                          MessageHandler(Filters.all, invalid_answer_language)
                          ],
            "persian" : [RegexHandler('^(ضرب المثل|کلمه)$', select_farsi),
                       MessageHandler(Filters.all, invalid_answer_farsi)
                       ],
            "play" : [CallbackQueryHandler(play)]
          	
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    ))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
