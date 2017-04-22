from django.shortcuts import render
from django.utils import timezone
import time
import json
import vk
from django.http import HttpResponse
from django.shortcuts import redirect

LOGGED = False
ERRORS = []
ON_PAGE = 'home'
def logged_token(a):
    global LOGGED
    if 'token' in a:
        LOGGED = True
    else:
        LOGGED = False

    return LOGGED

# Create your views here.
def home(request):
    global ON_PAGE
    global ERRORS
    global LOGGED
    logged_token(request.session)
    logged_array = []
    if LOGGED == True:
        token = request.session['token']
        ses = vk.Session(access_token = token)
        vkapi = vk.API(ses, v = '5.63')
        log = vkapi.users.get(fields = 'photo_50')
        logged_array.append(log[0]['first_name'])
        logged_array.append(log[0]['photo_50'])
        return redirect('get_dialogs')
    else:
        logged_array.append("empty")

    ON_PAGE = 'home'

    return render(request, 'messager/token.html', { 'logged': logged_array, 'errors': ERRORS, 'page': ON_PAGE })

def get_dialogs(request):
    global ON_PAGE
    global ERRORS
    global LOGGED
    try:
        if 'token' in request.POST or 'token' in request.session:
            if 'token' in request.POST:
                token = request.POST['token']
            elif 'token' in request.session:
                token = request.session['token']

            users_array = []
            bodys_array = []

            ses = vk.Session(access_token = token)
            vkapi = vk.API(ses, v = '5.63')
            mas = vkapi.messages.getDialogs(count = 10)

            if len(mas) > 0:
                request.session['token'] = token

            array = mas['items']

            for i in array:
                users_array.append(i['message']['user_id'])
                body = str(i['message']['body'])
                if len(body) > 55:
                    bodys_array.append(body[0:55] + "..")
                elif body == '':
                    bodys_array.append("(Фотография, стикер, пересланное сообщение)")
                else:
                    bodys_array.append(body)

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

            logged_token(request.session)
            logged_array = []
            if LOGGED == True:
                log = vkapi.users.get(fields = 'photo_50')
                logged_array.append(log[0]['first_name'])
                logged_array.append(log[0]['photo_50'])
            else:
                logged_array.append("empty")

            ERRORS.clear()
            ON_PAGE = 'dialogs'

            return render(request, 'messager/all_messages.html', { 'users': usernames, 'images': userfotos, 'text': bodys_array, 'logged': logged_array, 'users_id': users_array, 'page': ON_PAGE })
        else:
            return render(request, 'messager/token.html', {})

    except:
        ERRORS.append("error!")
        return redirect('home')

def logout(request):
    try:
        del request.session['token']
        return redirect('home')
    except:
        return redirect('home')

def dialog(request, us_id):
    global ON_PAGE
    global LOGGED

    ses = vk.Session(access_token = request.session['token'])
    vkapi = vk.API(ses, v = '5.63')

    users_id = []
    mas_array = []
    date_array = []

    messages = vkapi.messages.getHistory(user_id = us_id, count = 80)
    massages_array = messages['items']
    for i in massages_array:
        users_id.append(i['from_id'])
        if i['body'] == '':
            mas_array.append("(Фотография, стикер, пересланное сообщение)")
        else:
            mas_array.append(i['body'])
        date_array.append(time.strftime('%d.%m %H:%M', time.localtime(i['date'])))

    usernames = []
    userfotos = []
    for i in users_id:
        user = vkapi.users.get(user_ids = i, fields = 'photo_50')
        time.sleep(0.3)
        usernames.append(user[0]['first_name'])
        userfotos.append(user[0]['photo_50'])

    logged_token(request.session)
    logged_array = []
    if LOGGED == True:
        token = request.session['token']
        ses = vk.Session(access_token = token)
        vkapi = vk.API(ses, v = '5.63')
        log = vkapi.users.get(fields = 'photo_50')
        logged_array.append(log[0]['first_name'])
        logged_array.append(log[0]['photo_50'])
    else:
        logged_array.append("empty")

    ON_PAGE = 'mess'
    friend_id = us_id

    return render(request, 'messager/user_mess.html', { 'users': usernames, 'images': userfotos, 'text': mas_array, 'date': date_array, 'logged': logged_array, 'page': ON_PAGE, 'need_id': friend_id })

def get_foto(request, fr_id):
    global LOGGED
    global ON_PAGE

    ses = vk.Session(access_token = request.session['token'])
    vkapi = vk.API(ses, v = '5.63')

    photos = vkapi.messages.getHistoryAttachments(peer_id = fr_id, media_type = 'photo', count = 20)
    ar = photos['items']
    mini_foto = []
    big_foto = []
    for i in ar:
        mini_foto.append(i['attachment']['photo']['photo_130'])
        if 'photo_807' in i['attachment']['photo']:
            big_foto.append(i['attachment']['photo']['photo_807'])
        elif 'photo_807' not in i['attachment']['photo']:
            big_foto.append(i['attachment']['photo']['photo_604'])
        else:
            big_foto.append(i['attachment']['photo']['photo_130'])

    user = vkapi.users.get(user_ids = fr_id)
    namus = str(user[0]['first_name']) + ' ' + str(user[0]['last_name'])

    logged_token(request.session)
    logged_array = []
    if LOGGED == True:
        token = request.session['token']
        ses = vk.Session(access_token = token)
        vkapi = vk.API(ses, v = '5.63')
        log = vkapi.users.get(fields = 'photo_50')
        logged_array.append(log[0]['first_name'])
        logged_array.append(log[0]['photo_50'])
    else:
        logged_array.append("empty")

    ON_PAGE = 'photo'
    return render(request, 'messager/photos.html', { 'page': ON_PAGE, 'need_id': fr_id, 'logged': logged_array, 'mini_foto': mini_foto, 'big_foto': big_foto, 'name': namus })

STATUS = []
def set_status(request):
    global STATUS
    global ON_PAGE
    global LOGGED
    STATUS.clear()
    logged_token(request.session)
    logged_array = []
    if LOGGED == True:
        token = request.session['token']
        ses = vk.Session(access_token = token)
        vkapi = vk.API(ses, v = '5.63')
        log = vkapi.users.get(fields = 'photo_50')
        logged_array.append(log[0]['first_name'])
        logged_array.append(log[0]['photo_50'])
    else:
        logged_array.append("empty")

    if 'answer' in request.session:
        STATUS.append(request.session['answer'])
        del request.session['answer']

    ON_PAGE = 'status'

    return render(request, 'messager/status.html', { 'logged': logged_array, 'page': ON_PAGE, 'status': STATUS })

def sprocess(request):
    global STATUS
    token = request.session['token']
    ses = vk.Session(access_token = token)
    vkapi = vk.API(ses, v = '5.63')
    if 'status' in request.POST:
        text = request.POST['status']
        new = vkapi.status.set(text = text)
        if new == 1:
            answer = 'true'
            request.session['answer'] = answer
        else:
            answer = 'false'
            request.session['answer'] = answer
    else:
        answer = 'false'
        request.session['answer'] = answer
    return redirect('set_status')
