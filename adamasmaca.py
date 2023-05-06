from telebot import TeleBot, types
import random

# Create a new bot with your API token
bot = TeleBot("5861916928:AAF1szw5vhSWcaGksYeO2m9bS4FENSE6W9M")

# Define the game and its variables
words = "vefa","cengo","mamaklı","ışık","özcan","aslı","emine","fatma","oktay","ilkay"
guesses = []
max_guesses = 6
game_started = False
word = ""

# Define the hangman drawing
hangman_drawings = [
    "  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\  |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\  |\n /    |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\  |\n / \  |\n      |\n========="
]

# Define the game start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global game_started, guesses, word
    game_started = False
    guesses = []
    word = ""
    bot.reply_to(message, "Ooooo yigenim hoş geldin! Adam Asmaca oynamak için /haydi komutunu kullan.")

# Define the game play command
@bot.message_handler(commands=['haydi'])
def play_game(message):
    global game_started, word, guesses
    if game_started:
        bot.reply_to(message, "Oyun zaten başladı, lütfen devam edin.")
        return
    word = random.choice(words)
    guesses = []
    game_started = True
    bot.reply_to(message, "Adam Asmaca oynayalım! {} harfli bir kelime düşünüyorum. Sohbete yazarak bir harf veya tam kelime tahmin edin..".format(len(word)))

# Define the game guess handler
@bot.message_handler(func=lambda message: game_started and message.text.isalpha() and (len(message.text)==1 or len(message.text)==len(word)))
def handle_message(message):
    global word, guesses, max_guesses, game_started
    guess = message.text.lower()
    if guess in guesses:
        bot.reply_to(message, "O harfi/kelimeyi zaten tahmin ettin! Tekrar tahmin et..")
        return
    guesses.append(guess)
    if word == guess:
        bot.reply_to(message, "Tebrikler, kazandınız! Kelime {}.".format(word))
        game_started = False
        return
    if len(guess) == len(word):
        if guess == word:
            bot.reply_to(message, "Tebrikler, kazandınız! Kelime {}.".format(word))
            game_started = False
            return
        else:
            bot.reply_to(message, "Üzgünüm, yanlış kelime tahmini. Tekrar tahmin et..")
            bot.reply_to(message, "{}\n{}".format(" ".join(guesses), hangman_drawings[len(guesses)-1]))
            if len(guesses) >= max_guesses:
                bot.reply_to(message, "Üzgünüz, tahminleriniz tükendi! Kelime {}.".format(word))
                game_started = False
    else:
        if guess in word:
            masked_word = "".join([letter if letter in guesses else "_" for letter in word])
            bot.reply_to(message, "İyi tahmin! Şimdiye kadarki kelime:\n{}\n{}".format(masked_word, hangman_drawings[len(guesses)]))
            if masked_word == word:
                bot.reply_to(message, "Tebrikler, kazandınız! Kelime {}.".format(word))
                game_started = False
        else:
            bot.reply_to(message, "Üzgünüm, o harf kelimede yok. Tekrar tahmin et..")
            bot.reply_to(message, "{}\n{}".format(" ".join(guesses), hangman_drawings[len(guesses)-1]))
            if len(guesses) >= max_guesses:
                bot.reply_to(message, "Üzgünüz, tahminleriniz tükendi! Kelime {}.".format(word))
                game_started = False

# Ignore messages that are not game related
@bot.message_handler(func=lambda message: True)
def ignore_message(message):
    if game_started:
        bot.reply_to(message, "Oyun devam ediyor, lütfen sadece harf veya kelime tahminleri yapın.")
    else:
        pass

flags = [{'name': 'Türkiye', 'emoji': '🇹🇷'},
         {'name': 'Brezilya', 'emoji': '🇧🇷'},
         {'name': 'Japonya', 'emoji': '🇯🇵'},
         {'name': 'Fransa', 'emoji': '🇫🇷'},
         {'name': 'İtalya', 'emoji': '🇮🇹'}]



# Check answer function
def check_answer(message):
    user_answer = message.text.lower()
    flag = bot.flag
    if user_answer == flag['name'].lower():
        bot.send_message(message.chat.id, "Doğru cevap! Yeni bir bayrak gösteriliyor.")
        game(message.chat.id)
    else:
        
        bot.register_next_step_handler(message, check_answer)

# Game function
def game(chat_id):
    flag = random.choice(flags)
    bot.flag = flag
    bot.send_message(chat_id, f"Aşagıda gösterilen Bayrağın ülkesini yazın...")
    bot.register_next_step_handler(bot.send_message(chat_id, f"{flag['emoji']}"), check_answer)

# Start command handler
@bot.message_handler(commands=['bayrak'])
def bayrak(message):
    bot.send_message(message.chat.id, "Bayrak tahmin oyununa hoş geldiniz!")
    game(message.chat.id)


bot.polling()
