import abc


class BaseMessages(abc.ABC):
    @abc.abstractmethod
    def start(self, name=None):
        raise NotImplemented


class AdminUser(BaseMessages):
    def __init__(self):
        self.admin_password_flag = {}
        self.admin_stop_msg = {}

    def start(self, name=None):
        text = f'Добро пожаловать, {name}. Вы вошли в аккаунт администратора\n' \
               f'Вы можете создать рассылки для всех пользователей, присылая нам медиафайлы, текст и другие сообщения.\n' \
               f'Как закончите, нажмите кнопка "<< Назад"'
        return text

    def password_false(self):
        text = f'Пароль введен неверно, попробуйте еще раз'
        return text

    def write_down_password(self):
        text = 'Введите пароль, чтобы войти в качестве админа\n'
        return text


class RegularUser(BaseMessages):
    def __init__(self):
        self.flag_for_last1, self.flag_for_last2, self.polls = {}, {}, {}
        self.list_of_polls, self.flag_for_list_polls, self.main_pol = {}, {}, {}

    def start(self, name=None):
        text = f'Здравствуйте, это электронный помощник Артели печников «АРКА».' \
               f' Мы базируемся в г. Сергиев Посад Московской области и профессионально занимаемся строительством' \
               f' печей, каминов и комплексов барбекю из кирпича. Как Вас зовут?'
        return text

    def forgot_user(self):
        text = 'Мы вас забыли, такое могло случиться, если бот был перезапущен\n' \
               'Нажмите кнопку "/start" и авторизируйтесь снова!'
        return text

    def unknown(self):
        text = 'Извините, в рамках нашего общения мы приняли Вашу заявку и в ближайшее время свяжемся с Вами.' \
               ' Если у Вас возник срочный вопрос, то, пожалуйста, позвоните по номеру +79260539539 или  задайте' \
               ' свой вопрос в  @arka_pechnik. А если Вы хотите снова пройти опрос, то нажмите "Опросник"'
        return text

    def portfolio(self):
        text = 'Ознакомьтесь с нашим портфолио'
        return text

    def contact(self):
        text = 'Наши контакты:\n' \
               '+7 926 053 95 39'
        return text

    def products(self, name):
        text = f'Что именно вас интересует, {name}?'
        return text

    def channel(self):
        text = 'Переходите в наш канал'
        return text

    def site(self):
        text = f'Ознакомьтесь с нашим сайтом. На нем представлено больше информации'
        return text

    def answers(self):
        text = 'Если у вас возникли вопросы, внизу появились кнопки - воспользуйтесь ими '
        return text


class AGroup:
    def a1(self):
        text = 'В скольких комнатах/помещениях дома будет расположена печь?'
        return text

    def a2(self):
        text = 'Какова общая площадь помещений, которые требуется отопить этой печью?\n' \
                'Площадь: 0 кв. м.'
        return text

    def a3(self):
        text = 'Вид и функционал печи'
        return text

    def a4(self):
        text = 'Печь нужна как:'
        return text

    def a5(self):
        text = 'Дом уже построен?'
        return text

    def a6(self):
        text = 'Сделан ли фундамент для печи?'
        return text


class BGroup:
    def b1(self):
        text = 'Имея опыт в строительстве банных печей, мы рекомендуем рассмотреть два варианта:\n\n' \
               '1. Кирпичная печь-каменка с закладкой из чугуна – классика русской бани. Примерная стоимость' \
               ' «под ключ» 700-900 т.рублей.\n\n' \
               '2. Металлическая печь, совмещённая с отопительным щитком из кирпича – более бюджетный выбор.' \
               'Примерная стоимость «под ключ» 350-450 т.рублей.'

        return text

    def b2(self):
        text = 'Тип бани, где нужно сложить печь:'
        return text

    def b3(self):
        text = 'Площадь помещения парной: 0 кв. м.'
        return text

    def b4(self):
        text = 'Из какого материала построена баня?'
        return text

    def b5(self):
        text = 'Сделан ли фундамент для печи?'
        return text


class CGroup:
    def c1(self):
        text = 'Камин является украшением интерьера, очагом, обладающим притягательной силой,' \
               ' но в качестве источника тепла имеет весьма скромные способности. Поэтому наряду' \
               ' с классическим камином с открытой топкой предлагаем Вам рассмотреть вариант каминопечи.\n' \
               'Каминопечь может эксплуатироваться в двух режимах – и как камин, и как полноценная печь,' \
               ' отапливающая помещение.\n\n' \
               'Введите площадь помещения, где планируется разместить камин.\n' \
               'Площадь: 0 кв. м.'
        return text

    def c2(self):
        text = 'Высота потолка в этом помещении:\n' \
               '0 м.'
        return text

    def c3(self):
        text = 'Варианты отделки камина:'
        return text


class DGroup:
    def __init__(self):
        self.focies = {}

    def d1(self):
        text = 'Какие очаги и элементы Вы выбираете? \n' \
                'Ваш выбор: '
        return text

    def d2(self):
        text = 'Место размещения комплекса:'
        return text

    def d3(self):
        text = 'Какова общая длина комплекса: 0 м.'

        return text

    def d4(self):
        text = 'Варианты отделки:'
        return text

    def d6(self):
        text = 'Варианты:'
        return text


class EGroup:
    def e1(self):
        text = 'Мне нужны: '
        return text

    def another_btn_chosen(self):
        text = 'Данная категория не была добавлена к заказу.\nДля того, чтобы выбрать сразу несколько категорий,' \
                                 'нажмите кнопку "Несколько печей"'
        return text

    def not_all_filled(self):
        text = 'Вы заполнили не все заказы, нажмите "Далеe", чтобы закончить'
        return text


class LastGroup:
    def last_1(self):
        text = 'В каком районе расположен Ваш дом (или: в каком районе планируете строительство?)'
        return text

    def last_2(self):
        text = 'Когда Вы планируете приступить к строительству печи?'
        return text

    def last_buy(self, chat_id, names):
        text = f'Большое спасибо Вам за обращение, {names[chat_id]}, в скором времени мы с вами свяжемся. '
        return text


admin = AdminUser()
reg_user = RegularUser()
group_a = AGroup()
group_b = BGroup()
group_c = CGroup()
group_d = DGroup()
group_e = EGroup()
group_last = LastGroup()
