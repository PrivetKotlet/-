from telebot import types
import config
import parss



class keyboard():
    class inline():

        def main_menu_keyboard():
            markup = types.InlineKeyboardMarkup()
            for i in parss.sq.select.get_workers(config.COFFE_HOUSE_NAME):
                config.fio.append(i)
                markup.add(types.InlineKeyboardButton(text = i,callback_data=i))
            return markup

    class non_inline_keyboard():

        def main_keyboard():
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            keyboard = types.KeyboardButton(text = 'Выбрать замену 🗄')
            keyboard_2 = types.KeyboardButton(text = 'Записать замену 📝')
            keyboard_3 = types.KeyboardButton(text = 'Взятые замены 📊')
            keyboard_4 = types.KeyboardButton(text = 'Отданные замены 👐')
            keyboard_5 = types.KeyboardButton(text = 'Требуемые замены🔖')
            return markup.add(keyboard,keyboard_2,keyboard_3,keyboard_4,keyboard_5)

        def delete_key():
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            keyboard = types.KeyboardButton(text = 'Удалить Замену 🗑')
            keyboard2 = types.KeyboardButton(text = 'Редактировать дату замены 📆')
            keyboard3 = types.KeyboardButton(text = 'Редактировать время работы⏳')
            keyboard4 = types.KeyboardButton(text = 'Назад 🔙')
            return markup.add(keyboard,keyboard2,keyboard3,keyboard4)

        def choosed_rep_keyboard():
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            keyboard = types.KeyboardButton(text = 'Вернуть замену в общий лист замен')
            keyboard4 = types.KeyboardButton(text = 'Назад 🔙')
            return markup.add(keyboard,keyboard4)
        
        def demanding_replecement_keyboard():
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            keyboard = types.KeyboardButton(text = 'Записать 📝')
            keyboard2 = types.KeyboardButton(text = 'Посмотреть 🗄')
            keyboard4 = types.KeyboardButton(text = 'Назад 🔙')
            return markup.add(keyboard,keyboard2,keyboard4)
            
        def demanding_replecement_keyboard2():
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            keyboard = types.KeyboardButton(text = 'Удалить 📝')
            keyboard4 = types.KeyboardButton(text = 'Назад 🔙')
            return markup.add(keyboard,keyboard4)
         
        def back_keyboard():
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            keyboard4 = types.KeyboardButton(text = 'Назад 🔙')
            return markup.add(keyboard4)


