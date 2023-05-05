import telebot

# Create a new bot with your API token
bot = telebot.TeleBot("5861916928:AAF1szw5vhSWcaGksYeO2m9bS4FENSE6W9M")

# Define the game and its variables
word = "vefa","cengo","mamaklı","ışık","özcan","aslı","emine","fatma","oktay","ilkay"
guesses = []
max_guesses = 6

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
    bot.reply_to(message, "Ooooo yigenim hoş geldin başlamak açın /haydi komutunu kullan.")

# Define the game play command
@bot.message_handler(commands=['haydi'])
def play_game(message):
    global word, guesses
    word = ("vefa", "Mamaklı", "cengo", "fatmazel")
    guesses = []
    bot.reply_to(message, "Adam Asmaca oynayalım! {}-harfli bir kelime düşünüyorum. Sohbete yazarak bir harf tahmin edin..".format(len(word)))

# Define the game guess handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global word, guesses, max_guesses
    if len(guesses) >= max_guesses:
        bot.reply_to(message, "Üzgünüz, tahminleriniz tükendi! Kelime {}.".format(word))
        return
    guess = message.text.lower()
    if guess in guesses:
        bot.reply_to(message, "O harfi zaten tahmin ettin! Tekrar tahmin et..")
        return
    guesses.append(guess)
    if guess in word:
        if set(word) == set(guesses):
            bot.reply_to(message, "Tebrikler, kazandınız! Kelime {}.".format(word))
            return
        else:
            masked_word = "".join([letter if letter in guesses else "_" for letter in word])
            bot.reply_to(message, "İyi tahmin! Şimdiye kadarki kelime:\n{}\n{}".format(masked_word, hangman_drawings[len(guesses)-1]))
    else:
        bot.reply_to(message, "Üzgünüm, o harf kelimede yok. Tekrar tahmin et..")
        bot.reply_to(message, "{}\n{}".format(" ".join(guesses), hangman_drawings[len(guesses)-1]))

# Start the bot
bot.polling()
