import telebot

# Create a new bot with your API token
bot = telebot.TeleBot("5861916928:AAF1szw5vhSWcaGksYeO2m9bS4FENSE6W9M")

# Define the game and its variables
word = "vefa","cengo","mamaklı","ışık"
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
    bot.reply_to(message, "Welcome to Hangman! Type /play to start a new game.")

# Define the game play command
@bot.message_handler(commands=['play'])
def play_game(message):
    global word, guesses
    word = "python"
    guesses = []
    bot.reply_to(message, "Let's play Hangman! I'm thinking of a {}-letter word. Guess a letter by typing it in the chat.".format(len(word)))

# Define the game guess handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global word, guesses, max_guesses
    if len(guesses) >= max_guesses:
        bot.reply_to(message, "Sorry, you've run out of guesses! The word was {}.".format(word))
        return
    guess = message.text.lower()
    if guess in guesses:
        bot.reply_to(message, "You already guessed that letter! Guess again.")
        return
    guesses.append(guess)
    if guess in word:
        if set(word) == set(guesses):
            bot.reply_to(message, "Congratulations, you've won! The word was {}.".format(word))
            return
        else:
            masked_word = "".join([letter if letter in guesses else "_" for letter in word])
            bot.reply_to(message, "Good guess! The word so far is:\n{}\n{}".format(masked_word, hangman_drawings[len(guesses)-1]))
    else:
        bot.reply_to(message, "Sorry, that letter is not in the word. Guess again.")
        bot.reply_to(message, "{}\n{}".format(" ".join(guesses), hangman_drawings[len(guesses)-1]))

# Start the bot
bot.polling()
