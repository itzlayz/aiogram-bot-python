from aiogram import (
    Bot,
    Dispatcher,
    executor,
    types,
)
from autocorrect import Speller
from googletrans import Translator
import asyncio
import googletrans
import languages

API_TOKEN = "api token"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def starthelp(message: types.Message):
    await message.reply("Привет! Данный бот поможет тебе с текстом на русском и английском, все команды есть в меню.")

# переводит сообщение пользователя в верхний регистр
@dp.message_handler(commands=['upper'])
async def upper(message: types.Message):
    usertext = message.text[7:]
    await message.reply(f'Твой текст: {usertext.upper()}')

# переводит сообщение пользователя в нижний регистр
@dp.message_handler(commands=['lower'])
async def lower(message: types.Message):
    usertext = message.text[7:]
    await message.reply(f'Твой текст: {usertext.lower()}')

# переводит первую букву текста в верхний регистр
@dp.message_handler(commands=['up'])
async def firstupper(message: types.Message):
    usertext = message.text[12:]
    await message.reply(f'Твой текст: {usertext.capitalize()}')

# проверяет русский текст на ошибки
@dp.message_handler(commands=['checkru'])
async def checkru(message: types.Message):
    await message.answer('Проверка может занять от 15 секунд или более')
    # asyncio для отправки ^, без будет ждать выполнения spell()
    await asyncio.sleep(0.1)
    # язык русский
    spell = Speller('ru')
    await message.reply(f'Твой текст (Возможны ошибки): {spell(message.text[8:])}')

# проверяет английский текст на ошибки
@dp.message_handler(commands=['checkeng'])
async def checkeng(message: types.Message):
    #язык английский
    spell = Speller('en')
    await message.reply(f'Твой текст (Возможны ошибки): {spell(message.text[9:])}')

# считает количество букв в тексте
@dp.message_handler(commands=['countletters'])
async def checkletters(message: types.Message):
    total_letters = [total_letters+1 for letter in message.text]
    await message.reply(f'В твоем тексте {total_letters} букв')

# считает слова в тексте
@dp.message_handler(commands=['countwords'])
async def checkwords(message: types.Message):
    words = message.text[12:].split()
    await message.reply(f'В твоем тексте {len(words)} слов(а)')

# определяет язык текста/слова
@dp.message_handler(commands=['lang'])
async def checklang(message: types.Message):
    try:
        await message.answer('Определяю язык текста/слова... \n Язык будет написан как en, es, pt!')
        await asyncio.sleep(0.1)
        #определяет язык
        language = googletrans.Translator().detect(message.text[6:]).lang
        if len(language) > 1:
            await message.reply('Я думаю что это '+' '.join(languages.ln_lang[language]))
        if len(language) == 1:
            await message.reply(f'Я думаю что это {languages.ln_lang[language]}!')
    except Exception as error:
        await message.reply('ошибка {}'.format(error))

@dp.message_handler(commands=['translate'])
async def checklang(message: types.Message):
    tr = Translator()
    src = tr.detect(message.text[11:]).lang
    translated = tr.translate(text = message.text[11:], src = src, dest = 'ru')
    await message.reply(f'Перевод текста/слова: {translated.text}')

if __name__ == '__main__':   
    executor.start_polling(dp, skip_updates=True)
