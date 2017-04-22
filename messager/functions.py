'''import vk
import time
def get_user_dialogs(token):
    MAIN_ARRAY = []
    users_array = []
    bodys_array = []

    session = vk.Session(access_token = token)
    vkapi = vk.API(session, v = '5.63')
    mas = vkapi.messages.getDialogs(count = 10)
    array = mas['items']

    for i in array:
        users_array.append(i['message']['user_id'])
        bodys_array.append(i['message']['body'])

    usernames = []
    userfotos = []

    for i in users_array:
        my_id = str(i)
        user = vkapi.users.get(user_ids = my_id, fields = 'photo_50')
        name = user[0]['first_name'] + ' ' + user[0]['last_name']
        image = user[0]['photo_50']
        time.sleep(0.3)
        usernames.append(name)
        userfotos.append(image)

    MAIN_ARRAY.append(usernames)
    MAIN_ARRAY.append(userfotos)
    MAIN_ARRAY.append(bodys_array)

    return MAIN_ARRAY'''

print(len("Здравствуйте, если вы изучаете python и увлекаетесь програм"))
b = { '11': 'Andrew' }
if 'name' in b:
    print('COOL')
else:
    print("FUCK")
