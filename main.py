"""
Pepeland bondage bot
"""
try: 
	import replit
	on_server = True
except: on_server = False

server_text = "replit" if on_server else "local"
print(f"INFO:Running on {server_text} server")

if on_server: from background import keep_alive
import logging
import client
import minepi
import PIL
import os, io
from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import InputMedia, InputFile, CallbackQuery
from aiogram.types import ReplyKeyboardRemove, \
		ReplyKeyboardMarkup, KeyboardButton, \
		InlineKeyboardMarkup, InlineKeyboardButton
from colorthief import ColorThief
from datetime import datetime, date, time, timedelta  #Модуль времени
import pytz

if on_server: API_TOKEN = '6121533259:AAGkmSVFcTPlikJWieOvL3IDtOi7qdWEYO8'
else: API_TOKEN = '5850445478:AAFx4SZdD1IkSWc4h_0qU9IoXyT8VAElbTE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
listOfClients = []


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	now_time_log = datetime.now(pytz.timezone('Etc/GMT-3'))

	now_time_format = "{}.{}.{}-{}:{}".format(now_time_log.day,
																						now_time_log.month,
																						now_time_log.year,
																						now_time_log.hour,
																						now_time_log.minute)

	big_button_1: InlineKeyboardButton = InlineKeyboardButton(
		text='Из файла', callback_data='file')

	big_button_2: InlineKeyboardButton = InlineKeyboardButton(
		text='По нику', callback_data='nick')

	# Создаем объект инлайн-клавиатуры
	keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
		inline_keyboard=[[big_button_1], [big_button_2]])
	await message.answer("Привет! Давай начнём.\nОткуда брать скин?",
											 reply_markup=keyboard)
	global listOfClients
	if listOfClients == []: listOfClients.append(client.Client(message.chat.id))
	else:
		finded = False
		for add in range(len(listOfClients)):
			if listOfClients[add].chat_id == message.chat.id:
				finded == True
				listOfClients[add] = client.Client(message.chat.id)
				break
		if not finded: listOfClients.append(client.Client(message.chat.id))
	f_usr_list = []

	if os.path.isfile("usr.txt"):
		userListFile = open("usr.txt", 'r', encoding='utf-8')
		f_usr_list = userListFile.read().split("\n")
		userListFile.close()
		userListFile = open("usr.txt", 'a', encoding='utf-8')

	else:
		userListFile = open("usr.txt", 'w', encoding='utf-8')
		userListFile.close()
		userListFile = open("usr.txt", 'a', encoding='utf-8')

	if os.path.isfile("usr_use.txt"):
		userListFile1 = open("usr_use.txt", 'a', encoding='utf-8')

	else:
		userListFile1 = open("usr_use.txt", 'w', encoding='utf-8')
		userListFile1.close()
		userListFile1 = open("usr_use.txt", 'a', encoding='utf-8')
	if f_usr_list != []:
		if not str(f"https://t.me/{message.from_user.username}") in f_usr_list:
			userListFile.write(f"https://t.me/{message.from_user.username}\n")

	userListFile1.write(f"{message.from_user.username} - {now_time_format} - {message.from_user.id}\n")
	userListFile.close()
	userListFile1.close()


@dp.message_handler(commands=['donate'])
async def send_welcome(message: types.Message):
	await message.answer(
		"Вы можете поддержать разработчиков бота, отправив донат по ссылке\nhttps://www.donationalerts.com/r/andcool_systems"
	)


@dp.callback_query_handler(text="file")
async def from_f(message: CallbackQuery):
	await message.message.answer(
		'Хорошо, теперь отправь мне свой скин.\nОбязательно при отправке убери галочку "Сжать изображение"'
	)
	await message.message.delete()
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)
	listOfClients[id].wait_to_file = 1


@dp.callback_query_handler(text="nick")
async def from_f(message: CallbackQuery):
	await message.message.answer("Хорошо, теперь отправь мне свой никнейм.")
	await message.message.delete()
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)
	listOfClients[id].wait_to_file = 2


@dp.message_handler(content_types=['document'])
async def handle_docs_photo(message: types.Message):
	global listOfClients
	id = client.find_client(listOfClients, message.chat.id)

	if listOfClients[id].wait_to_file == 1:
		id1 = message.chat.id

		if document := message.document:
			await document.download(destination_file=f'{id1}.png', )
		try:
			usr_img = Image.open(f'{id1}.png').convert("RGBA")
			w, h = usr_img.size
			if w == 64 and h == 64:
				await listOfClients[id].init_mc_f(usr_img)
				listOfClients[id].wait_to_file = 0

				await listOfClients[id].prerender()

				skin_rer = await listOfClients[id].rerender()
				skin_rer.save(f'1-{id1}.png')
				photo = open(f'1-{id1}.png', 'rb')

				msg = await message.answer_photo(photo,
																				 "Вот предварительный просмотр")
				listOfClients[id].prewiew_id = msg
				photo.close()

				os.remove(f'1-{id1}.png')
				os.remove(f'{id1}.png')

				msg = await colorDialog(message, id)
				listOfClients[id].info_id = msg
			else:
				await message.reply(
					"Пожалуйста, отправьте развёртку скина в формате png с разрешением 64х64 пикселей"
				)
				usr_img.close()
				os.remove(f'{id1}.png')
		except:
			await message.reply(
				"Пожалуйста, отправьте развёртку скина в формате png с разрешением 64х64 пикселей"
			)
			os.remove(f'{id1}.png')


#---------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="red")
async def from_f(message: CallbackQuery):

	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)
	await listOfClients[id].info_id.delete()
	listOfClients[id].colour = 1

	skin_rer = await listOfClients[id].rerender()
	skin_rer.save(f'1-{id1}.png')

	photo = open(f'1-{id1}.png', 'rb')

	await listOfClients[id].prewiew_id.delete()
	msg = await message.message.answer_photo(photo,
																					 "Вот предварительный просмотр")
	listOfClients[id].prewiew_id = msg
	os.remove(f'1-{id1}.png')
	await acceptChoose(message.message)


@dp.callback_query_handler(text="green")
async def from_f(message: CallbackQuery):

	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)
	await listOfClients[id].info_id.delete()
	listOfClients[id].colour = 2

	skin_rer = await listOfClients[id].rerender()
	skin_rer.save(f'1-{id1}.png')

	photo = open(f'1-{id1}.png', 'rb')

	await listOfClients[id].prewiew_id.delete()
	msg = await message.message.answer_photo(photo,
																					 "Вот предварительный просмотр")
	listOfClients[id].prewiew_id = msg

	os.remove(f'1-{id1}.png')
	await acceptChoose(message.message)


@dp.callback_query_handler(text="blue")
async def from_f(message: CallbackQuery):

	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)
	await listOfClients[id].info_id.delete()
	listOfClients[id].colour = 3

	skin_rer = await listOfClients[id].rerender()
	skin_rer.save(f'1-{id1}.png')

	photo = open(f'1-{id1}.png', 'rb')
	await listOfClients[id].prewiew_id.delete()
	msg = await message.message.answer_photo(photo,
																					 "Вот предварительный просмотр")
	listOfClients[id].prewiew_id = msg

	os.remove(f'1-{id1}.png')
	await acceptChoose(message.message)


@dp.callback_query_handler(text="yellow")
async def from_f(message: CallbackQuery):

	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)
	await listOfClients[id].info_id.delete()
	listOfClients[id].colour = 4

	skin_rer = await listOfClients[id].rerender()
	skin_rer.save(f'1-{id1}.png')

	photo = open(f'1-{id1}.png', 'rb')

	await listOfClients[id].prewiew_id.delete()
	msg = await message.message.answer_photo(photo,
																					 "Вот предварительный просмотр")
	listOfClients[id].prewiew_id = msg
	os.remove(f'1-{id1}.png')
	await acceptChoose(message.message)


@dp.callback_query_handler(text="done_c")
async def from_f(message: CallbackQuery):

	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)

	await start_set(message.message)


@dp.callback_query_handler(text="custom")
async def from_f(message: CallbackQuery):

	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)
	await listOfClients[id].info_id.delete()
	listOfClients[id].colour = 5

	listOfClients[id].wait_to_file = 3

	#await message.message.delete()

	msg = await message.message.answer(
		"Теперь отправьте свой цвет в формате HEX\nЦвет можно получить на сайте https://colorscheme.ru/color-converter.html"
	)
	listOfClients[id].info_id = msg

#---------------------------------------------------------------------------------------------------
async def acceptChoose(message):
	global listOfClients
	id = client.find_client(listOfClients, message.chat.id)
	big_button_4: InlineKeyboardButton = InlineKeyboardButton(
			text='Готово', callback_data='done_d')

	big_button_5: InlineKeyboardButton = InlineKeyboardButton(
		text='Изменить цвет', callback_data='colD')

		# Создаем объект инлайн-клавиатуры
	keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup(
		inline_keyboard=[[big_button_4], [big_button_5]])
	msg = await message.answer("Готово?", reply_markup=keyboard1)
	listOfClients[id].info_id = msg
	

@dp.callback_query_handler(text="colD")
async def from_f(message: CallbackQuery):
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)
	await listOfClients[id].info_id.delete()
	msg = await colorDialog(message.message, id)
	listOfClients[id].info_id = msg
	

@dp.callback_query_handler(text="done_d")
async def from_f(message: CallbackQuery):
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)
	await listOfClients[id].info_id.delete()
	await start_set(message.message)
#---------------------------------------------------------------------------------------------------
async def colorDialog(message, id):
	global listOfClients
	
	big_button_1: InlineKeyboardButton = InlineKeyboardButton(
		text='Синий', callback_data='blue')

	big_button_2: InlineKeyboardButton = InlineKeyboardButton(
		text='Красный', callback_data='red')
	big_button_3: InlineKeyboardButton = InlineKeyboardButton(
		text='Зелёный', callback_data='green')
	big_button_4: InlineKeyboardButton = InlineKeyboardButton(
		text='Жёлтый', callback_data='yellow')

	big_button_5: InlineKeyboardButton = InlineKeyboardButton(
		text='Кастомный', callback_data='custom')

			# Создаем объект инлайн-клавиатуры
	keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup(
		inline_keyboard=[[big_button_1], 
										 [big_button_2], 
										 [big_button_3],
											[big_button_4], 
											[big_button_5]])
	msg = await message.answer("Теперь выбери цвет повязки",
															reply_markup=keyboard1)
	return msg
#---------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="done")
async def from_f(message: CallbackQuery):
	global listOfClients
	id1 = message.message.chat.id
	id = client.find_client(listOfClients, message.message.chat.id)
	listOfClients[id].skin_raw.save("2" + f'{id1}.png')
	await message.message.answer_document(open("2" + f'{id1}.png', "rb"))
	os.remove("2" + f'{id1}.png')
	await listOfClients[id].info_id.delete()
	listOfClients.pop(id)


#---------------------------------------------------------------------------------------------------
async def start_set(message):
	global listOfClients
	id = client.find_client(listOfClients, message.chat.id)

	big_button_1: InlineKeyboardButton = InlineKeyboardButton(text='↑',
																														callback_data='up')

	big_button_2: InlineKeyboardButton = InlineKeyboardButton(
		text=f'{listOfClients[id].pos}/8', callback_data='no')
	big_button_3: InlineKeyboardButton = InlineKeyboardButton(
		text='↓', callback_data='down')
	big_button_4: InlineKeyboardButton = InlineKeyboardButton(
		text='Первый слой', callback_data='first')

	big_button_7: InlineKeyboardButton = InlineKeyboardButton(text='В ч/б',
																														callback_data='bw')

	big_button_8: InlineKeyboardButton = InlineKeyboardButton(
		text='Инвертировать', callback_data='negative')

	big_button_9: InlineKeyboardButton = InlineKeyboardButton(
		text='Поза', callback_data='pose')

	big_button_5: InlineKeyboardButton = InlineKeyboardButton(
		text='Оверлей', callback_data='over')
	
	big_button_10: InlineKeyboardButton = InlineKeyboardButton(
		text='Часть тела', callback_data='body_part')
	
	big_button_11: InlineKeyboardButton = InlineKeyboardButton(
		text='-', callback_data='passs')
	
	big_button_12: InlineKeyboardButton = InlineKeyboardButton(
		text='-', callback_data='passs')

	big_button_6: InlineKeyboardButton = InlineKeyboardButton(
		text='Готово', callback_data='done')

	# Создаем объект инлайн-клавиатуры
	keyboard3: InlineKeyboardMarkup = InlineKeyboardMarkup()
	keyboard3.row(big_button_1, big_button_4, big_button_10, big_button_7)
	keyboard3.row(big_button_2, big_button_5, big_button_11, big_button_8)
	keyboard3.row(big_button_3, big_button_9, big_button_12, big_button_6)

	try: await listOfClients[id].info_id.delete()
	except: pass
	listOfClients[id].delete_mess = True
	txt11 = "Алекс" if listOfClients[id].slim else "Стив"
	txt1 = f"Версия скина: {txt11}\n"
	txt2 = f"Позиция повязки: {listOfClients[id].pos}\n"
	txt12 = "Вкл" if listOfClients[id].overlay else "Выкл"

	txt13 = "Выкл"
	if listOfClients[id].first_layer == 0: txt13 = "Выкл"
	elif listOfClients[id].first_layer == 1: txt13 = "Подкладка"
	elif listOfClients[id].first_layer == 2: txt13 = "Дублирование повязки"

	body = ["Левая рука", "Левая нога", "Правая рука", "Правая нога"]
	txt7 = f"Часть тела: {body[listOfClients[id].absolute_pos]}\n"

	txt14 = "Вкл" if listOfClients[id].bw else "Выкл"
	txt15 = "Вкл" if listOfClients[id].negative else "Выкл"

	txt3 = f"Оверлей: {txt12}\n"
	txt4 = f"Первый слой: {txt13}\n"
	txt5 = f"Чёрно-белый: {txt14}\n"
	txt6 = f"Негатив: {txt15}\n"
	msg = await message.answer(
		f"Параметры:\n{txt1}{txt2}{txt3}{txt4}{txt5}{txt6}{txt7}",
		reply_markup=keyboard3)
	listOfClients[id].info_id = msg


@dp.callback_query_handler(text="up")
async def from_f(message: CallbackQuery):

	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)

	if listOfClients[id].pos > 0:
		listOfClients[id].pos -= 1

	skin_rer = await listOfClients[id].rerender()
	skin_rer.save(f'1-{id1}.png')

	photo = open(f'1-{id1}.png', 'rb')
	await listOfClients[id].prewiew_id.delete()
	listOfClients[id].prewiew_id = await message.message.answer_photo(
		photo, "Вот предварительный просмотр")
	os.remove(f'1-{id1}.png')
	await start_set(message.message)


@dp.callback_query_handler(text="pose")
async def from_f(message: CallbackQuery):

	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)

	listOfClients[id].pose = not listOfClients[id].pose

	skin_rer = await listOfClients[id].rerender()
	skin_rer.save(f'1-{id1}.png')

	photo = open(f'1-{id1}.png', 'rb')
	await listOfClients[id].prewiew_id.delete()
	listOfClients[id].prewiew_id = await message.message.answer_photo(
		photo, "Вот предварительный просмотр")
	os.remove(f'1-{id1}.png')
	await start_set(message.message)


@dp.callback_query_handler(text="bw")
async def from_f(message: CallbackQuery):

	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)

	listOfClients[id].bw = not listOfClients[id].bw

	skin_rer = await listOfClients[id].rerender()
	skin_rer.save(f'1-{id1}.png')

	photo = open(f'1-{id1}.png', 'rb')
	await listOfClients[id].prewiew_id.delete()
	listOfClients[id].prewiew_id = await message.message.answer_photo(
		photo, "Вот предварительный просмотр")
	os.remove(f'1-{id1}.png')
	await start_set(message.message)


@dp.callback_query_handler(text="negative")
async def from_f(message: CallbackQuery):

	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)

	listOfClients[id].negative = not listOfClients[id].negative

	skin_rer = await listOfClients[id].rerender()
	skin_rer.save(f'1-{id1}.png')

	photo = open(f'1-{id1}.png', 'rb')
	await listOfClients[id].prewiew_id.delete()
	listOfClients[id].prewiew_id = await message.message.answer_photo(
		photo, "Вот предварительный просмотр")
	os.remove(f'1-{id1}.png')
	await start_set(message.message)


@dp.callback_query_handler(text="down")
async def from_f(message: CallbackQuery):
	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)

	if listOfClients[id].pos < 7:
		listOfClients[id].pos += 1

	skin_rer = await listOfClients[id].rerender()
	skin_rer.save(f'1-{id1}.png')

	photo = open(f'1-{id1}.png', 'rb')
	await listOfClients[id].prewiew_id.delete()
	listOfClients[id].prewiew_id = await message.message.answer_photo(
		photo, "Вот предварительный просмотр")
	os.remove(f'1-{id1}.png')
	await start_set(message.message)


@dp.callback_query_handler(text="first")
async def from_f(message: CallbackQuery):
	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)

	listOfClients[id].first_layer += 1

	if listOfClients[id].first_layer > 2: listOfClients[id].first_layer = 0

	skin_rer = await listOfClients[id].rerender()
	skin_rer.save(f'1-{id1}.png')

	photo = open(f'1-{id1}.png', 'rb')
	await listOfClients[id].prewiew_id.delete()
	listOfClients[id].prewiew_id = await message.message.answer_photo(
		photo, "Вот предварительный просмотр")
	os.remove(f'1-{id1}.png')
	await start_set(message.message)


@dp.callback_query_handler(text="over")
async def from_f(message: CallbackQuery):
	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)

	listOfClients[id].overlay = not listOfClients[id].overlay

	skin_rer = await listOfClients[id].rerender()
	skin_rer.save(f'1-{id1}.png')

	photo = open(f'1-{id1}.png', 'rb')
	await listOfClients[id].prewiew_id.delete()
	listOfClients[id].prewiew_id = await message.message.answer_photo(
		photo, "Вот предварительный просмотр")
	os.remove(f'1-{id1}.png')
	await start_set(message.message)

@dp.callback_query_handler(text="body_part")
async def from_f(message: CallbackQuery):
	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)

	listOfClients[id].absolute_pos += 1

	if listOfClients[id].absolute_pos > 3: listOfClients[id].absolute_pos = 0

	skin_rer = await listOfClients[id].rerender()
	skin_rer.save(f'1-{id1}.png')

	photo = open(f'1-{id1}.png', 'rb')
	await listOfClients[id].prewiew_id.delete()
	listOfClients[id].prewiew_id = await message.message.answer_photo(
		photo, "Вот предварительный просмотр")
	os.remove(f'1-{id1}.png')
	await start_set(message.message)
#---------------------------------------------------------------------------------------------------
@dp.message_handler(content_types=['any'])
async def echo(message: types.Message):
	global listOfClients
	id = client.find_client(listOfClients, message.chat.id)
	id1 = message.chat.id
	#if listOfClients[id].delete_mess: await message.delete()
	if listOfClients[id].wait_to_file == 2:
		done = await listOfClients[id].init_mc_n(message.text)
		if done:
			listOfClients[id].wait_to_file = 0

			await listOfClients[id].prerender()

			skin_rer = await listOfClients[id].rerender()
			skin_rer.save(f'1-{id1}.png')
			photo = open(f'1-{id1}.png', 'rb')

			msg = await message.answer_photo(photo, "Вот предварительный просмотр")
			listOfClients[id].prewiew_id = msg
			photo.close()

			msg = await colorDialog(message, id)
			os.remove(f'1-{id1}.png')
			listOfClients[id].info_id = msg
		else:
			await message.answer("Аккаунт с таким именем не найден(")
	if listOfClients[id].wait_to_file == 3:
		try:
			await listOfClients[id].info_id.delete()
			msg_c = message.text.lstrip('#')
			colour = tuple(int(msg_c[i:i + 2], 16) for i in (0, 2, 4))
			listOfClients[id].bondg_color = colour

			await message.delete()
			listOfClients[id].wait_to_file = 0
			skin_rer = await listOfClients[id].rerender()

			skin_rer.save(f'1-{id1}.png')
			photo = open(f'1-{id1}.png', 'rb')
			await listOfClients[id].prewiew_id.delete()
			msg = await message.answer_photo(photo, "Вот предварительный просмотр")
			listOfClients[id].prewiew_id = msg
			photo.close()

			big_button_4: InlineKeyboardButton = InlineKeyboardButton(
				text='Готово', callback_data='done_c')

			big_button_5: InlineKeyboardButton = InlineKeyboardButton(
				text='Изменить цвет', callback_data='custom')

			# Создаем объект инлайн-клавиатуры
			keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup(
				inline_keyboard=[[big_button_4], [big_button_5]])
			msg = await message.answer("Готово?", reply_markup=keyboard1)
			os.remove(f'1-{id1}.png')
			listOfClients[id].info_id = msg

		except Exception as e:
			await message.answer("Не удалось получить цвет(\nПопробуйте ещё раз")


if on_server: keep_alive()
if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
