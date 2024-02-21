from telebot import TeleBot, types
import random

# Create a new bot with your API token
bot = TeleBot("6704245576:AAGqYQrMMuH2yt2sHJ9Zhk7q2wtNrDA_Eow")


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


bot.polling()
