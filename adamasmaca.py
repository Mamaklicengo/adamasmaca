import telethon
import asyncio

class adamasmaca:
    def __init__(self, client, chat_id, word):
        self.client = client
        self.chat_id = chat_id
        self.word = word
        self.lives = 6
        self.guessed = set()
        self.game_over = False

    async def play(self):
        await self.client.send_message(self.chat_id, f"Adam asmaca oyununa hoşgeldiniz! {len(self.word)} harfli bir kelime söyleyin.")
        await self.show_word()
        while not self.game_over:
            guess = await self.get_input()
            if guess == self.word:
                await self.client.send_message(self.chat_id, "Tebrikler, doğru bildiniz!")
                self.game_over = True
            elif guess in self.guessed:
                await self.client.send_message(self.chat_id, f"{guess} zaten tahmin edildi.")
            else:
                self.guessed.add(guess)
                if guess not in self.word:
                    self.lives -= 1
                    await self.show_adamasmacs()
                    if self.lives == 0:
                        await self.client.send_message(self.chat_id, f"Kaybettiniz! Kelime {self.word} idi.")
                        self.game_over = True
                    else:
                        await self.client.send_message(self.chat_id, f"{guess} yanlış tahmin. {self.lives} canınız kaldı.")
                else:
                    await self.show_word()
                    if set(self.word) == self.guessed:
                        await self.client.send_message(self.chat_id, "Tebrikler, doğru bildiniz!")
                        self.game_over = True

    async def get_input(self):
        message = await self.client.send_message(self.chat_id, "Bir harf veya kelime tahmin edin.\n"
                                                             "Her yanlış tahminde adamın bir bölümü çizilecektir.")
        guess = (await self.client.get_messages(self.chat_id, limit=1))[0].message.strip().lower()
        while not guess.isalpha() or len(guess) > 1 and len(guess) != len(self.word):
            await self.client.send_message(self.chat_id, "Geçersiz tahmin. Lütfen bir harf veya kelime girin.")
            guess = (await self.client.get_messages(self.chat_id, limit=1))[0].message.strip().lower()
        return guess

    async def show_word(self):
        display_word = "".join([c if c in self.guessed else "_" for c in self.word])
        await self.client.send_message(self.chat_id, display_word)

    async def show_adamasmaca(self):
        stages = [  
            """
                 --------
                 |      |
                 |      O
                 |
                 |
                 |
                 -
            """,
            """
                 --------
                 |      |
                 |      O
                 |      |
                 |      |
                 |
                 -
            """,
            """
                 --------
                 |      |
                 |      O
                 |     \|
                 |      |
                 |
                 -
            """,
            """
                 --------
                 |      |
                 |      O
                 |     \|/
                 |      |
                 |
                 -
            """,
            """
                 --------
                 |      |
                 |      O
                 |     \|/
                 |      |
                 |     /
                 -
            """,
            """
                 --------
                 |      |
                 |      O
                 |     \|/
                 |      |
                 |     / \\
                 -
            """
        ]
        await self.client.send_message(self.chat_id, stages[self.lives])
        
api_id = '25989627'
api_hash = 'dff2250c7620fef64cd17e4355432d82'
bot_token = '6022154020:AAEekctwuqrK8ZchRxW4_CPVEn-srDGgEYo'

client = telethon.TelegramClient('adamasmamaca', api_id, api_hash).start(bot_token=bot_token)


@client.on(telethon.events.NewMessage(pattern='/adamasmaca'))
async def adamasmaca(event):
    game = adamasmaca(client, event.chat_id, "telethon")
    await game.play()

async def main():
    await client.start()
    await client.run_until_disconnected()

asyncio.run(main())
