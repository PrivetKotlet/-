import telebot
import config
import keyboard
import parss
from data_chek import chek
from colorama import Fore
from requests import exceptions

'''
   _____/ /_____ ___________   _________  / __/ __/__  ___
  / ___/ __/ __ `/ ___/ ___/  / ___/ __ \/ /_/ /_/ _ \/ _ /
 (__  ) /_/ /_/ / /  (__  )  / /__/ /_/ / __/ __/  __/  __/
/____/\__/\__,_/_/  /____/   \___/\____/_/ /_/  \___/\___/
'''



token = '5650906424:AAEd1pu_F61aYY5gQTxeQlzqsYCSnaCaLOM'


bot = telebot.TeleBot(token, parse_mode = None, threaded= False )


#Приветсвенное сообщение
@bot.message_handler(commands=['start',])
def send_welcome(message):
	bot.send_message(message.chat.id, "Привет я рабочий бот stars coffee ☕️",reply_markup= keyboard.keyboard.non_inline_keyboard.main_keyboard()) 


@bot.message_handler(commands=['help',])
def send_help(message):
	bot.send_message(message.chat.id, '''/start - запуск бота
/help - Помощь
/autocast - подписка на авторассылку
/coffee_house_registered - регистрация кофейн (Для Админа)
/coffee_house_delete -удаление кофейн (Для Админа)
/worker_registered -регистрация работников
/worker_deleted -удаление работников''',reply_markup= keyboard.keyboard.non_inline_keyboard.main_keyboard()) 


#авторассылка
@bot.message_handler(commands=['autocast',])
def send_autocast(message):
	bot.send_message(message.chat.id, "Чтобы получать уведомления введите пароль УКа ")
	bot.register_next_step_handler(message, reg_autocast)

def reg_autocast(message):
	record_in_config(message.text)
	if chek.chek_Yk_password(config.password_YK) == True:
		config.user_id = message.from_user.id
		parss.sq.update.update_user_id(config.user_id,config.COFFE_HOUSE_NAME)
		bot.send_message(message.chat.id,'Вы подписанны на уведомления')
	else:
		invalid_password(message)
	


#Регистрация кофеен
@bot.message_handler(commands=['coffee_house_registered',])
def reg(message):
		bot.send_message(message.chat.id, "Введите Логин Администратора")
		bot.register_next_step_handler(message, login)

def login(message):
	if message.text == 'НАЗАД':
		bot.send_message(message.chat.id, "Напишите НАЗАД ещё раз ")
		bot.register_next_step_handler(message,send_welcome)
	else:
		config.admin.admin_login = message.text
		bot.send_message(message.chat.id, "Введите Пароль Администратора")
		bot.register_next_step_handler(message, chek_login_and_password)

#Проверка логина и пароля администратора
def chek_login_and_password(message):
	config.admin.admin_password = str(message.text)
	if parss.sq.select.chek(config.admin.admin_login,config.admin.admin_password) == True:
		bot.send_message(message.chat.id, "Введите Название Кофейни")
		bot.register_next_step_handler(message, reg_coffee_house)
	else:
		bot.send_message(message.chat.id, "Логин или пароль не верный 🤨")
		bot.send_message(message.chat.id, "Введите Логин Администратора. Напишите НАЗАД если хотите выйти")
		bot.register_next_step_handler(message, login)


def reg_coffee_house(message):
	config.COFFE_HOUSE_NAME = str(message.text)
	bot.send_message(message.chat.id, "Введите ФИО УКА")
	bot.register_next_step_handler(message, reg_YK)


def reg_YK(message):
	config.YK_NAME = str(message.text)
	bot.send_message(message.chat.id, "Введите Пароль УКА")
	bot.register_next_step_handler(message, reg_YK_password)

def reg_YK_password(message):
	config.password_YK = str(message.text)
	parss.sq.insert.insert_coffee_house(config.COFFE_HOUSE_NAME,config.YK_NAME,config.password_YK)
	bot.send_message(message.chat.id, "Кофейня успешно зарегистрированна")

#удаление кофейни
@bot.message_handler(commands=['coffee_house_delete',])
def reg1(message):
		bot.send_message(message.chat.id, "Введите Логин Администратора")
		bot.register_next_step_handler(message, login1)

def login1(message):
	if message.text == 'НАЗАД':
		bot.send_message(message.chat.id, "Напишите НАЗАД ещё раз ")
		bot.register_next_step_handler(message,send_welcome)
	else:
		config.admin.admin_login = message.text
		bot.send_message(message.chat.id, "Введите Пароль Администратора")
		bot.register_next_step_handler(message, chek_login_and_password1)

#Проверка логина и пароля администратора
def chek_login_and_password1(message):
	config.admin.admin_password = str(message.text)
	if parss.sq.select.chek(config.admin.admin_login,config.admin.admin_password) == True:
		bot.send_message(message.chat.id, "Введите Название Кофейни")
		bot.register_next_step_handler(message, delete_coffee_house)
	else:
		bot.send_message(message.chat.id, "Логин или пароль не верный 🤨")
		bot.send_message(message.chat.id, "Введите Логин Администратора. Напишите НАЗАД если хотите выйти")
		bot.register_next_step_handler(message, login1)

def delete_coffee_house(message):
	config.COFFE_HOUSE_NAME = str(message.text)
	mes = parss.sq.delete.delete_coffe_house(config.COFFE_HOUSE_NAME)
	bot.send_message(message.chat.id,"Кофейня удаленна ")

#регистрация сотрудников
@bot.message_handler(commands=['worker_registered',])

def protect(message):
	bot.send_message(message.chat.id, "Введите пароль УКа ")
	bot.register_next_step_handler(message, name_worker)

def name_worker(message):
	if chek.chek_Yk_password(message.text) == True:
		config.COFFE_HOUSE_NAME = parss.sq.select.get_coffee_house(message.text)
		bot.send_message(message.chat.id, "Введите ФИО Партнера ")
		bot.register_next_step_handler(message, contact_worker)
	else:
		invalid_password(message)


def contact_worker(message):
	config.FIO_WORKER = str(message.text)
	bot.send_message(message.chat.id, "Введите номер телефона партнера для связи в формате +7XXXXXXXXXX 📱")
	bot.register_next_step_handler(message, post_wprcers)

def post_wprcers(message):
	if chek.chek_contact(message.text) == True:
		config.CONTACT_WORKERS = str(message.text)
		bot.send_message(message.chat.id, "Введите должность партнера")
		bot.register_next_step_handler(message, fin_reg)
	else:
		bot.send_message(message.chat.id, 'Номер телефона партнера был записан в некоректном формате')
		bot.send_message(message.chat.id, "Введите номер телефона партнера для связи в формате +7XXXXXXXXXX 📱")
		bot.register_next_step_handler(message, post_wprcers)


def fin_reg(message):
	config.post= str(message.text)
	bot.send_message(message.chat.id, "Партнер зарегистрирован")
	parss.sq.insert.insert_worker(config.FIO_WORKER,config.COFFE_HOUSE_NAME,config.post,config.CONTACT_WORKERS)


#удаление сотрудников
@bot.message_handler(commands=['worker_deleted',])
def delete_worker(message):
	bot.send_message(message.chat.id, "Введите пароль УКа ")
	bot.register_next_step_handler(message, delete_workers_2)

def delete_workers_2(message):
	record_in_config(message.text)
	if chek.chek_Yk_password(config.password_YK) == True:
		bot.send_message(message.chat.id, "Введите ФИО партнера")
		bot.register_next_step_handler(message, delete_workers_3)
	else:
		invalid_password(message)

def delete_workers_3(message):
	parss.sq.delete.delete_workers(config.COFFE_HOUSE_NAME,message.text)
	bot.send_message(message.chat.id,'Партнер был удалён')

@bot.message_handler(content_types=['sticker'])
def stick(message):
	bot.send_message(message.chat.id,'Это классный стикер )))')


#Обработка текста и неинлайновых кнопок
@bot.message_handler(content_types=['text'])
def text_handler(message):
	match message.text:
		case 'Привет':
			bot.send_message(message.chat.id, "Привет я рабочий бот напиши команду help ")
		case'Выбрать замену 🗄':
			bot.send_message(message.chat.id, "Введите пароль УКа")
			bot.register_next_step_handler(message, select_rep_for_mes)
		case 'Записать замену 📝':
			bot.send_message(message.chat.id, "Введите пароль УКа")
			bot.register_next_step_handler(message, fio_workers)
		case 'Взятые замены 📊':
			bot.send_message(message.chat.id, "Введите пароль УКа")
			bot.register_next_step_handler(message, select_choosed_replacemenr)
		case "Отданные замены 👐":
			bot.send_message(message.chat.id, "Введите пароль УКа")
			bot.register_next_step_handler(message, seleсе_my_rep)
		case 'Требуемые замены🔖':
			bot.send_message(message.chat.id, "Введите пароль УКа")
			bot.register_next_step_handler(message, demanding_replecement)
		case 'Назад 🔙':
			send_welcome(message)
		case _:
			bot.send_message(message.chat.id, 'Я вас не понял')

#Требуемые замены
def demanding_replecement(message):
	record_in_config(message.text)
	if chek.chek_Yk_password(config.password_YK) == True:
		bot.send_message(message.chat.id, "Выбирете записать или просмотреть",reply_markup= keyboard.keyboard.non_inline_keyboard.demanding_replecement_keyboard())
		bot.register_next_step_handler(message, demanding_replecement_text)
	else:
		invalid_password(message)

def demanding_replecement_text(message):
	match message.text:
		case 'Записать 📝':
			bot.send_message(message.chat.id, "Введите дату требуемой замены", reply_markup= None)
			bot.register_next_step_handler(message, demanding_day) 
		case'Посмотреть 🗄':
			try:
				bot.send_message(message.chat.id, parss.sq.select.select_demanding_replacement(),reply_markup= keyboard.keyboard.non_inline_keyboard.demanding_replecement_keyboard2())
				bot.register_next_step_handler(message, text_demanding_replecement) 
			except telebot.apihelper.ApiTelegramException:
				bot.send_message(message.chat.id,"Похоже что никто не требует замены")
		case 'Назад 🔙':
			send_welcome(message)

def text_demanding_replecement(message):
	match message.text:
		case 'Удалить 📝':
			bot.send_message(message.chat.id, 'Введите ID записи',reply_markup= None)
			bot.register_next_step_handler(message, delete_demanding_replecrmrnt)
		case 'Назад 🔙':
			send_welcome(message)

def delete_demanding_replecrmrnt(message):
	if chek.chek_iddm(message.text) == True:
		if chek.chek_coffe_house_name_for_rep(message.text,config.COFFE_HOUSE_NAME,2) == True:
			parss.sq.delete.delete_demanding_replacment(message.text)
			bot.send_message(message.chat.id, 'Требуемая замена удалена',reply_markup= keyboard.keyboard.non_inline_keyboard.main_keyboard())
		else:
			bot.send_message(message.chat.id, 'Вы не можете удалить чужую замену',reply_markup= keyboard.keyboard.non_inline_keyboard.main_keyboard())
	else:
		bot.send_message(message.chat.id, "Данный id нераспознан или же был записан в некоректном формате")

#Запись требуемой замены
def demanding_day(message):
	config.demanding_replecement.date = message.text
	bot.send_message(message.chat.id, "Введите должность партнера для требуемой замены", reply_markup= None)
	bot.register_next_step_handler(message, demanding_post) 

def demanding_post(message):
	if message.text == 'Назад 🔙':
		send_welcome(message)
	else:
		config.demanding_replecement.demanding_post = message.text
		bot.send_message(message.chat.id, "Введите временной промежуток для требуемой замены", reply_markup= None)
		bot.register_next_step_handler(message, finish_demanding_replecement) 

def finish_demanding_replecement(message):
	if message.text == 'Назад 🔙':
		send_welcome(message)
	else:
		bot.send_message(message.chat.id, "Требуемая замена записана", reply_markup= keyboard.keyboard.non_inline_keyboard.main_keyboard())
		parss.sq.insert.insert_demanding_replacement(config.demanding_replecement.date,parss.sq.select.get_coffee_house(config.password_YK),config.demanding_replecement.demanding_post,message.text)




#ВЫБОР ЗАМЕНЫ
def select_rep_for_mes(message):
	record_in_config(message.text)
	try:
		if chek.chek_Yk_password(config.password_YK) == True:
			mes = parss.sq.select.select_replacement()
			bot.send_message(message.chat.id, "Выбирите замену записав id записи")
			bot.send_message(message.chat.id, mes, reply_markup= keyboard.keyboard.non_inline_keyboard.back_keyboard())
			bot.register_next_step_handler(message, choose_replacement)
		else:
			invalid_password(message)
	except telebot.apihelper.ApiTelegramException:
		bot.send_message(message.chat.id, "Похоже свободных замен нету",reply_markup= keyboard.keyboard.non_inline_keyboard.back_keyboard())
		bot.register_next_step_handler(message, choose_replacement)

def choose_replacement(message):
	id = message.text
	if id == 'Назад 🔙':
		send_welcome(message)
	else:
		if chek.chek_coffe_house_name_for_rep(id,config.COFFE_HOUSE_NAME,1) == True:
			if chek.chek_id(id) == True:
				parss.sq.update.update_replacement(message.text,config.COFFE_HOUSE_NAME)
				config.replecemt = parss.sq.select.select_replacementByID(id)
				autocoast(id)
				bot.send_message(message.chat.id, "Замена выбрана",reply_markup= keyboard.keyboard.non_inline_keyboard.back_keyboard())
			else:
				bot.send_message(message.chat.id, "Данный id нераспознан или же был записан в некоректном формате",reply_markup= keyboard.keyboard.non_inline_keyboard.back_keyboard())
		else:
			bot.send_message(message.chat.id, "Замена не выбрана вы выбираете своего же работника")
			bot.send_sticker(message.chat.id,"CAACAgEAAxkBAAEGS0hjY33rRTmMu1a9trHGfj5AQIOfWAACKwIAAjbd2UeL36EJdj6f4ioE",reply_markup= keyboard.keyboard.non_inline_keyboard.back_keyboard())

#ЗАПИСЬ ЗАМЕНЫ
def fio_workers(message):
	record_in_config(message.text)
	if chek.chek_Yk_password(config.password_YK) == True:
		bot.send_message(message.chat.id, "Выберите Партнера",reply_markup= keyboard.keyboard.inline.main_menu_keyboard())
	else:
		invalid_password(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	config.chosen.fio_worker_chosen = str(call.data)
	if call.data in config.fio:
		bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="Введите Временной промежуток Партнера ⏳ ",reply_markup= None)
		bot.register_next_step_handler(call.message,rep_day)

def rep_day (message):
	config.chosen.time_line = message.text
	bot.send_message(message.chat.id, "Введите дату замены")
	bot.register_next_step_handler(message,rep_comments)

def rep_comments(message):
	config.day = message.text
	bot.send_message(message.chat.id, "Введите комментарий")
	bot.register_next_step_handler(message,rep_finished)


def rep_finished(message):
	parss.sq.insert.insert_replacement(config.chosen.fio_worker_chosen,config.COFFE_HOUSE_NAME,parss.sq.select.select_replacement_post(config.COFFE_HOUSE_NAME,config.chosen.fio_worker_chosen ),parss.sq.select.select_replacement_contact(config.COFFE_HOUSE_NAME,config.chosen.fio_worker_chosen ),config.chosen.time_line,config.day, message.text)
	bot.send_message(message.chat.id, "Замена записана 👍")


#Просмотр взятых замен
def select_choosed_replacemenr(message):
	record_in_config(message.text)
	if chek.chek_Yk_password(config.password_YK) == True:
		try:
			bot.send_message(message.chat.id,parss.sq.select.select_choosed_replacement(config.COFFE_HOUSE_NAME),reply_markup= keyboard.keyboard.non_inline_keyboard.choosed_rep_keyboard())
			bot.register_next_step_handler(message,text_hendler_for_choosed_rep)
		except telebot.apihelper.ApiTelegramException:
			bot.send_message(message.chat.id,'Похоже что вы не взяли не одной замены ',reply_markup= None)
	else:
		invalid_password(message)

def text_hendler_for_choosed_rep(message):
	match message.text:
		case 'Вернуть замену в общий лист замен':
			bot.send_message(message.chat.id, "Введите id замены")
			bot.register_next_step_handler(message, select_status_of_rep)
		case 'Назад 🔙':
			send_welcome(message)
		

def select_status_of_rep(message):
	parss.sq.update.update_choosed_replacement(config.COFFE_HOUSE_NAME,message.text)
	config.replecemt = parss.sq.select.select_replacementByID(message.text)
	autocoast2(message.text)
	bot.send_message(message.chat.id, "Замена возвращенна ", reply_markup= keyboard.keyboard.non_inline_keyboard.main_keyboard())

#Просмотр отданых замен
def seleсе_my_rep(message):
	record_in_config(message.text)
	
	if chek.chek_Yk_password(config.password_YK) == True:
		mes =parss.sq.select.select_my_replacement(config.COFFE_HOUSE_NAME)
		try:
			bot.send_message(message.chat.id,mes,reply_markup= keyboard.keyboard.non_inline_keyboard.delete_key())
			bot.register_next_step_handler(message,text_select_my_rep)
		except telebot.apihelper.ApiTelegramException:
			bot.send_message(message.chat.id,'Похоже что вы не отдавали замен',reply_markup= None)
	else:
		invalid_password(message)

def text_select_my_rep(message):
	match message.text:
		case 'Удалить Замену 🗑':
			bot.send_message(message.chat.id, "Введите id замены")
			bot.register_next_step_handler(message, delete_my_replecement)
		case 'Редактировать дату замены 📆':
			bot.send_message(message.chat.id, "Введите id замены")
			bot.register_next_step_handler(message, get_new_date)
		case 'Редактировать время работы⏳':
			bot.send_message(message.chat.id, "Введите id замены")
			bot.register_next_step_handler(message, get_new_time)
		case 'Назад 🔙':
			send_welcome(message)

#Удалить замену
def delete_my_replecement(message):
	parss.sq.delete.delete_replacment(message.text,config.COFFE_HOUSE_NAME)
	bot.send_message(message.chat.id, "Замена удалена",reply_markup= keyboard.keyboard.non_inline_keyboard.main_keyboard())

#Редактировать временной промежуток замены
def get_new_time(message):
	config.id = message.text
	bot.send_message(message.chat.id, "Введите новый временной промежуток")
	bot.register_next_step_handler(message,update_time_replacement )

def update_time_replacement(message):
	parss.sq.update.update_time_replacement(config.id,message.text)
	bot.send_message(message.chat.id,"Временной промежуток изменён",reply_markup= keyboard.keyboard.non_inline_keyboard.main_keyboard())

#редактировать дату
def get_new_date(message):
	config.id = message.text
	bot.send_message(message.chat.id, "Введите новую дату")
	bot.register_next_step_handler(message,update_date_replacement )

def update_date_replacement(message):
	parss.sq.update.update_date_replacement(config.id,message.text)
	bot.send_message(message.chat.id,"Дата изменина",reply_markup= keyboard.keyboard.non_inline_keyboard.main_keyboard())

#Неправильный пароль
def invalid_password(message):
	bot.send_message(message.chat.id, "Пароль неверный 🤨 ")
	bot.send_sticker(message.chat.id,"CAACAgEAAxkBAAEGS0hjY33rRTmMu1a9trHGfj5AQIOfWAACKwIAAjbd2UeL36EJdj6f4ioE", reply_markup=keyboard.keyboard.non_inline_keyboard.main_keyboard())

#запись пароля и названия кофейни 
def record_in_config(password):
	config.password_YK = password
	config.COFFE_HOUSE_NAME = parss.sq.select.get_coffee_house(config.password_YK)
	try:
		config.password_YK = str(config.password_YK)
	except TypeError as erorr:
		config.password_YK = " "

def autocoast(message):
	coffee_house  = parss.sq.select.select_coffee_houseByID(message)
	user_id = parss.sq.select.select_user_id(coffee_house)
	if user_id == None: 
		pass
	else:
		bot.send_message(user_id,'У вас взяли замену')
		bot.send_message(user_id,config.replecemt)

def autocoast2(message):
	coffee_house  = parss.sq.select.select_coffee_houseByID(message)
	user_id = parss.sq.select.select_user_id(coffee_house)
	if user_id == None: 
		pass
	else:
		bot.send_message(user_id,'замена была возвращенна в общий лист замен')
		bot.send_message(user_id,config.replecemt)

def main():
	try:
		print(Fore.GREEN + "start")
		bot.polling()
	except exceptions.ConnectionError as eror:
		print(Fore.RED + 'Нет подключения к интернету')

	
if __name__ == "__main__":
	main()