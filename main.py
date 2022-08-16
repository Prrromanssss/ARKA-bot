import asyncio
import config
import telebot.async_telebot
import message as msg_text
from telebot import types


bot = telebot.async_telebot.AsyncTeleBot(config.API_TOKEN)
flags_for_names = {}  # There is not register_nest_step_handler
                      # in async_telebot, that's why such crutch
names = {}
usernames = {}
flag_for_last1 = {}
flag_for_last2 = {}
msg_for_delete = {}
admin_password_flag = {}
admin_stop_msg = {}
polls = {}
focies = {}
list_of_polls = {}
flag_for_list_polls = {}
main_pol = {}


'''Commands handlers'''
@bot.message_handler(commands=['start'])
async def get_commands(message):
    flags_for_names[message.chat.id] = True
    text = msg_text.RegularUser().start()
    await bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['admin'])
async def admin_command(message):
    text = 'Введите пароль, чтобы войти в качестве админа\n'

    admin_password_flag[message.chat.id] = True
    await bot.send_message(message.chat.id, text)


'''Message handlers'''
@bot.message_handler(content_types=['text'])
async def get_text_msg(message):
    if flags_for_names.get(message.chat.id):
        flags_for_names[message.chat.id] = False
        names[message.chat.id] = message.text
        usernames[message.chat.id] = message.from_user.username
        admin_password_flag[message.chat.id] = False
        await products(message)
    elif message.text == 'Портфолио':
        admin_password_flag[message.chat.id] = False
        await portfolio(message)
    elif message.text == 'Наш сайт':
        admin_password_flag[message.chat.id] = False
        await site(message)
    elif message.text == 'Связаться с нами':
        admin_password_flag[message.chat.id] = False
        await contact(message)
    elif message.text == 'Наш канал':
        admin_password_flag[message.chat.id] = False
        await channel(message)
    elif message.text in ['<< Назад', 'Опросник']:
        admin_stop_msg[message.chat.id] = False
        admin_password_flag[message.chat.id] = False
        flag_for_list_polls[message.chat.id] = False
        list_of_polls[message.chat.id] = []
        main_pol[message.chat.id] = ''
        await products(message)
    elif message.text == 'Далее':
        admin_stop_msg[message.chat.id] = False
        admin_password_flag[message.chat.id] = False
        await products(message)
    elif flag_for_last1.get(message.chat.id):

        await bot.send_message(message.chat.id, f'Ваше место: {message.text}')
        polls[message.chat.id] += f'Место: {message.text}\n'
        text = msg_text.LastGroup().last_2()
        await bot.send_message(message.chat.id, text)
        flag_for_last2[message.chat.id] = True
        flag_for_last1[message.chat.id] = False
    elif flag_for_last2.get(message.chat.id) and flag_for_list_polls.get(message.chat.id):
        await bot.send_message(message.chat.id, f'Вы хотите приступить: {message.text}')
        polls[message.chat.id] += f'Вы хотите приступить: {message.text}\n\n'
        flag_to_continue = True
        if list_of_polls.get(message.chat.id):

            main_pol[message.chat.id] = main_pol.get(message.chat.id, '') + '\n' + polls[message.chat.id]

            try:
                list_of_polls[message.chat.id].remove(''.join(polls[message.chat.id].split('\n')[2]).split(':')[-1].strip())
            except Exception:
                flag_to_continue = False
                txt_bad_choice = 'Данная категория не была добавлена к заказу.\nДля того, чтобы выбрать сразу несколько категорий,' \
                                 'нажмите кнопку "Несколько печей"'

                await bot.send_message(message.chat.id, txt_bad_choice)
        if not list_of_polls.get(message.chat.id):
            text = msg_text.LastGroup().last_buy(message.chat.id, names)
            await bot.send_message(config.chat_to_poll['arka_pechnik'], main_pol[message.chat.id])
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton(text='Портфолио'))
            markup.add(types.KeyboardButton(text='Наш канал'))
            markup.add(types.KeyboardButton(text='Связаться с нами'))
            markup.add(types.KeyboardButton(text=f'Наш сайт'))
            markup.add(types.KeyboardButton(text='<< Назад'))
            await bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html')
            flag_for_list_polls[message.chat.id] = False
        else:
            if flag_to_continue:
                text = 'Вы заполнили не все заказы, нажмите "Далеe", чтобы закончить'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(types.KeyboardButton(text='Далее'))
                await bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html')
        flag_for_last2[message.chat.id] = False
    elif flag_for_last2.get(message.chat.id) and not flag_for_list_polls.get(message.chat.id):
        await bot.send_message(message.chat.id, f'Вы хотите приступить: {message.text}')
        polls[message.chat.id] += f'Вы хотите приступить: {message.text}\n'
        text = msg_text.LastGroup().last_buy(message.chat.id, names)
        await bot.send_message(config.chat_to_poll['arka_pechnik'], polls[message.chat.id])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(text='Портфолио'))
        markup.add(types.KeyboardButton(text='Наш канал'))
        markup.add(types.KeyboardButton(text='Связаться с нами'))
        markup.add(types.KeyboardButton(text=f'Наш сайт'))
        markup.add(types.KeyboardButton(text='<< Назад'))
        await bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html')
        flag_for_last2[message.chat.id] = False
    elif admin_password_flag.get(message.chat.id):
        if message.text == config.admin_password:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton(text='<< Назад'))
            text = msg_text.AdminUser().start(names[message.chat.id])
            admin_password_flag[message.chat.id] = False
            admin_stop_msg[message.chat.id] = True
            await bot.send_message(message.chat.id, text, reply_markup=markup)
        else:
            text = msg_text.AdminUser().password_false()
            await bot.send_message(message.chat.id, text)
    elif admin_stop_msg.get(message.chat.id):
        await newsletter(message)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Опросник', callback_data='Questionnaire'))
        text = msg_text.RegularUser().unknown()
        await bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(content_types=config.CONTENT_TYPES)
async def newsletter(message):
    if admin_stop_msg.get(message.chat.id):
        for user in names:
            await bot.forward_message(user, message.chat.id, message.message_id)


async def channel(message):
    text = msg_text.RegularUser().channel()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Перейти', url='https://t.me/arka_pechi'))
    await bot.send_message(message.chat.id, text=text, reply_markup=markup)



'''Functions for ReplyKeyboardMarkup'''


async def site(message):
    text = msg_text.RegularUser().site()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Перейти', url=config.SITE_URL))
    await bot.send_message(message.chat.id, text=text, reply_markup=markup)


async def portfolio(message):
    text = msg_text.RegularUser().portfolio()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Печи', url='https://t.me/+8xk3vH5YSuoxOWMy'))
    markup.add(types.InlineKeyboardButton(text='Барбекю', url='https://t.me/+NhMVJp9xHSo2NDdi'))
    await bot.send_message(message.chat.id, text=text, reply_markup=markup)


async def contact(message):
    text = msg_text.RegularUser().contact()
    await bot.send_message(message.chat.id, text=text)


async def products(message):
    text = msg_text.RegularUser().products(names[message.chat.id])
    markup = types.InlineKeyboardMarkup(row_width=3)
    if message.text == 'Далее':
        text += f'\nВам осталось выбрать: {", ".join(list_of_polls[message.chat.id])}'
    markup.add(types.InlineKeyboardButton(text='Печь для отопления дома', callback_data='A1'))
    markup.add(types.InlineKeyboardButton(text='Печь для бани', callback_data='B1'))
    markup.add(types.InlineKeyboardButton(text='Камин', callback_data='C1'))
    markup.add(types.InlineKeyboardButton(text='Комплекс барбекю', callback_data='D1'))
    markup.add(types.InlineKeyboardButton(text='Несколько печей', callback_data='E1'))
    markup.add(types.InlineKeyboardButton(text='Другое', callback_data='F_last'))
    await bot.send_message(message.chat.id, text=text, reply_markup=markup)

    text = 'Если у вас возникли вопросы, внизу появились кнопки - воспользуйтесь ими '

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text='Портфолио'))
    markup.add(types.KeyboardButton(text='Наш канал'))
    markup.add(types.KeyboardButton(text='Связаться с нами'))
    markup.add(types.KeyboardButton(text=f'Наш сайт'))
    markup.add(types.KeyboardButton(text='<< Назад'))
    msg = await bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html')
    msg_for_delete[message.chat.id] = msg


'''Callback handlers'''

@bot.callback_query_handler(func=lambda callback: 'A' in callback.data and 'last' not in callback.data)
async def group_A(callback):

    text = eval(f'msg_text.AGroup().{callback.data.lower().split("__")[0] if "__" in callback.data else callback.data.lower().split("_")[0]}()')
    markup = types.InlineKeyboardMarkup()
    if 'A1' in callback.data:
        polls[callback.message.chat.id] = f'Пользователь: {names[callback.message.chat.id]}\n' \
                                              f'Юзернейм: @{usernames[callback.message.chat.id]}\n' \
                                              f'Что интересует: Печь для отопления дома\n'

        markup.add(types.InlineKeyboardButton(text='одной', callback_data='A2__1'))
        markup.add(types.InlineKeyboardButton(text='в двух', callback_data='A2__2'))
        markup.add(types.InlineKeyboardButton(text='в трёх и более.', callback_data='A2__3'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'A2' in callback.data and 'A2_1' not in callback.data:

        pol_txt = {'1': 'в одной', '2': 'в двух', '3': 'в трёх и более.'}
        polls[callback.message.chat.id] += f'Количество комнат: {pol_txt[callback.data.split("__")[-1]]}\n'
        for i in range(10):
            markup.add(types.InlineKeyboardButton(text=f'{i}', callback_data=f'A2_1{i}'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'A2_1' in callback.data:

        square = ''.join(callback.message.text.split(':')[-1]).split('кв')[0].strip()
        for i in range(10):
            markup.add(types.InlineKeyboardButton(text=f'{i}', callback_data=f'A2_1{i}'))
        markup.add(types.InlineKeyboardButton(text='Ввод окончен', callback_data='A3'))
        square = square + callback.data.split('A2_1')[-1] if square != '0' else callback.data.split('A2_1')[-1]
        text = ''.join(callback.message.text.split(':')[0]) + f': {square} кв. м.'
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'A3' in callback.data:
        pol_text = callback.message.text.split(':')[-1]
        polls[callback.message.chat.id] += f'Площадь: {pol_text}\n'
        markup.add(types.InlineKeyboardButton(text='отопление', callback_data='A4__1'))
        markup.add(types.InlineKeyboardButton(text='с варочной плитой', callback_data='A4__2'))
        markup.add(types.InlineKeyboardButton(text='с духовкой (хлебной камерой)', callback_data='A4__3'))
        markup.add(types.InlineKeyboardButton(text='с варочной плитой и духовкой', callback_data='A4__4'))
        markup.add(types.InlineKeyboardButton(text='с лежанкой', callback_data='A4__5'))
        markup.add(types.InlineKeyboardButton(text='русская печь классическая', callback_data='A4__6'))
        markup.add(types.InlineKeyboardButton(text='русская печь с подтопком', callback_data='A4__7'))
        markup.add(types.InlineKeyboardButton(text='с пристроенным камином', callback_data='A4__8'))
        markup.add(types.InlineKeyboardButton(text='каминопечь', callback_data='A4__9'))
        markup.add(types.InlineKeyboardButton(text='пока не выбрали, посоветуйте.', callback_data='A4__10'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'A4' in callback.data:
        pol_txt = {'1': 'отопление', '2': 'с варочной плитой', '3': 'с духовкой (хлебной камерой)',
                   '4': 'с варочной плитой и духовкой', '5': 'с лежанкой', '6': 'русская печь классическая',
                   '7': 'русская печь с подтопком', '8': 'с пристроенным камином', '9': 'каминопечь',
                   '10': 'пока не выбрали, посоветуйте.'}
        polls[callback.message.chat.id] += f'Вид и функционал: {pol_txt[callback.data.split("__")[-1]]}\n'
        markup.add(types.InlineKeyboardButton(text='основной источник тепла, проживаем в доме постоянно',
                                              callback_data='A5__1'))
        markup.add(types.InlineKeyboardButton(text='резервный источник тепла', callback_data='A5__2'))
        markup.add(types.InlineKeyboardButton(text='это дача, жить постоянно здесь не планируем.', callback_data='A5__3'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'A5' in callback.data:
        pol_txt = {'1': 'основной источник тепла, проживаем в доме постоянно', '2': 'резервный источник тепла', '3': 'это дача, жить постоянно здесь не планируем.'}
        polls[callback.message.chat.id] += f'Печь нужна как: {pol_txt[callback.data.split("__")[-1]]}\n'
        markup.add(types.InlineKeyboardButton(text='да', callback_data='A6__1'))
        markup.add(types.InlineKeyboardButton(text='пока нет, но строительство уже начато', callback_data='A6__2'))
        markup.add(types.InlineKeyboardButton(text='нет, сейчас делаем проект.', callback_data='A6__3'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'A6' in callback.data:
        pol_txt = {'1': 'да', '2': 'пока нет, но строительство уже начато', '3': 'нет, сейчас делаем проект.'}
        polls[callback.message.chat.id] += f'Дом уже построен: {pol_txt[callback.data.split("__")[-1]]}\n'

        markup.add(types.InlineKeyboardButton(text='да', callback_data='A_last__1'))
        markup.add(types.InlineKeyboardButton(text='нет', callback_data='A_last__2'))
        markup.add(types.InlineKeyboardButton(text='нужна консультация печника', callback_data='A_last__3'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: 'B' in callback.data and 'last' not in callback.data)
async def group_B(callback):

    markup = types.InlineKeyboardMarkup()
    if 'B1' in callback.data:
        text = msg_text.BGroup().b1()
        polls[callback.message.chat.id] = f'Пользователь: {names[callback.message.chat.id]}\n' \
                                          f'Юзернейм: @{usernames[callback.message.chat.id]}\n' \
                                          f'Что интересует: Печь для бани\n'
        markup.add(types.InlineKeyboardButton(text=f'1', callback_data=f'B2'))
        markup.add(types.InlineKeyboardButton(text=f'2', callback_data=f'B3'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'B2' in callback.data or 'B3' in callback.data:
        text = msg_text.BGroup().b2()
        if callback.data == 'B2':
            polls[callback.message.chat.id] += f'Печь: Кирпичная печь-каменка с закладкой из чугуна – классика русской бани. \n'
        elif callback.data == 'B3':
            polls[callback.message.chat.id] += f'Печь: Металлическая печь, совмещённая с отопительным щитком из кирпича \n'
        markup.add(types.InlineKeyboardButton(text='домашняя баня', callback_data='B4'))
        markup.add(types.InlineKeyboardButton(text='общественная баня.', callback_data='B5'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'B4' in callback.data or 'B5' in callback.data:
        text = msg_text.BGroup().b3()
        pol_txt = {'B4': 'домашняя баня', 'B5': 'общественная баня.'}
        polls[callback.message.chat.id] += f'Тип бани: {pol_txt[callback.data]}\n'
        for i in range(10):
            markup.add(types.InlineKeyboardButton(text=f'{i}', callback_data=f'B6_1{i}'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)

    elif 'B6_1' in callback.data:
        square = ''.join(callback.message.text.split(':')[-1]).split('кв')[0].strip()
        for i in range(10):
            markup.add(types.InlineKeyboardButton(text=f'{i}', callback_data=f'B6_1{i}'))
        markup.add(types.InlineKeyboardButton(text='Ввод окончен', callback_data='B6'))
        square = square + callback.data.split('B6_1')[-1] if square != '0' else callback.data.split('B6_1')[-1]
        text = ''.join(callback.message.text.split(':')[0]) + f': {square} кв. м.'
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'B6' in callback.data and 'B6_1' not in callback.data:
        text = msg_text.BGroup().b4()
        pol_text = callback.message.text.split(':')[-1]
        polls[callback.message.chat.id] += f'Площадь помещения парной: {pol_text}\n'
        markup.add(types.InlineKeyboardButton(text='бревно (брус)', callback_data='B7__1'))
        markup.add(types.InlineKeyboardButton(text='кирпич', callback_data='B7__2'))
        markup.add(types.InlineKeyboardButton(text='керамические блоки', callback_data='B7__3'))
        markup.add(types.InlineKeyboardButton(text='газосиликатные блоки', callback_data='B7__4'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'B7' in callback.data:
        text = msg_text.BGroup().b5()
        pol_txt = {'1': 'бревно (брус)', '2': 'кирпич', '3': 'керамические блоки', '4': 'газосиликатные блоки'}
        polls[callback.message.chat.id] += f'Из какого материала построена баня: {pol_txt[callback.data.split("__")[-1]]}\n'
        markup.add(types.InlineKeyboardButton(text='да', callback_data='B_last__1'))
        markup.add(types.InlineKeyboardButton(text='нет', callback_data='B_last__2'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: 'C' in callback.data and 'last' not in callback.data)
async def group_C(callback):

    markup = types.InlineKeyboardMarkup()
    if 'C1' in callback.data and len(callback.data) == 2:
        text = msg_text.CGroup().c1()
        polls[callback.message.chat.id] = f'Пользователь: {names[callback.message.chat.id]}\n' \
                                              f'Юзернейм: @{usernames[callback.message.chat.id]}\n' \
                                              f'Что интересует: Камин\n'
        for i in range(10):
            markup.add(types.InlineKeyboardButton(text=f'{i}', callback_data=f'C1{i}'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)

    elif 'C1' in callback.data and len(callback.data) > 2:

        square = ''.join(callback.message.text.split(':')[-1]).split('кв')[0].strip()
        for i in range(10):
            markup.add(types.InlineKeyboardButton(text=f'{i}', callback_data=f'C1{i}'))
        markup.add(types.InlineKeyboardButton(text='Ввод окончен', callback_data='C2'))
        square = square + callback.data.split('C1')[-1] if square != '0' else callback.data.split('C1')[-1]
        text = ''.join(callback.message.text.split(':')[0]) + f': {square} кв. м.'
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'C2' in callback.data and len(callback.data) == 2:
        text = msg_text.CGroup().c2()
        pol_text = callback.message.text.split(':')[-1]
        polls[callback.message.chat.id] += f'Площадь помещения, где планируется разместить камин: {pol_text}\n'

        for i in range(10):
            markup.add(types.InlineKeyboardButton(text=f'{i}', callback_data=f'C2{i}'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'C2' in callback.data and len(callback.data) > 2:
        square = ''.join(callback.message.text.split(':')[-1]).split('м')[0].strip()
        for i in range(10):
            markup.add(types.InlineKeyboardButton(text=f'{i}', callback_data=f'C2{i}'))
        markup.add(types.InlineKeyboardButton(text='Ввод окончен', callback_data='C3'))
        square = square + callback.data.split('C2')[-1] if square != '0' else callback.data.split('C2')[-1]
        text = ''.join(callback.message.text.split(':')[0]) + f': {square} м.'
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'C3' in callback.data:
        text = msg_text.CGroup().c3()
        pol_text = callback.message.text.split(':')[-1]
        polls[callback.message.chat.id] += f'Высота потолка в этом помещении: {pol_text}\n'

        markup.add(types.InlineKeyboardButton(text='просто аккуратная кирпичная кладка', callback_data='C_last__1'))
        markup.add(types.InlineKeyboardButton(text='изразцы', callback_data='C_last__2'))
        markup.add(types.InlineKeyboardButton(text='камень', callback_data='C_last__3'))
        markup.add(types.InlineKeyboardButton(text='пока выбираем, советуемся с дизайнером', callback_data='C_last__4'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: ('D' in callback.data and 'last' not in callback.data)
                                                  or ('d' in callback.data and 'radio' not in callback.data))
async def group_D(callback):

    markup = types.InlineKeyboardMarkup()
    if 'D1' in callback.data and 'radio' not in callback.data:

        text = msg_text.DGroup().d1()
        polls[callback.message.chat.id] = f'Пользователь: {names[callback.message.chat.id]}\n' \
                                          f'Юзернейм: @{usernames[callback.message.chat.id]}\n' \
                                          f'Что интересует: Комплекс барбекю\n'
        foci = ['мангал', 'печь казана', 'тандыр', 'русская печь',
                'хлебная печь (духовка)', 'помпейская печь (пицца-печь)',
                'коптильня', 'мойка']
        for foc in foci:
            markup.add(types.InlineKeyboardButton(text=foc, callback_data=f'D1_radio_{foc}'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'radio' in callback.data:

        foci = ['мангал', 'печь казана', 'тандыр', 'русская печь',
                'хлебная печь (духовка)', 'помпейская печь (пицца-печь)',
                'коптильня', 'мойка']

        focies[callback.message.chat.id] = focies.get(callback.message.chat.id, []) + [callback.data.split('_')[-1]]
        for foc in foci:
            if foc in focies[callback.message.chat.id]:
                markup.add(types.InlineKeyboardButton(text=f'\u2705 {foc}', callback_data=f'D1_radio_{foc}'))
            else:
                markup.add(types.InlineKeyboardButton(text=foc, callback_data=f'D1_radio_{foc}'))
        text = callback.message.text.split(':')[-1]
        if not text.strip():
            text += callback.data.split('_')[-1] + '.'
        elif callback.data.split('_')[-1] not in text.split('.')[0]:
            text = text.split('.')[0] + ', ' + callback.data.split('_')[-1] + '.'
        text = callback.message.text.split(':')[0] + ':' + text

        markup.add(types.InlineKeyboardButton(text='Выбор окончен', callback_data=f'D2'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'D2' in callback.data:
        text = msg_text.DGroup().d2()
        pol_text = ', '.join(focies[callback.message.chat.id])
        del focies[callback.message.chat.id]
        polls[callback.message.chat.id] += f'Какие очаги и элементы Вы выбираете: {pol_text}\n'

        markup.add(types.InlineKeyboardButton(text='отдельная беседка', callback_data='d31'))
        markup.add(types.InlineKeyboardButton(text='веранда дома', callback_data='d32'))
        markup.add(types.InlineKeyboardButton(text='веранда бани', callback_data='d33'))
        markup.add(types.InlineKeyboardButton(text='другое', callback_data='d34'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'd3' in callback.data:
        text = msg_text.DGroup().d3()

        pol_txt = {'1': 'отдельная беседка', '2': 'веранда дома',
                   '3': 'веранда бани', '4': 'другое'}
        polls[callback.message.chat.id] += f'Место размещения комплекса: {pol_txt[callback.data.split("d3")[-1]]}\n'
        for i in range(10):
            markup.add(types.InlineKeyboardButton(text=f'{i}', callback_data=f'd5{i}'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'd5' in callback.data:
        square = ''.join(callback.message.text.split(':')[-1]).split('м')[0].strip()
        for i in range(10):
            markup.add(types.InlineKeyboardButton(text=f'{i}', callback_data=f'd5{i}'))
        markup.add(types.InlineKeyboardButton(text='Ввод окончен', callback_data='d4'))
        square = square + callback.data.split('d5')[-1] if square != '0' else callback.data.split('d5')[-1]
        text = ''.join(callback.message.text.split(':')[0]) + f': {square} м.'
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'd4' in callback.data:
        text = msg_text.DGroup().d4()
        pol_txt = callback.message.text.split(':')[-1]
        polls[callback.message.chat.id] += f'Какова общая длина комплекса: {pol_txt} м.\n'
        markup.add(types.InlineKeyboardButton(text='аккуратная кирпичная кладка', callback_data='D6'))
        markup.add(types.InlineKeyboardButton(text='изразцы', callback_data='D_last_1__1'))
        markup.add(types.InlineKeyboardButton(text='другое', callback_data='D_last_1__2'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)
    elif 'D6' in callback.data:
        text = msg_text.DGroup().d6()
        polls[callback.message.chat.id] += f'Варианты отделки: аккуратная кирпичная кладка\n'

        markup.add(types.InlineKeyboardButton(text='стандартный кирпич с гладкой поверхностью (красный, коричневый, бежевый)',
                                              callback_data='D_last_2__1'))
        markup.add(types.InlineKeyboardButton(text='кирпич ручной формовки уменьшенного формата.', callback_data='D_last_2__2'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: 'E' in callback.data and 'last' not in callback.data)
async def group_E(callback):

    text = eval(f'msg_text.EGroup().{callback.data.lower().split("_")[-1]}()') if 'radio' not in callback.data else msg_text.EGroup().e1()
    markup = types.InlineKeyboardMarkup()
    flag_for_list_polls[callback.message.chat.id] = True
    main_pol[callback.message.chat.id] = ''
    if 'E1' in callback.data:

        stoves = ['Печь для отопления дома', 'Печь для бани', 'Камин',
                  'Комплекс барбекю', 'Другое']
        for stove in stoves:
            markup.add(types.InlineKeyboardButton(text=stove, callback_data=f'E_radio_{stove}'))

        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)

    elif 'radio' in callback.data:

        list_of_polls[callback.message.chat.id] = list_of_polls.get(callback.message.chat.id, []) + [callback.data.split('_')[-1]]
        stoves = ['Печь для отопления дома', 'Печь для бани',
                  'Камин', 'Комплекс барбекю', 'Другое']
        for stove in stoves:
            if stove in list_of_polls[callback.message.chat.id]:
                markup.add(types.InlineKeyboardButton(text=f'\u2705 {stove}', callback_data=f'E_radio_{stove}'))
            else:
                markup.add(types.InlineKeyboardButton(text=stove, callback_data=f'E_radio_{stove}'))
        text = callback.message.text.split(':')[-1]
        if not text.strip():
            text += callback.data.split('_')[-1] + '.'
        elif callback.data.split('_')[-1] not in text.split('.')[0]:

            text = text.split('.')[0] + ', ' + callback.data.split('_')[-1] + '.'
        text = callback.message.text.split(':')[0] + ':' + text
        markup.add(types.InlineKeyboardButton(text='Выбор окончен', callback_data='E_last'))
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: 'last' in callback.data)
async def group_last(callback):
    text = msg_text.LastGroup().last_1()
    if 'A' in callback.data:
        pol_txt = {'1': 'да', '2': 'нет', '3': 'нужна консультация печника'}
        polls[callback.message.chat.id] += f'Сделан ли фундамент для печи: {pol_txt[callback.data.split("__")[-1]]}\n'
    elif 'B' in callback.data:
        pol_txt = {'1': 'да', '2': 'нет'}
        polls[callback.message.chat.id] += f'Сделан ли фундамент для печи?: {pol_txt[callback.data.split("__")[-1]]}\n'
    elif 'C' in callback.data:
        pol_txt = {'1': 'просто аккуратная кирпичная кладка', '2': 'изразцы',
                   '3': 'камень', '4': 'пока выбираем, советуемся с дизайнером'}
        polls[callback.message.chat.id] += f'Варианты отделки камина: {pol_txt[callback.data.split("__")[-1]]}\n'
    elif 'D' in callback.data:
        if '1' in callback.data:
            pol_txt = {'1': 'изразцы', '2': 'другое'}
            polls[callback.message.chat.id] += f'Варианты отделки: {pol_txt[callback.data.split("__")[-1]]}\n'
        elif '2' in callback.data:
            pol_txt = {'1': 'стандартный кирпич с гладкой поверхностью (красный, коричневый, бежевый)',
                       '2': 'кирпич ручной формовки уменьшенного формата.'}
            polls[callback.message.chat.id] += f'Варианты кирпичной кладки: {pol_txt[callback.data.split("__")[-1]]}\n'
    elif 'E' in callback.data:
        text = 'Начните заполнять заказы\nНажмите кнопку "Далее", для того тобы начать'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(text='Далее'))
    elif 'F' in callback.data:

        polls[callback.message.chat.id] = f'Пользователь: {names[callback.message.chat.id]}\n' \
                                          f'Юзернейм: @{usernames[callback.message.chat.id]}\n' \
                                          f'Что интересует: Другое\n'
    flag_for_last1[callback.message.chat.id] = True
    if 'E' not in callback.data:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(text='Портфолио'))
        markup.add(types.KeyboardButton(text='Наш канал'))
        markup.add(types.KeyboardButton(text='Связаться с нами'))
        markup.add(types.KeyboardButton(text=f'Наш сайт'))
        markup.add(types.KeyboardButton(text='<< Назад'))

    await bot.delete_message(chat_id=msg_for_delete[callback.message.chat.id].chat.id,
                             message_id=msg_for_delete[callback.message.chat.id].id)
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
    await bot.send_message(chat_id=callback.message.chat.id, text=text, reply_markup=markup, parse_mode='html')


@bot.callback_query_handler(func=lambda callback: callback.data == 'Questionnaire')
async def init_questionnaire(callback):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
    await products(callback.message)


async def main():
    await asyncio.gather(bot.polling(
                                    interval=1,
                                    non_stop=True,
                                    request_timeout=1000,
                                    timeout=1000
                                    ))


if __name__ == '__main__':
    asyncio.run(main())