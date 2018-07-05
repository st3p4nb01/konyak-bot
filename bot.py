import re
import random
import vk_api
import datetime
import math
import time
ADMIN_ID = 154845243

print('Запуск бота..')

login, password = '+79150029295', 'konkovnelubitanal777'
vk_session = vk_api.VkApi(login, password)
try:
    vk_session.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)
vk = vk_session.get_api()

print('Бот авторизован.')


now = datetime.datetime.now()
if math.fmod(datetime.date(now.year, now.month, now.day).isocalendar()[1], 2) != 0: week = 1
else: week = 2
 
values = {'out': 0, 'count': 1, 'time_offset': 60, 'peer_id': 2000000002, 'start_messages_id' : int()}
chat_ident = 2
chat_name = vk.messages.getChat(chat_id=chat_ident)
chat_users = vk.messages.getChatUsers(chat_id=chat_ident)

def remove_user(chat_id, user_id):
    vk.messages.removeChatUser(chat_id=chat_id, user_id=user_id)

def create_chat(title):
    vk.messages.createChat(title=title)
	
def send_sticker(chat_id, sticker_id):
    vk.messages.sendSticker(chat_id=chat_id, sticker_id=sticker_id)
 
def send_photo(chat_id, message, attachment):
    vk.messages.send(chat_id=chat_id, message=message, attachment=attachment)
 
def write_msg(chat_id, message):
    vk.messages.send(chat_id=chat_id, message=message)
 
def chat_change(chat_id, title):
    vk.messages.editChat(chat_id=chat_id, title=title)
 
def random_chat(chat_id):
    id = random.choice(vk.messages.getChatUsers(chat_id=chat_id))
    vk.messages.send(chat_id=chat_id, message=str(vk.users.get(user_ids=id)[0]['first_name']) + ' ' +
                                              str(vk.users.get(user_ids=id)[0]['last_name']) + ' - сегодня лох.' )
 
while True:
    response = vk.messages.getHistory(out=values['out'], count=values['count'], peer_id=values['peer_id'], time_offset=values['time_offset'],
                               start_messages_id=values['start_messages_id'])
    if response['items']:
        values['start_messages_id'] = response['items'][0]['id']
    for item in response['items']:
        if response['items'][0]['body'] == '!cmd':
            write_msg(item['chat_id'],'Комнады бота &#129302;\n\n[Команды для холопов]\n\n!infme – Узнать информацию о себе\n!me [Действие] – Выполнить какое-либо действие\n!лох – Узнать кто сегодня лох\n!leave [Причина] – Покинуть беседу\n\n[Команды для админов]\n\n!title [Название] – Изменить название беседы\n!clear – Очистить чат\n!отпиздить [Кого?] – Кого-то отпидзить\n\n[Прочие команды]\n\n!binfo – Узнать информацию о боте\n!дата – Узнать сегодняшнюю дату\n!беседа – Узнать информацию о беседе')
        if response['items'][0]['body'][0:10] == '!отпиздить' and response['items'][0]['user_id'] == ADMIN_ID:
            write_msg(item['chat_id'], 'Слышь,'+ response['items'][0]['body'][10:] + ', щас будем пиздить тебя')
            write_msg(item['chat_id'], 'Так что, готовь ебальник')
            time.sleep(2)
            write_msg(item['chat_id'], 'Тааааа!!!')
            time.sleep(2)
            write_msg(item['chat_id'], 'Шаааа!!!')
            send_sticker(item['chat_id'], 2166)
            write_msg(item['chat_id'], 'Бля мужык упал!!!')
            time.sleep(2)
            write_msg(item['chat_id'], 'Нехуй,' + response['items'][0]['body'][10:] + ' было выёбываться')
        elif response['items'][0]['body'][0:10] == '!отпиздить' and response['items'][0]['user_id'] != ADMIN_ID:
        	write_msg(item['chat_id'], 'Хочешь чтобы тебя отпиздили?')
        elif response['items'][0]['body'] == '!беседа':
            write_msg(item['chat_id'], 'Информация о беседе: [id' + str(item['chat_id'])+ ']' + '\nКоличество участников в беседе: ' + 'None')
        elif response['items'][0]['body'][0:5] == '!chat':
            create_chat(response['items'][0]['body'][5:])
        elif response ['items'][0]['body'] == 'photo':
            send_photo(item['chat_id'], 'Кажись, работает.' ,'photo154845243_456242192')
        elif response['items'][0]['body'] == '!дата':
            write_msg(item['chat_id'], 'Сегодняшняя дата: ' + str(now.day) + '.' + str(now.month) + '.' + str(now.year))
        elif response['items'][0]['body'] == '!лох':
            random_chat(item['chat_id'])
        elif re.match('!me ', response['items'][0]['body']):
            write_msg(item[u'chat_id'], vk.users.get(user_ids=response['items'][0]['user_id'])[0]['first_name'] + ' ' +
                      vk.users.get(user_ids=response['items'][0]['user_id'])[0]['last_name'] + ': ' +
                      response['items'][0]['body'].replace('!me ', ''))
        elif response ['items'][0]['body'] == '!infme':
            write_msg(item['chat_id'], 'Имя: ' +  vk.users.get(user_ids=response['items'][0]['user_id'])[0]['first_name'] + '\nФамилия: ' +
       	         	 vk.users.get(user_ids=response['items'][0]['user_id'])[0]['last_name'])
        elif response['items'][0]['body'][0:6] == '!title' and response['items'][0]['user_id'] == ADMIN_ID:
            chat_change(item['chat_id'], response ['items'][0]['body'][6:])
        if response ['items'][0]['body'][0:6] == '!title' and response['items'][0]['user_id'] != ADMIN_ID:
        	write_msg(item['chat_id'], 'Недостаточно прав.')
        elif response['items'][0]['body'] == '!binfo':
            write_msg(item['chat_id'], 'Информация о боте:\n\nСоздатель бота: [id154845243|Степан&#128100;]\nВерсия бота: Python 3.7.0\nБот создан: 14.06.18')
        elif re.match('!kick', response['items'][0]['body']) and response['items'][0]['user_id'] == ADMIN_ID:
            vk.messages.removeChatUser(chat_id=item['chat_id'], user_id=response['items'][0]['fwd_messages'][0]['user_id'])
        elif response['items'][0]['body'] == '!clear' and response['items'][0]['user_id'] == ADMIN_ID:
            write_msg(item['chat_id'], '&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n' )
            time.sleep(1)
            write_msg(item['chat_id'], 'Очищено &#9989;')
			
          
        elif re.match('!leave', response['items'][0]['body']):
            vk.messages.removeChatUser(chat_id=item['chat_id'],user_id=response['items'][0]['user_id'])
            if response['items'][0]['body'].replace('!leave', '').strip() == '':
                write_msg(item['chat_id'], vk.users.get(user_ids=response['items'][0]['user_id'])[0]['first_name'] + ' ' +
                      vk.users.get(user_ids=response['items'][0]['user_id'])[0]['last_name'] + ' ушёл без причины')
            else:
                write_msg(item['chat_id'], vk.users.get(user_ids=response['items'][0]['user_id'])[0]['first_name'] + ' ' +
                      vk.users.get(user_ids=response['items'][0]['user_id'])[0]['last_name'] + ' ушёл от нас по причине: ' +
                      response['items'][0]['body'].replace('!leave', ''))