from aiogram import (
    Bot,
    Dispatcher,
    executor,
    types,
)
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from autocorrect import Speller
from googletrans import Translator
import asyncio
import googletrans
import config
from nltk.corpus import wordnet

API_TOKEN = config.configuration['token']
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def helpcommand(message: types.Message):
    text = '''Texthelper бот поможет тебе с текстом!
Команды:
    /upper - перевод в верхний регистр
    /lower - перевод в нижний регистр
    /checkru - проверка орфографии (рус.)
    /checkeng - проверка орфографии (англ.)
    /countletters - кол-во букв
    /countwords - кол-во слов
    /lang - определение языка
    /transru - перевод (рус.)
    /transeng - перевод (англ.)
    /synonym - синонимы
    /antonym - антонимы'''
    await message.reply(text)

# переводит сообщение пользователя в верхний регистр
@dp.message_handler(commands=['upper'])
async def upper(message: types.Message):
    usertext = message.get_args()
    await message.reply(f'Твой текст: {usertext.upper()}')

# переводит сообщение пользователя в нижний регистр
@dp.message_handler(commands=['lower'])
async def lower(message: types.Message):
    usertext = message.get_args()
    await message.reply(f'Твой текст: {usertext.lower()}')

# проверяет русский текст на ошибки
@dp.message_handler(commands=['checkru'])
async def checkru(message: types.Message):
    await message.answer('Проверка может занять от 15 секунд или более')
    # asyncio для отправки ^, без будет ждать выполнения spell()
    await asyncio.sleep(0.1)
    spell = Speller('ru')
    await message.reply(f'Твой текст (Возможны ошибки): {spell(message.get_args())}')

# проверяет английский текст на ошибки
@dp.message_handler(commands=['checkeng'])
async def checkeng(message: types.Message):
    spell = Speller('en')
    await message.reply(f'Твой текст (Возможны ошибки): {spell(message.get_args())}')

# считает количество букв в тексте
@dp.message_handler(commands=['countletters'])
async def checkletters(message: types.Message):
    await message.reply(f'В твоем тексте {len(str(message.get_args()))} букв')

# считает слова в тексте
@dp.message_handler(commands=['countwords'])
async def checkwords(message: types.Message):
    usertext = message.get_args()
    await message.reply(f'В твоем тексте {len(usertext.split())} слов(а)')

# определяет язык текста/слова
@dp.message_handler(commands=['lang'])
async def checklang(message: types.Message):
    try:
        await message.answer('Определяю язык текста/слова...')
        await asyncio.sleep(0.1)
        #определяет язык
        language = googletrans.Translator().detect(message.get_args()).lang
        if len(language) > 1:
            await message.reply('Я думаю что это '+''.join(config.ln_lang[language]))
        if len(language) == 1:
            await message.reply(f'Я думаю что это {config.ln_lang[language]}!')
    except:
        await message.reply('Вы не указали слово/язык или данный язык не найден')

#переводит текст на русский язык
@dp.message_handler(commands=['transru'])
async def translaterussian(message: types.Message):
    usertext = message.get_args()
    tr = Translator()
    src = tr.detect(usertext).lang
    if src == "ru":
        await message.reply(f'В вашем сообщение нету слова или текста, или текст/слово написан(о) на русском')
    else:
        translated = tr.translate(text = usertext, src = src, dest = 'ru')
        await message.reply(f'Перевод текста/слова на русский язык: {translated.text}')

#переводит текст на английский язык
@dp.message_handler(commands=['transeng'])
async def translateenligsh(message: types.Message):
    usertext = message.get_args()
    tr = Translator()
    src = tr.detect(usertext).lang
    if src == "en":
        await message.reply(f'В вашем сообщение нету слова или текста, или текст/слово написан(о) на английском')
    else:
        translated = tr.translate(text = usertext, src = src, dest = 'en')
        await message.reply(f'Перевод текста/слова на английский язык: {translated.text}')

@dp.message_handler(commands=['synonym'])
async def findsynonym(message: types.Message):
    try:
        text = message.get_args()
        synonyms = []
        for syn in wordnet.synsets(text):
            for l in syn.lemmas():
                if l.name().lower() not in synonyms and len(synonyms)<10:
                    synonyms.append(l.name().lower())
                else:
                    pass
        await message.answer('Возможные синонимы '+', '.join(synonyms))
    except IndexError:
        await message.reply('Данный язык не поддерживается, или не синонимы не найдены')

@dp.message_handler(commands=['antonym'])
async def antonym(message: types.Message):
    try:
        text = message.get_args()
        synsets = wordnet.synsets(text)
        antonyms = []
        for synset in synsets:
            for lemma in synset.lemmas():
                if lemma.antonyms():
                    if lemma.antonyms()[0].name() in antonyms or lemma.antonyms()[0].name().lower() in antonyms:
                        pass
                    else:
                        antonyms.append(lemma.antonyms()[0].name())
                else:
                    pass
        await message.answer('Возможные антонимы '+', '.join(antonyms))
    except IndexError:
        await message.reply('Данный язык не поддерживается, или не антонимы не найдены')

if __name__ == '__main__':   
    executor.start_polling(dp, skip_updates=True)
