#connecting to database-------------------------------------------------------------------------------------
from pickle import NONE
from time import sleep
import numpy as np
import os
file_path1 = os.path.abspath('/var/telegrambot/database')
import sys
sys.path.append(file_path1)
from db import DB
db = DB()
mycursor=db.get_cursor()
db.get_commit()





#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#ایجاد فایل .env و خواندن بخشی از اطلاعات از روی آن
import dotenv
from dotenv import dotenv_values
import os
import pandas as pd 

filename = os.path.basename(__file__)
path = str(__file__).replace(filename, '')
env = dotenv_values(path + '.env')




#-------------------------------------------------------------------------------------
# تعریف تابع لاگ
from os import path
filename = path.basename(__file__)
file_path = str(__file__).replace(filename, '')


def add_log(msg, log_type='Error'):
    with open(file_path + 'error-holoo-gate-api.log', 'a') as file:
        file.write( log_type + ': ' + msg + '\n')
        
        
add_log(str(mycursor), log_type="mycursor")

#-------------------------------------------------------------------------------------
#فراخوانی کتابخانه های مورد نیاز
from flask import Flask
from flask import request
from flask import Response
import requests
import json
import numpy as np 
import base64
import qrcode
import requests
from io import BytesIO

#-------------------------------------------------------------------------------------
#ست کردن توکن تلگرام
# TOKEN = "6524694661:AAH1YrHD9yPMqwrBu6yG88TPJvXFKMg0QVo"
TOKEN = env['TOKEN']
#------------------------------------------------------------------------------------- 
#------------------------------------------------------------------------------------- 
#شروع فریموورک فلاسک 
app = Flask(__name__)

#تجزیه یک  پیام و استخراج اطلاعات مهم از آن  
def tel_parse_message(message):
    print("message-->",message)
    try:
        chat_id = message['message']['chat']['id']
        txt = message['message']['text']
        # username = message['message']['chat']['username']
        print("chat_id-->", chat_id)
        print("txt-->", txt)
        # print("username-->", username)
 
        return chat_id,txt
    except:
        print("NO text found-->>")

#تجزیه یک پیام و استخراج اطلاعات خاص مربوط به فایل
def tel_parse_get_message(message):
    print("message-->",message)
   
    try:
        g_chat_id = message['message']['chat']['id']
        g_file_id = message['message']['photo'][0]['file_id']
        print("g_chat_id-->", g_chat_id)
        print("g_image_id-->", g_file_id)
 
        return g_chat_id,g_file_id
    except:
        try:
            g_chat_id = message['message']['chat']['id']
            g_file_id = message['message']['video']['file_id']
            print("g_chat_id-->", g_chat_id)
            print("g_video_id-->", g_file_id)
 
            return g_chat_id,g_file_id
        except:
            try:
                g_chat_id = message['message']['chat']['id']
                g_file_id = message['message']['audio']['file_id']
                print("g_chat_id-->", g_chat_id)
                print("g_audio_id-->", g_file_id)
 
                return g_chat_id,g_file_id
            except:
                try:
                    g_chat_id = message['message']['chat']['id']
                    g_file_id = message['message']['document']['file_id']
                    print("g_chat_id-->", g_chat_id)
                    print("g_file_id-->", g_file_id)
 
                    return g_chat_id,g_file_id
                except:
                    print("NO file found found-->>")
 
#ارسال پیام به یک چت مشخص شده با استفاده از API ربات تلگرام
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
 
    return r
 
#ارسال تصویر به یک چت مشخص شده با استفاده از API ربات تلگرام 
def tel_send_image(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': "https://hologate2.plus/price",
        'caption': "This is a price list"
    }
 
    r = requests.post(url, json=payload)
    return r

#ارسال فایل صوتی به چت مشخص شده با استفاده از API ربات تلگرام
def tel_send_audio(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendAudio'
 
    payload = {
        'chat_id': chat_id,
        "audio": "http://www.largesound.com/ashborytour/sound/brobob.mp3",
 
    }
 
    r = requests.post(url, json=payload)
 
    return r

#ارسال یک فایل ویدئویی به چت مشخص شده با استفاده از API ربات تلگرام
def tel_send_video(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendVideo'
 
    payload = {
        'chat_id': chat_id,
        "video": "https://www.appsloveworld.com/wp-content/uploads/2018/10/640.mp4",
 
    }
 
    r = requests.post(url, json=payload)
 
    return r

#ارسال فایل سند به چت مشخص شده با استفاده از API ربات تلگرام
def tel_send_document(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'
 
    payload = {
        'chat_id': chat_id,
        "document": "http://www.africau.edu/images/default/sample.pdf",
 
    }
 
    r = requests.post(url, json=payload)
 
    return r


#ارسال نظرسنجی به یک چت مشخص ز 
def tel_send_poll(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPoll'
    payload = {
        'chat_id': chat_id,
        "question": "خورشید از کدام جهت طلوع می کند؟",
        "options": json.dumps(["شمال", "جنوب", "شرق", "غرب"]),
        "is_anonymous": False,
        "type": "quiz",
        "correct_option_id": 2
    }
 
    r = requests.post(url, json=payload)
 
    return r


#----------------------------------------------------------------
#وقتی استارت را میزند این دکمه نمایش داده می شود.

def start_send_button(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    buttons = [
        [{'text': 'نرم افزارهای لازم 📲'}, {'text': 'پشتیبانی 🙋‍♀️'}],
        [{'text': 'پرداخت وجه 💰'}, {'text': 'اکانت تست 🆓'}],
        [{'text': 'مدیریت اشتراک ها 🔒'},{'text': 'قیمت خدمات 💸'}],
        [{'text': 'خرید اشتراک 🛒'}]
    ]
    
    keyboard = {
        'keyboard': buttons,
        'resize_keyboard': True,
        'one_time_keyboard': True
    }

    payload = {
        'chat_id': chat_id,
        'text': '🤖به ربات فیلتر شکن هلوگیت خوش آمدید\n\n-✨بهترین کیفیت با کمترین میزان قطعی و رضایت بالای کاربران\n\n-🚀ارائه سرویس های SSH و V2ray با لوکیشن های مختلف از سراسر جهان\n\n-🌈امکان تغییر سرور و نوع کانکشن توسط کاربر\n\n\nبا استفاده از دکمه های زیر، اکانت تست رایگان دو روزه دریافت کرده و اشتراک جدید خریداری و یا اشتراک فعلی خود را تمدید نمایید',
        'reply_markup': keyboard
    }

    r = requests.post(url, json=payload)

    return r

#-------------------------------------------------------------------------------------------------
#وقتی روی دکمه ی قیمت خدمات کلیک می کند این دکمه ها ارسال می شود.
def  SendPrice(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    buttons = [
        [{'text': '1 ماهه 2 دلار 🟢'}, {'text': '3 ماهه 5 دلار 🟢'}],
        [{'text': '6 ماهه 10 دلار 🟢'}, {'text': '1 ساله 18 دلار 🟢'}],
        [{'text': 'پشتیبانی 🙋‍♀️'}, {'text': 'صفحه 1 📄'}]
    ]  

    
    keyboard = {
        'keyboard': buttons,
        'resize_keyboard': True,
        'one_time_keyboard': True
    }

    payload = {
        'chat_id': chat_id,
        'text': 'برای خرید اشتراک هلوگیت، ابتدا مدت زمان کانکشن خود را انتخاب نمایید؛\nتمامی اشتراک ها 2 کاربره با ترافیک نامحدود هستند.',
        'reply_markup': keyboard
    }

    r = requests.post(url, json=payload)

    return r

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#وقتی روی دکمه ی پشتیبانی کلیک می کند ای دکمه ها برمیگردد
def support(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'


    buttons = [
        [{'text': 'قیمت خدمات 💸'}, {'text': 'چت با کارشناس 💬'}],
        [{'text': 'سئوالات متداول ❓'}, {'text': 'صفحه 1 📄'}]
    ]

    
    keyboard = {
        'keyboard': buttons,
        'resize_keyboard': True,
        'one_time_keyboard': True
    }

    payload = {
        'chat_id': chat_id,
        'text': 'لطفا سئوالات متداول را مطالعه کنید و چنانچه پاسخ خود را دریافت نکردید به کارشناسان ما پیام دهید لازم به ذکر است زمان پاسخگوئی از ساعت 9 صبح لغایت 4 بعد از ظهر می باشد.  ',
        'reply_markup': keyboard
    }

    r = requests.post(url, json=payload)

    return r
#----------------------------------------------------------------------------------------------------
def peyment_log_received(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
 
    payload = {
        'chat_id': chat_id,
        'text': "لطفا اطلاعات واریزی خود را از طریق لینک ذیل ارسال کنید تا بررسی و اشتراک شما تحویل گردد.  ",
                'reply_markup': {'keyboard': [[{'text': 'سئوالات متداول'}, {'text': 'چت با کارشناس'},{'text': ' صفحه 1'}]]}
    }
 
    r = requests.post(url, json=payload)
 
    return r


def tel_send_inlinebutton(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
 
    payload = {
        'chat_id': chat_id,
        'text': "گزینه مورد نظر را انتخاب کنید",
        'reply_markup': {
            "inline_keyboard": [[
                {
                    "text": "سایت",
                    "callback_data": "site"
                },
                {
                    "text": "ربات",
                    "callback_data": "bot"
                }]
            ]
        }
    }
    r = requests.post(url, json=payload)
    return r

def support_id(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
 
    payload = {
        'chat_id': chat_id,
                'text': "https://t.me/hologate5" 
        
    }
    r = requests.post(url, json=payload)
    return r

def payment_tron(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    
    payload = {
        'chat_id': chat_id,
                'text': " هلوگیت از طریق درگاه آنلاین پرداخت رمز ارزی را انجام می دهد و برای پرداخت با ترون یا تتر شما می توانید وارد فروشگاه هلوگیت شوید و در قسمت خرید اشتراک گزینه پرداخت با رمز ارز را انتخاب کنید. https://hologate2.plus/shop "
                #'text': "https://t.me/hologate5" 
            
    }
    r = requests.post(url, json=payload)
    return r


def tel_upload_file(file_id):
    url = f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}'
    a = requests.post(url)
    json_resp = json.loads(a.content)
    print("a-->",a)
    print("json_resp-->",json_resp)
    file_pathh = json_resp['result']['file_path']
    print("file_path-->", file_pathh)
   
    url_1 = f'https://api.telegram.org/file/bot{TOKEN}/{file_pathh}'
    b = requests.get(url_1)
    file_content = b.content
    with open("/home/bot/" + file_pathh, "wb") as f:
        f.write(file_content)
  
  
  

# ------------------------------------------------------------------------------------------------
user_email = None  # Global variable to store user email


#------------------------------------------------------------------------------------------------------------
#پس ار زدن دکمه ی مدیریت اشتراک ها، وارد این تابع میشود
def login(chat_id):
    chat_id = chat_id
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    response = requests.post(env['account_management'] , data={'chat':str(chat_id)}, headers={'token':env['token']})
    #response = requests.post('http://136.243.86.140:81/api/account_management' ,  data={'chat':str(chat_id)}, headers={'token':'UGFGtZ.RkMfiqfy80O5EP0VoBiVrcs3GGcjJjGKAyr2UAxNtG'})
    add_log(str(response.content), log_type='account_management')
    if response.status_code == 200:
        
        # Parse the JSON response
        servers5 = response.json() 
#در صورتی که قبلا کاربر لاگین نکرده باشد از او خواسته می شود که از طریق لینک ارسالی لاگین کرده و سپس مدیریت اشتراک ها را بفشارد.
        if "code" in servers5:
            # tel_send_message(chat_id, str(servers5))
            linker = servers5["message"]
                
            link = [
            "وارد لینک زیر شده و پس از ورود موفق، جهت مدیریت اشتراک ها و دریافت لیست اکانت ها مجددا همین جا دکمه ی مدیریت اشتراک ها را بفشارید.",
            f"{linker}"
            ]
                    
                    
                    
            for i in link:
                payload = {
                    'chat_id': chat_id,
                    'text': i
                }
                    

                r = requests.post(url, json=payload)
#در صورتی که کاربر پیش ازین لاگین کرده باشد :

        else:
#اگر کاربر هیچ اکانتی نداشته باشد پیام زیر چاپ می شود
            if len(servers5["message"]["account"])==0:
                tel_send_message(chat_id, "شما هم اکنون هیچ اکانتی ندارید!")
#در صورتی که کاربر اکانتی داشته باشد، لیست اکانتهای موجود به صورت دکمه های اینلاین به او برمیگردد.     
            else:
                buttons=[]        
                # Iterate over the button names and create button objects
                for server in servers5["message"]["account"]:
                    button = {
                        "text": server["username"]+","+server["type"]+ " " + "🔒"+","+server["expiration_date"],
                        "callback_data": str(server["type"])+","+str(server["id"])
                    }

                    buttons.append([button])

                message = "اکانت مورد نظر را انتخاب نمایید:"
                keyboard=buttons
                response = send_inline_keyboard(chat_id, message, keyboard)
                if response["ok"]:
                    return "Inline keyboard sent successfully."
# در صورتی که سرور پاسخ ندهد یا استتوس آن 200 نباشد پیام زیر چاپ میشود.
    else:
        tel_send_message(chat_id, "Server Error!")



#------------------------------------------------------------------------------------------------------------
# #پس از زدن دکمه ی خرید اشتراک، وارد این تابع میشود

def buy(chat_id):

    chat_id = chat_id

#موجودی کیف پول کاربر در این بخش دریافت و دذخیره می شود
#-----------------------------------------------------------------------
    chat_id = chat_id
    response1 = requests.post(env['get-balance'] , data={'chat': str(chat_id)}, headers={'token':env['token']})
    #response1 = requests.post('http://136.243.86.140:81/api/get-balance', data={'chat': str(chat_id)}, headers={'token':'UGFGtZ.RkMfiqfy80O5EP0VoBiVrcs3GGcjJjGKAyr2UAxNtG'})
    add_log(str(response1.content), log_type='get-balance')
    if response1.status_code == 200:
        balance= response1.json() 
        balance= str(balance["message"])
    else:
        tel_send_message(chat_id, "Server Error!")
#---------------------------------------------------------------------


    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    response = requests.post(env['service-account'] , headers={'token':env['token']})
    #response = requests.post('http://136.243.86.140:81/api/service-account', headers={'token':'UGFGtZ.RkMfiqfy80O5EP0VoBiVrcs3GGcjJjGKAyr2UAxNtG'})
    add_log(str(response.content), log_type='service-account11')
    if response.status_code == 200:
        
        # Parse the JSON response
        buying_options = response.json() 
        # tel_send_message(chat_id, str(buying_options["data"][0]))
        buttons=[]        
        # Iterate over the button names and create button objects
        for option in buying_options["data"]:
            button = {
                "text": str(option["name"])+", "+str(option["number_of_devices"])+", نامحدود, "+str(option["price"])+ " 🔗",
                "callback_data": str(option["id"])+","+"buying_options&%@"
            }

            buttons.append([button])

        message = f"موجودی کیف پول شما {balance}$ می باشد؛گزینه مورد نظر خود را انتخاب نمایید:"
        keyboard=buttons
        response = send_inline_keyboard(chat_id, message, keyboard)
        if response["ok"]:
            return "Inline keyboard sent successfully."
    else:
        tel_send_message(chat_id, "Server Error!")


#---------------------------------------------------------------------------------------------------------------
#پس از دریافت ایمیل کاربر جهت دریاف اکانت تست، با این تابع لیست سرورهای تست به صورت اینلاین به کاربر نمایش داده می شود، یا پیام های مرتبط به او بازمیگردد.
def send2(chat_id, user_email):
    chat_id = chat_id
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

  
    response = requests.post(env['find-server-test'] , data={'email': user_email , 'chat':str(chat_id)}, headers={'token':env['token']})
    #response = requests.post('http://136.243.86.140:81/api/find-server-test' ,  data={'email': user_email , 'chat':str(chat_id)}, headers={'token':'UGFGtZ.RkMfiqfy80O5EP0VoBiVrcs3GGcjJjGKAyr2UAxNtG'})
    add_log(str(response.content), log_type='find-server-test2')
    if response.status_code == 200:
                
        # Parse the JSON response
        servers = response.json()
        buttons = []
 #درصورتی که قبلا اکانت تست خود را دریافت کرده باشد پیام زیر چاپ می شود.                  
        if "message1" in servers:   
                    
            payload = {
                'chat_id': chat_id,
                'text': str(servers['message1'])
            }
                    
                
            r = requests.post(url, json=payload)
        elif "message3" in servers:   
                    
            payload = {
                'chat_id': chat_id,
                'text': str(servers['message3'])
            }
                    
                
            r = requests.post(url, json=payload)

        elif "message4" in servers:   
                    
            payload = {
                'chat_id': chat_id,
                'text': str(servers['message'])
            }
                    
                
            r = requests.post(url, json=payload)
        else:
#در صورتی که کاربر قبلا با ایمیل دیگری ثبت نام کرده باشد، این پیام به همراه ایمیل اولیه به او نمایش داده می شود و سپس لیست سرورهای تست موجود به صورت اینلاین چاپ می شود.
            if "message2" in servers:

                for server in servers['servers']:
                    button = {
                        "text": server['name'],
                        "callback_data": str(server['id'])+","+"#*$های"
                        
                    }

                    buttons.append([button])

                m1=servers['message2']
                message = str(m1)
                keyboard=buttons
                response = send_inline_keyboard(chat_id, message, keyboard)
                if response["ok"]:
                    return "Inline keyboard sent successfully."
                else:
                    return "Error sending inline keyboard: " + response["description"]   
                            
#در صورتی که کاربر برای نخستین بار و بدون ایمیل قبلی اقدام به دریافت اکانت تست می کند.        
            else:
                # Iterate over the button names and create button objects
                for server in servers['servers']:
                    button = {
                        "text": server['name'],
                        "callback_data": str(server['id'])+","+"#*$های"
                    }

                    buttons.append([button])

                message = "ایمیل شما دریافت شد. لطفا سرور مورد نظر را انتخاب کنید!"
                keyboard=buttons
                response = send_inline_keyboard(chat_id, message, keyboard)
                if response["ok"]:
                    return "Inline keyboard sent successfully."
                else:
                    return "Error sending inline keyboard: " + response["description"]          
    else:
        tel_send_message(chat_id, "Server Error to find test server!") 

#-------------------------------------------------------------------------------------------------------------
#لازمه های اجرای دکمه های اینلاین
BASE_URL = f'https://api.telegram.org/bot{TOKEN}/'
#BASE_URL = f"https://api.telegram.org/bot6524694661:AAH1YrHD9yPMqwrBu6yG88TPJvXFKMg0QVo/"
def send_telegram_request(method, params=None):
    url = BASE_URL + method
    response = requests.post(url, json=params)
    return response.json()

# تابع ارسال پیام از طرف ربات
def send_message(chat_id, text):
    params = {
        "chat_id": chat_id,
        "text": text
    }
    response = send_telegram_request("sendMessage", params)
    return response

# تابع ارسال دکمه های اینلاین 
def send_inline_keyboard(chat_id, message, keyboard):
    params = {
        "chat_id": chat_id,
        "text": message,
        "reply_markup": {
            "inline_keyboard": keyboard
        }
    }
    response = send_telegram_request("sendMessage", params)
    add_log(str(response), log_type='inline_button')
    return response

#---------------------------------------------------------------------------------------------------------------

#مدیریت تمام دیتاهای کال بک دکمه های اینلاین توسط ای تابع انجام می شود.
def handle_callback(update):
    data = update["callback_query"]["data"]
    chat_id = update["callback_query"]["message"]["chat"]["id"]


# پس از فشردن دکمه ی مدیریت اشتراک و دریافت لیست اشتراک ها، اگر روی اکانتی با تایپ وی2ری کلیک کند، 3 گزینه به صورت اینلاین به او نمایش داده می شود
    if "v2ray" in data:
        # tel_send_message(chat_id, data)
        udata=data.split(",")
        #buttons=[[{'text': 'مشاهده اکانت' + ' 👁️', 'callback_data':str(udata[1])+","+",v_account_show*&@@^&"}],[{'text': 'تمدید اشتراک' + ' ♻️', 'callback_data':'hi'}], [{'text': 'تغییر سرور' + ' 🔄', 'callback_data':"#v_change_server#$%"+","+str(udata[1])}]]        
        buttons=[[{'text': 'مشاهده اکانت' + ' 👁️', 'callback_data':str(udata[1])+","+",v_account_show*&@@^&"}], [{'text': 'تغییر سرور' + ' 🔄', 'callback_data':"#v_change_server#$%"+","+str(udata[1])}]]
        message = "تمایل به انجام چه کاری دارید؟"
        keyboard=buttons
        response = send_inline_keyboard(chat_id, message, keyboard)
        if response["ok"]:
            return "Inline keyboard sent successfully."

# پس از فشردن دکمه ی مدیریت اشتراک و دریافت لیست اشتراک ها، اگر روی اکانتی با تایپ اس اس اچ کلیک کند، 4 گزینه به صورت اینلاین به او نمایش داده می شود
    elif "ssh" in data:
        udata=data.split(",")
        #buttons=[[{'text': 'مشاهده اکانت' + ' 👁️', 'callback_data':str(udata[1])+","+",s_account_show*&^%@"}],[{'text': 'تمدید اشتراک' + ' ♻️', 'callback_data':'hii'}], [{'text': 'تغییر سرور' + ' 🔄', 'callback_data':"#s_change_server%$%^#@"+","+str(udata[1])}], [{'text': 'تغییر رمز عبور' + ' 🔐', 'callback_data':str(udata[1])+",changepass#s#"}]]        
        buttons=[[{'text': 'مشاهده اکانت' + ' 👁️', 'callback_data':str(udata[1])+","+",s_account_show*&^%@"}], [{'text': 'تغییر سرور' + ' 🔄', 'callback_data':"#s_change_server%$%^#@"+","+str(udata[1])}], [{'text': 'تغییر رمز عبور' + ' 🔐', 'callback_data':str(udata[1])+",changepass#s#"}]]
        message = "تمایل به انجام چه کاری دارید؟"
        keyboard=buttons
        response = send_inline_keyboard(chat_id, message, keyboard)
        if response["ok"]:
            return "Inline keyboard sent successfully."
#پس از انتخاب سرور اکانت تست وارد این مرحله میشود و اطلاعات اکانت تست یا پیام مربوطه را دریافت می نماید.
    elif "های" in data:
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        chat_id=chat_id
        udata=data.split(",")
        response = requests.post(env['account-test'] , data={'provider': str(udata[0]) , 'chat':str(chat_id)}, headers={'token':env['token']})
        add_log(str(response.content), log_type='account-test')    
        if response.status_code == 200:
            # Parse the JSON response
            servers3 = response.json() 
#در صورتی که کاربر قبلا اکانت تستش را دریافت کرده باشد یا چت آیدی معتبر نباشد
            if "message" in servers3:
                    
                payload = {
                    'chat_id': chat_id,
                    'text': str(servers3['message'])
                }
                r = requests.post(url, json=payload)
                    
#در صورتی که برای نخستین بار قرار است اطلاعات اکانت تست به کاربر نشان داده شود وارد این بخش می شود               
            else:
                    
                username = servers3["username"]
                password = servers3["password"]
                host = servers3["host"]
                port = servers3["port"]
                    
                info_messages = [
        "Username:",
        f"{username}",
        "Password:",
        f"{password}",
        "Host:",
        f"{host}",
        "Port:",
        f"{port}",
        "برای دریافت نرم افزارهای لازم برای استفاده از کانفیگ در اندروید و ios و ویندوز، نرم افزار راهنمای ذیل را مطالعه نمائید. https://hologate2.plus/add-ssh-key"]
                    
                    
                    
                for info_message in info_messages:
                    payload = {
            'chat_id': chat_id,
            'text': info_message
        }
                    

                    r = requests.post(url, json=payload)

            return r   
        else:
            tel_send_message(chat_id, "Server Error!") 
                
        

#پس از فشردن دکمه ی تغییر رمز عبور در اکانت های نوع اس اس اچ وارد این بخش می شود.
    elif "changepass#s#" in data:
        udata=data.split(",")
        response = requests.post(env['change-password'] , data={'accountnum':str(udata[0])}, headers={'token':env['token']})
        # response = requests.post('http://g11.hologate88.com:81/api/change-password' ,  data={'accountnum':str(udata[0])}, headers={'token':'UGFGtZ.RkMfiqfy80O5EP0VoBiVrcs3GGcjJjGKAyr2UAxNtG'})
        add_log(str(response.content), log_type='change-password')
        link = response.json() 
        if response.status_code == 200:
            tel_send_message(chat_id, "جهت تغییر رمز عبور این اکانت، وارد لینک زیر شوید:"+"\n"+str(link["message"]))
        else:
            tel_send_message(chat_id, "Server Error!") 
            



#_sshپس از فشردن دکمه ی مشاهده اکانت  وارد این بخش میشود و اطلاعات اکانت نمایش داده می شود.
    elif "s_account_show*&^%@" in data:
        udata=data.split(",")
        response = requests.post(env['show-account'] , data={'accountnum':str(udata[0])}, headers={'token':env['token']})
        # response = requests.post('http://136.243.86.140:81/api/show-account' ,  data={'accountnum':str(udata[0])}, headers={'token':'UGFGtZ.RkMfiqfy80O5EP0VoBiVrcs3GGcjJjGKAyr2UAxNtG'})
        add_log(str(response.content), log_type='show-account')
        if response.status_code == 200:
        # Parse the JSON response
            account = response.json() 
            tel_send_message(chat_id, "آدرس سرور:"+" "+str(account['data']['serverAddress'])+"\nپورت سرور:"+" "+str(account['data']['port'])+"\nنام کاربری:"+" "+str(account['data']['username'])+"\nرمز عبور:"+" "+str(account['data']['password'])+"\nتعداد دستگاه:"+" "+str(account['data']['number_of_devices'])+"\nتاریخ انقضا:"+" "+str(account['data']['expiration_date']))
        else:
            tel_send_message(chat_id, "Server Error!") 

#در صورتی که اکانت اولیه ی انتخاب شده توسط کاربر پس از دکمه ی مدیریت اشتراک ها از نوع اس اس اچ باشد و سپس گزینه ی تغییر سرور را بفشارد دو دکمه ی اینلاین زیر به او نمایش داده می شود در این مرحله.            
    elif "#s_change_server%$%^#@" in data: 
        udata1=data.split(",")
        # tel_send_message(chat_id, str(udata1[1]))
        output = f"اشتراک فعلی شما تکنولوژی ssh می باشد.\nمی توانید با همین تکنولوژی سرور جدید انتخاب نمایید و یا تکنولوژی v2ray را تست بفرمایید."
        tel_send_message(chat_id, str(output))
        buttons=[[{'text': 'تغییر به سرورهای v2ray' + ' 🌐', 'callback_data':udata1[1]+",change_to_v@%^&*"}],[{'text': 'تغییر به سرورهای ssh' + ' 🔑', 'callback_data':udata1[1]+",change_to_s*&^%"}]]        
        message = "تکنولوژی مورد نظر را انتخاب نمایید:"
        keyboard=buttons
        response = send_inline_keyboard(chat_id, message, keyboard)
        if response["ok"]:
            return "Inline keyboard sent successfully."

# در صورتی که کاربر بخواهد اکانتش را به اکانت نوع اس اس اچ تغییر دهد وارد این بخش می شود و لیست سرورهای اس اس اچ موجود به صورت دکمه های اینلاین نمایش داده می شود        
    elif "change_to_s*&^%" in data:
        udata=data.split(",")
        # tel_send_message(chat_id, str(udata))
        
        response = requests.post(env['find-provider/with-account-move'] , data={'type':"ssh", 'accountnum':str(udata[0])}, headers={'token':env['token']})
        add_log(str(response.content), log_type='find-provider/with-account-move-ssh')
        # response = requests.post('http://g11.hologate88.com:81/api/find-provider/with-account-move' ,  data={'type':"ssh", 'accountnum':str(udata[0])}, headers={'token':'UGFGtZ.RkMfiqfy80O5EP0VoBiVrcs3GGcjJjGKAyr2UAxNtG'})
        if response.status_code == 200:   
        # Parse the JSON response
            servers = response.json() 
            buttons = []

            if "message" in servers:
                for server in servers['message']:
                    button = {
                        "text": server['name'],
                        "callback_data": str(udata[0])+","+str(server['id'])+","+"s_server_account_info*&(^)"
                    }

                    buttons.append([button])
                # tel_send_message(chat_id, buttons)

                message = "لطفا سرور ssh مورد نظر خود را انتخاب نمایید:"
                keyboard=buttons
                response = send_inline_keyboard(chat_id, message, keyboard)
                if response["ok"]:
                    return "Inline keyboard sent successfully."
                else:
                    return "Error sending inline keyboard: " + response["description"]  
                
            elif "error1" in servers:
                tel_send_message(chat_id, servers['error1'])
            elif "error2" in servers:
                tel_send_message(chat_id, servers['error2'])
            elif "error3" in servers:
                tel_send_message(chat_id, servers['error3'])
  
        else:
            tel_send_message(chat_id, "Server Error!")
  
            
          
# در صورتی که کاربر بخواهد اکانتش را به اکانت نوع وی2ری تغییر دهد وارد این بخش می شود و لیست سرورهای وی2ری به صورت دکمه های اینلاین نمایش داده می شود                   
    elif "change_to_v@%^&*" in data:
        udata=data.split(",")
        # tel_send_message(chat_id, str(udata))
        response = requests.post(env['find-provider/with-account-move'] , data={'type':"v2ray", 'accountnum':str(udata[0])}, headers={'token':env['token']})
        add_log(str(response.content), log_type='find-provider/with-account-move-v2ray')
        # response = requests.post('http://g11.hologate88.com:81/api/find-provider/with-account-move' ,  data={'type':"v2ray", 'accountnum':str(udata[0])}, headers={'token':'UGFGtZ.RkMfiqfy80O5EP0VoBiVrcs3GGcjJjGKAyr2UAxNtG'})
        if response.status_code == 200:      
        # Parse the JSON response
            servers = response.json() 
            # data = json.loads(servers["message"])
            buttons = []

            if "message" in servers:
                
                for server in servers['message']:
                    button = {
                        "text": server['name'],
                        "callback_data": str(udata[0])+","+str(server['id'])+","+"v_server_account_info&$%@*"
                    }

                    buttons.append([button])

                message = "لطفا سرور v2ray مورد نظر خود را انتخاب نمایید:"
                keyboard=buttons
                response = send_inline_keyboard(chat_id, message, keyboard)
                if response["ok"]:
                    return "Inline keyboard sent successfully."
                else:
                    return "Error sending inline keyboard: " + response["description"]  
                
            elif "error1" in servers:
                tel_send_message(chat_id, servers['error1'])
            elif "error2" in servers:
                tel_send_message(chat_id, servers['error2'])
            elif "error3" in servers:
                tel_send_message(chat_id, servers['error3'])
  
        else:
            tel_send_message(chat_id, "Server Error!")


#زمانی که شخص پس از درخواست تغییر اکانت به نوع اس اس اچ، روی یکی از سرورهای نوع اس اس اچ کلیک میکند وارد این بخش میشود و سپس اطلاعات اکانت انتخابی یا پیامهای مرتبط به او نمایش داده میشود 
    elif "s_server_account_info*&(^)" in data:
        udata=data.split(",")
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        response = requests.post(env['change-account'] , data={'type':"ssh",'accountnum':str(udata[0]), 'providernum':str(udata[1])}, headers={'token':env['token']})
        add_log(str(response.content), log_type='change-account-ssh')
        # response = requests.post('http://g11.hologate88.com:81/api/change-account' ,  data={'type':"ssh",'accountnum':str(udata[0]), 'providernum':str(udata[1])}, headers={'token':'UGFGtZ.RkMfiqfy80O5EP0VoBiVrcs3GGcjJjGKAyr2UAxNtG'})
    
        if response.status_code == 200:
            account = response.json()
            if "error1" in account:
                tel_send_message(chat_id, str(account['error1']))
            elif "error2" in account:
                tel_send_message(chat_id, str(account['error2']))
            elif "error3" in account:
                tel_send_message(chat_id, str(account['error3']))
            else: 
                tel_send_message(chat_id, str(account['message']))
                tel_send_message(chat_id, "آدرس سرور:"+" "+str(account['server']['serverAddress'])+"\nپورت سرور:"+" "+str(account['server']['port'])+"\nنام کاربری:"+" "+str(account['server']['username'])+"\nرمز عبور:"+" "+str(account['server']['password'])+"\nتعداد دستگاه:"+" "+str(account['server']['number_of_devices'])+"\nتاریخ انقضا:"+" "+str(account['server']['expiration_Date']))
        else:
            tel_send_message(chat_id, "Server Error!")

#زمانی که شخص پس از درخواست تغییر اکانت به نوع وی2ری، روی یکی از سرورهای نوع وی2ری کلیک میکند وارد این بخش میشود و سپس اطلاعات اکانت انتخابی یا پیامهای مرتبط به او نمایش داده میشود  
    elif "v_server_account_info&$%@*" in data:
        udata=data.split(",")
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        response = requests.post(env['change-account'] , data={'type':"v2ray",'accountnum':str(udata[0]), 'providernum':str(udata[1])}, headers={'token':env['token']})
        add_log(str(response.content), log_type='change-account-v2ray')
        # response = requests.post('http://g11.hologate88.com:81/api/change-account' ,  data={'type':"v2ray",'accountnum':str(udata[0]), 'providernum':str(udata[1])}, headers={'token':'UGFGtZ.RkMfiqfy80O5EP0VoBiVrcs3GGcjJjGKAyr2UAxNtG'})
    
        if response.status_code == 200:
            account = response.json()
            if "error1" in account:
                tel_send_message(chat_id, str(account['error1']))
            elif "error2" in account:
                tel_send_message(chat_id, str(account['error2']))
            elif "error3" in account:
                tel_send_message(chat_id, str(account['error3']))
            else: 
                tel_send_message(chat_id, str(account['message']))
        else:        
            tel_send_message(chat_id, "Server Error!")


#_v2rayپس از فشردن دکمه ی مشاهده اکانت  وارد این بخش میشود و اطلاعات اکانت نمایش داده می شود.
    elif "v_account_show*&@@^&" in data:
        udata=data.split(",")
        response = requests.post(env['show-account'] , data={'accountnum':str(udata[0])}, headers={'token':env['token']})
        # response = requests.post('http://136.243.86.140:81/api/show-account' ,  data={'accountnum':str(udata[0])}, headers={'token':'UGFGtZ.RkMfiqfy80O5EP0VoBiVrcs3GGcjJjGKAyr2UAxNtG'})
        add_log(str(response.content), log_type='show-account2')
        if response.status_code == 200:
        # Parse the JSON response
            account = response.json() 
            tel_send_message(chat_id, str(account['data']['vmess']))
        else:
            tel_send_message(chat_id, "Server Error!")
    
#پس از انتخاب یکی از گزینه های خرید اشتراک برای انتخاب نوع تکنولوژی وارد این بخش می شود.
    elif "buying_options&%@" in data:
        udata1=data.split(",")
        # tel_send_message(chat_id, str(udata1[1]))
        # #output = f"اشتراک فعلی شما تکنولوژی ssh می باشد.\nمی توانید با همین تکنولوژی سرور جدید انتخاب نمایید و یا تکنولوژی v2ray را تست بفرمایید."
        # # tel_send_message(chat_id, str(output))
        buttons=[[{'text': 'v2ray' + ' 🌐', 'callback_data':udata1[0]+","+"v_buytype@$%"}],[{'text': 'ssh' + ' 🔑', 'callback_data':udata1[0]+","+"s_buytype@$%"}]]        
        message = "تکنولوژی مورد نظر را انتخاب نمایید:"
        keyboard=buttons
        response = send_inline_keyboard(chat_id, message, keyboard)
        if response["ok"]:
            return "Inline keyboard sent successfully."
        
#وقتی برای خرید اکانت تکنولوژی وی2ری را انتخاب میکند لیست سرورهای موجود به شکل اینلاین به او نمایش داده می شود        
    elif "v_buytype@$%" in data:
        udata1=data.split(",")
        # tel_send_message(chat_id, str(data))
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        response = requests.post(env['find-protocol'] , data={'type':"v2ray"}, headers={'token':env['token']})
        #response = requests.post('http://136.243.86.140:81/api/find-protocol', data={'type':"v2ray"}, headers={'token':'UGFGtZ.RkMfiqfy80O5EP0VoBiVrcs3GGcjJjGKAyr2UAxNtG'})
        add_log(str(response.content), log_type='find-protocol_v2ray')
        if response.status_code == 200:
            
            # Parse the JSON response
            servers= response.json() 
            # tel_send_message(chat_id, str(servers))
            
            buttons=[]        
            # Iterate over the button names and create button objects
            for server in servers["message"]:
                button = {
                    # "text": option["name"]+","+option["price"]+ +","+option["number_of_devices"]+", نامحدود"+ " 🔗",
                    "text": str(server["name"])+ " 🔗",
                    "callback_data": str(udata1[0])+","+str(server["id"])+","+"v_servers&%@"
                }

                buttons.append([button])
            # tel_send_message(chat_id, str(buttons))
            

            message = f"سرور v2ray مد  نظر خود را انتخاب نمایید:"
            keyboard=buttons
            response = send_inline_keyboard(chat_id, message, keyboard)
            if response["ok"]:
                return "Inline keyboard sent successfully."
        else:
            tel_send_message(chat_id, "Server Error!")
            
    #وقتی برای خرید اکانت، تکنولوژی اس اس اچ را انتخاب میکند لیست سرورهای موجود به شکل اینلاین به او نمایش داده می شود        
    elif "s_buytype@$%" in data:
        udata1=data.split(",")
        # tel_send_message(chat_id, str(data))
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        response = requests.post(env['find-protocol'] , data={'type':"ssh"}, headers={'token':env['token']})
        #response = requests.post('http://136.243.86.140:81/api/find-protocol', data={'type':"v2ray"}, headers={'token':'UGFGtZ.RkMfiqfy80O5EP0VoBiVrcs3GGcjJjGKAyr2UAxNtG'})
        add_log(str(response.content), log_type='find-protocol_ssh')
        if response.status_code == 200:
            
            # Parse the JSON response
            servers= response.json() 
            # tel_send_message(chat_id, str(servers))
            
            buttons=[]        
            # Iterate over the button names and create button objects
            for server in servers["message"]:
                button = {
                    # "text": option["name"]+","+option["price"]+ +","+option["number_of_devices"]+", نامحدود"+ " 🔗",
                    "text": str(server["name"])+ " 🔗",
                    "callback_data": str(udata1[0])+","+str(server["id"])+","+"s_servers&%@"
                }

                buttons.append([button])
            # tel_send_message(chat_id, str(buttons))
            

            message = f"سرور ssh مد  نظر خود را انتخاب نمایید:"
            keyboard=buttons
            response = send_inline_keyboard(chat_id, message, keyboard)
            if response["ok"]:
                return "Inline keyboard sent successfully."
        else:
            tel_send_message(chat_id, "Server Error!")
        

    #وقتی برای خرید یکی از سورهای اس اس اچ را انتخاب میکند وارد این بخش میشود و داشتن یا نداشتن کد تخفیف به صورت دکمه های اینلاین از او پرسیده می شود
    elif "s_servers&%@" in data:
        udata1=data.split(",")
        # tel_send_message(chat_id, str(udata1))
        buttons=[[{'text': 'بله' + ' 😎', 'callback_data':str(udata1[0])+","+str(udata1[1])+","+"s-s-h"+","+"s_discount_yes@$%"}],[{'text': 'خیر' + ' ☹️', 'callback_data':str(udata1[0])+","+str(udata1[1])+","+"s-s-h"+","+"s_discount-no@$%"}]]        
        message = "آیا کد تخفیف دارید؟"
        keyboard=buttons
        response = send_inline_keyboard(chat_id, message, keyboard)
        if response["ok"]:
            return "Inline keyboard sent successfully."

    #وقتی برای خرید یکی از سورهای وی2ری را انتخاب میکند وارد این بخش میشود و داشتن یا نداشتن کد تخفیف به صورت دکمه های اینلاین از او پرسیده می شود
    elif "v_servers&%@" in data:     
        udata1=data.split(",")
        # tel_send_message(chat_id, str(udata1))
        buttons=[[{'text': 'بله' + ' 😎', 'callback_data':str(udata1[0])+","+str(udata1[1])+","+"v-2-r-a-y"+","+"v_discount_yes@$%"}],[{'text': 'خیر' + ' ☹️', 'callback_data':str(udata1[0])+","+str(udata1[1])+","+"v-2-r-a-y"+","+"v_discount-no@$%"}]]        
        message = "آیا کد تخفیف دارید؟"
        keyboard=buttons
        response = send_inline_keyboard(chat_id, message, keyboard)
        if response["ok"]:
            return "Inline keyboard sent successfully."   
        
    #زمانی که قصد خریداکانت اس اس اچ دارد و کد تخفیف دارد
    elif "s_discount_yes@$%" in data:
        global udata2
        udata2=data.split(",")
        
        # tel_send_message(chat_id, str(udata2)) 
        # servicenum2=udata2[0]
        # providernum2=udata2[1]
        # type2=udata2[2].replace("-", "")
        #-----------------------------------------------
        #در صورتی که کدتخفیف داشته باشد، به از او میخواهیم که کد را وارد کند و استیت او را به کد تخفیف اپدیت می کنیم.
        tel_send_message(chat_id, 'لطفا کد تخفیف خود را وارد نمایید:' )
        new_state = "s_discount"
        sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
        values = (new_state, chat_id)
        mycursor.execute(sql, values)
        db.get_commit()
        result = mycursor.fetchone()
        add_log(str(result), log_type=str(chat_id)+'s_discount')

            

    #زمانی که قصد خرید اکانت اس اس اچ دارد و کد تخفیف ندارد اطلاعات لازم در بادی به سمت سرور فرستاده شده و اکانت خریداری میشود و به کابر تحویل داده می شود.
    elif "s_discount-no@$%" in data:  
        udata1=data.split(",") 
        #tel_send_message(chat_id, str(udata1)) 
        servicenum=udata1[0]
        providernum=udata1[1]
        type=udata1[2].replace("-", "")
        chat=chat_id 
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        response = requests.post(env['buy-account'] , data={'servicenum':str(servicenum), 'providernum':str(providernum),'type':str(type), 'chat':str(chat)}, headers={'token':env['token']})
        #response = requests.post('http://136.243.86.140:81/api/buy-account', data={'servicenum':str(servicenum), 'providernum':str(providernum),'type':str(type), 'chat':str(chat)}, headers={'token':'UGFGtZ.RkMfiqfy80O5EP0VoBiVrcs3GGcjJjGKAyr2UAxNtG'})
        add_log(str(response.content), log_type='buy-account')
        if response.status_code == 200:
            account= response.json() 
            if "error1" in account:
                tel_send_message(chat_id, str(account['error1']))

            elif "error2" in account:
                tel_send_message(chat_id, str(account['error2']))

            elif "error3" in account:
                tel_send_message(chat_id, str(account['error3']))

            elif "error4" in account:
                tel_send_message(chat_id, str(account['error4']))

            elif "error5" in account:
                tel_send_message(chat_id, str(account['error5']))

            elif "error6" in account:
                tel_send_message(chat_id, str(account['error6']))

            elif "error7" in account:
                tel_send_message(chat_id, str(account['error7']))

            elif "error8" in account:
                tel_send_message(chat_id, str(account['error8']))

            else:
                tel_send_message(chat_id, str(account["message"])+"!")
                #---------------------------------------------------
                username = account["server"]["username"]
                password = account["server"]["password"]
                port = account["server"]["port"]
                expiration_date = account["server"]["expiration_Date"]
                serverAddress= account["server"]["serverAddress"]
                number_of_devices= account["server"]["number_of_devices"]
                    
                info_messages = [
                                "نام کاربری:",
                                f"{username}",
                                "رمز عبور:",
                                f"{password}",
                                "پورت سرور:",
                                f"{port}",
                                "تاریخ انقضا:",
                                f"{expiration_date}",
                                "آدرس سرور",
                                f"{serverAddress}",
                                "تعداد دستگاه",
                                f"{number_of_devices}",
                                ]
                      
                for info_message in info_messages:
                    payload = {
                        'chat_id': chat_id,
                        'text': info_message
                    }
                    
                    r = requests.post(url, json=payload)

            return r   

        else:
            tel_send_message(chat_id, "Server Error!")

    
    #زمانی که قصد خریداکانت وی2ری دارد و کد تخفیف دارد
    elif "v_discount_yes@$%" in data:
        
        global udata3
        udata3=data.split(",")
        # tel_send_message(chat_id, str(udata3)) 
        # servicenum2=udata3[0]
        # providernum2=udata3[1]
        # type2=udata3[2].replace("-", "")
        #-----------------------------------------------
        tel_send_message(chat_id, 'لطفا کد تخفیف خود را وارد نمایید:' )
        new_state = "v_discount"
        sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
        values = (new_state, chat_id)
        mycursor.execute(sql, values)
        db.get_commit()
        result = mycursor.fetchone()
        add_log(str(result), log_type=str(chat_id)+'v-discount')

            

    #زمانی که قصد خرید اکانت وی2ری دارد و کد تخفیف ندارد
    elif "v_discount-no@$%" in data:  
        udata1=data.split(",") 
        #tel_send_message(chat_id, str(udata1)) 
        servicenum=udata1[0]
        providernum=udata1[1]
        type=udata1[2].replace("-", "")
        chat=chat_id 
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        response = requests.post(env['buy-account'] , data={'servicenum':str(servicenum), 'providernum':str(providernum),'type':str(type), 'chat':str(chat)}, headers={'token':env['token']})
        #response = requests.post('http://136.243.86.140:81/api/buy-account', data={'servicenum':str(servicenum), 'providernum':str(providernum),'type':str(type), 'chat':str(chat)}, headers={'token':'UGFGtZ.RkMfiqfy80O5EP0VoBiVrcs3GGcjJjGKAyr2UAxNtG'})
        add_log(str(response.content), log_type='buy-account')
        if response.status_code == 200:
            account= response.json() 
            if "error1" in account:
                tel_send_message(chat_id, str(account['error1']))

            elif "error2" in account:
                tel_send_message(chat_id, str(account['error2']))

            elif "error3" in account:
                tel_send_message(chat_id, str(account['error3']))

            elif "error4" in account:
                tel_send_message(chat_id, str(account['error4']))

            elif "error5" in account:
                tel_send_message(chat_id, str(account['error5']))

            elif "error6" in account:
                tel_send_message(chat_id, str(account['error6']))

            elif "error7" in account:
                tel_send_message(chat_id, str(account['error7']))

            elif "error8" in account:
                tel_send_message(chat_id, str(account['error8']))

            else:
                tel_send_message(chat_id, "اکانت شما با موفقیت خریداری شد!")
                tel_send_message(chat_id, str(account["message"]))

        else:
            tel_send_message(chat_id, "Server Error!")
    


            # #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            ##اطلاعات مربوط به تصویر کردن کد وی2ری
            # # def generate_qr_code():
            # # Input string
            # input_string = str(account['data']['vmess'])

            # # Remove the "vmess://" part
            # encoded_data = input_string.replace("vmess://", "")

            # # Decode base64
            # decoded_data = base64.b64decode(encoded_data)

            # # Create a QR code instance
            # qr_code = qrcode.QRCode()

            # # Add data to the QR code
            # qr_code.add_data(decoded_data)

            # # Generate the QR code image
            # qr_code.make(fit=True)

            # # Create a PIL image from the QR code
            # image = qr_code.make_image(fill_color="black", back_color="white")

            # # Create an in-memory buffer to hold the image data
            # buffer = BytesIO()
            # image.save(buffer, format='PNG')
            # buffer.seek(0)

            # # Send the image as a message in the Telegram bot
            # url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
            # files = {"photo": buffer}
            # data = {"chat_id": chat_id}
            # response = requests.post(url, files=files, data=data)

            # # return "QR code sent!"
            # #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


##در صورتی که اکانت اولیه ی انتخاب شده توسط کاربر پس از دکمه ی مدیریت اشتراک ها از نوع وی2ری باشد و سپس گزینه ی تغییر سرور را بفشارد دو دکمه ی اینلاین زیر به او نمایش داده می شود در این مرحله.  
    elif "#v_change_server#$%" in data:
        udata1=data.split(",")
        output = f"اشتراک فعلی شما تکنولوژی v2ray می باشد.\nمی توانید با همین تکنولوژی سرور جدید انتخاب نمایید و یا تکنولوژی ssh را تست بفرمایید."
        tel_send_message(chat_id, str(output))
        ##send_message(chat_id, "yuhaha! v2ray")

        buttons=[[{'text': 'تغییر به سرورهای v2ray' + ' 🌐', 'callback_data':udata1[1]+",change_to_v@%^&*"}],[{'text': 'تغییر به سرورهای ssh' + ' 🔑', 'callback_data':udata1[1]+",change_to_s*&^%"}]]          
        message = "تکنولوژی مورد نظر را انتخاب نمایید:"
        keyboard=buttons
        response = send_inline_keyboard(chat_id, message, keyboard)
        if response["ok"]:
            return "Inline keyboard sent successfully."
        
    else:
        tel_send_message(chat_id, "nothing has been set for this button yet")



#-----------------------------------------------------------------------------------------------------------------
#جهت مدیریت تمامی کامندها و استیت ها، این تابع فراخوانی میشود.
def state_handling(chat_id,txt):

    software = "بهترین نرم افزار برای اندروید و ios نپسترنت وی یا nV می باشد\n https://hologate2.plus/napsternetv/ \n اگر دسترسی به گوگل پلی هم ندارید از طریق سایت ما دانلود و نصب کنید. \n برای ویندوز هم بعد از خرید اکانت  راهنمای لازم برای شما ارسال خواهد شد. \n "  
    cafeArzLink='https://app.cafearz.com/login  \nلینک مراجعه مستقیم به کافه ارز - کارمزد 1000 تومان'
    #novinLink = "https://panel.novinpardakht.com/    \nکارمزد 20 هزار تومان لینک مراجعه مستقیم به فروشگاه نوین پرداخت"
    nikpardakht = "آموزش خرید ووچر پرفکت مانی از سایت نیک پرداخت \n1. وارد سایت ذیل می شوید و ثبت نام می کنید \n https://nikpardakht.com/ \n 2. از منوی سمت راست خرید ووچر پرفکت مانی را انتخاب کنید  \n 3. مبلغ دلاری را وارد کرده و پرداخت کنید.\n 4. بعد از 10 دقیقه شماره ووچر و کدفعالسازی در سفارش شما اضافه می شود\n"
    tron = " هلوگیت از طریق درگاه آنلاین پرداخت رمز ارزی را انجام می دهد و برای پرداخت با ترون یا تتر شما می توانید وارد فروشگاه هلوگیت شوید و در قسمت خرید اشتراک گزینه پرداخت با رمز ارز را انتخاب کنید. https://hologate2.plus/shop"
    transaction_log_send = "بعد از پرداخت وجه اتوماتیک مبلغ دلاری به کیف پول هلوگیت شما اضافه می شود و اکانت شما تحویل می گردد در صورتی که مشکلی ایجاد شد به پشتیبانی در  تلگرام پیام دهید \n https://t.me/hologate5 "
    #novin = "https://hologate2.plus/xray/images/pages/buy-ssh/novin.mp4 فیلم خرید پرفکت مانی از نوین پرداخت "
    fq0 = "\nلطفا پرسش های متداول زیر را مطالعه کرده و در صورتی که جواب شما در آن ها نبود به آیدی  پشتیبانی پیام دهید:"
    fq1 = "\n❓در صورتی که سرور فیلتر شد، سرور جدید ارائه می شود؟\n  احتمال فیلتر شدن سرورهای هلوگیت به دلیل استفاده از تکنولوژی های خاص، کم است. با این حال در صورتی که سروری فیلتر شود توسط تیم پشتیبانی هلوگیت به سرعت تعویض خواهد شد. همچنین شما می توانید با مراجعه به پنل کاربری خود در هلوگیت، سرور کانکشن خود را تغییر دهید.\n"
    fq2 = "\n❓سرورهای هلوگیت آی پی ثابت هستند؟\n آی پی سرورها ممکن است تغییر کنند اما لوکیشن همواره ثابت خواهد بود. برای کارهایی مانند ترید هلوگیت مناسب است چرا که سایت های صرافی خارجی روی لوکیشن شما حساس هستند و آی پی در اولویت آنها نیست.\n"
    fq3 = "\n❓چطور می توانم از تخفیف های هلوگیت برای خرید عمده استفاده کنم؟\n  در هلوگیت با شارژ عمده حساب خود می توانید از هدیه های هلوگیت به صورت زیر بهره مند شوید:\n-هر 10 دلار شارژ حساب در یک شارژ - 1 دلار هدیه\n-هر 20 دلار شارژ حساب در یک شارژ - 3 دلار هدیه\n-هر 50 دلار شارژ حساب در یک شارژ - 10 دلار هدیه\n"
    fq4 = "\n❓اکانت ها چند کاربره هستند؟ محدودیت حجمی چقدر است؟\n تمامی اشتراک های هلوگیت 2 کاربره با ترافیک نا محدود می باشند.\n"
    fq5 = "\n❓در صورت اتصال بیش از 2 کاربر، اکانت بلاک می شود؟\n خیر، هیچ گاه بیش از 2 دستگاه نمی توانند به یک کانکشن متصل شوند و امکان اتصال نفرات اضافه به صورت خودکار وجود ندارد.\n"
    fq6 = "\n❓کانکشن های هلوگیت از چه کشورهایی است؟\n سرورهای هلوگیت در کشورهای اروپایی و آمریکا قرار دارند. در صورت نیاز به لوکیشن خاص، پیش از خرید به آی دی پشتیبانی پیام دهید.\n"
    fq7 = "\n❓سرعت و کیفیت کانکشن هلوگیت چطور است؟\n اشتراک های هلوگیت سرعت کاملا مناسبی برای وبگردی و استفاده از شبکه های اجتماعی دارند و شما چه از نظر دانلود و چه از نظر آپلود مشکلی در اتصال نخواهید داشت. \n"
    fq8 = "\n❓نرم افزارهای لازم برای اتصال به کانکشن های هلوگیت چیست؟\n در لینک زیر نرم افزارهای لازم برای اتصال به کانکشن های هلوگیت عنوان شده‌اند:\nhttp://hologate4.com/select-tools\n"
    # fq9 = "\n❓حجم اکانت ها نامحدود است ؟ \n بله نامحدود است."
    fqf = fq0 + fq1 + fq2 + fq3 + fq4 + fq5 +fq6 + fq7 + fq8
    select_payment = "\n روش دوم استفاده از رمز ارزهای تتر و ترون می باشد که اگر کیف پول رمز ارزی ندارید بهتر است از روش اول استفاده نمائید برای آشنائی بهتر لینک ذیل را مطالعه کنید https://hologate2.plus/crypto-payment"
    payment = "با استفاده از راهنمای ذیل، یک کارت مثلا 2 دلاری پرفکت مانی خریداری کنید و بعد از طریق فروشگاه اشتراک خود را فورا تحویل بگیرید . \n https://hologate2.plus/shop \n" 

    #به محض این که هر کاربری چیزی در ربات تایپ کند، چک میشود که آیا چت آیدی او در دیتابیس موجود است یا خیر
    #____________________
    sql2 = "SELECT chat_id FROM chat_states WHERE chat_id = ?"
    value2 = (chat_id,)
    mycursor.execute(sql2, value2)
    result = mycursor.fetchone()  # Retrieve a single row
    # tel_send_message(chat_id, str(result))
         # اگر چت آیدی از قبل وجود نداشته باشد، به دیتابیس اضافه شده و استیت ان هم هوم در نظر گرفته می شود
    #______________________________________________________________________________________________________________
    if not result:
        # Chat ID doesn't exist in the database, insert a new record
        sql = "INSERT INTO chat_states (chat_id , state) VALUES (?, ? ) "
        value = (chat_id, 'home')
        mycursor.execute(sql , value)
        db.get_commit()
        # handle_state_one(chat_id, text)
        add_log("Done", log_type="New chat ID added to the database.")
        # tel_send_message(chat_id,"New chat ID added to the database.")***
    #در صورتی که از قبل ان چت آیدی در دیتابیس موجود باشد، در لاگ میبینیم که چت آیدی از قبل موجود است و صرفا استیت آنرا دریافت میکنیم .
    else:
        # Chat ID exists in the database
        add_log("this chat id alredy exists", log_type="chat_id existence check")
        # tel_send_message(chat_id, "this chat id alredy exists as "+str(result))***
                    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%.
    sql = "SELECT state FROM chat_states WHERE chat_id = ?"
    value = (chat_id,)
    mycursor.execute(sql, value)
    state = mycursor.fetchone()  # Retrieve a single row  
    state=state[0] 
    add_log(str(state), log_type="reciving state of a chat_id")
    # tel_send_message(chat_id, "you are in <"+str(state)+"> state now!")***
    #---------------------------------------------------------------
    #حالا با توجه به این که هر چت آیدی در چه استیتی قرار دارد، بخش های زیر اجرا می شود
    #---------------------------------------------------------
    #استیت دیفالت، هوم می باشد و همه چیز به صورت عادی در هوم اجرا می شود و پس از دریافت ورودی ها در سایر استیت ها نیز استیت ها مجددا به هوم آپدیت میشوند.
    if state=="home":
        if txt == "/start" or txt == "صفحه 1 📄":
            add_log(str(env['find-server-test']), log_type='ببینیم کجا درخواست میزنه')
            start_send_button(chat_id)
        elif txt == "قیمت خدمات 💸":
            tel_send_image(chat_id)
            SendPrice(chat_id)
        elif "مدیریت اشتراک ها 🔒" in txt :
            login(chat_id)
        #پس از انتخاب دکمه ی اکانت تست، از کاربر خواسته میشود ایمیلش را وارد کند 
        #بعد از انتخاب اکانت تست، استیت چت آیدی کاربر، به استیت ایمیل آپدیت میشود و منتظر دریافت ایمیل کاربر می ماند
        elif txt ==  "اکانت تست 🆓" :
            tel_send_message(chat_id, 'برای دریافت اکانت تست فیلترشکن هلوگیت، ایمیل خود را وارد نمایید. \nاطلاعات کانکشن تست برای شما ارسال خواهد شد.' )
            new_state = "email"
            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
            values = (new_state, chat_id)
            mycursor.execute(sql, values)
            db.get_commit()
            result = mycursor.fetchone()
            add_log(str(result), log_type=str(chat_id)+'email')
        
        elif "خرید اشتراک 🛒" in txt :
            #tel_send_message(chat_id, f"موجودی کیف پول شما {x}$ می باشد؛گزینه مورد نظر خود را انتخاب نمایید:")
            buy(chat_id)
        elif txt == "نرم افزارهای لازم 📲":
            tel_send_message(chat_id, fq8)
            
        elif (txt == "1 ماهه 2 دلار 🟢" or txt == "3 ماهه 5 دلار 🟢" or txt == "6 ماهه 10 دلار 🟢" or txt == "1 ساله 18 دلار 🟢"):  
            tel_send_message(chat_id,"از دو طریق می توانید اشتراک های هلوگیت را خریداری نمایید.\n\nخرید با ووچر پرفکت مانی\nراهنمای خرید ووچر پرفکت مانی در 3 دقیقه\nhttps://t.me/hologate6/513\n\nخرید با رمز ارز\nراهنمای خرید با رمز ارز\nhttp://hologate4.com/crypto-payment")
            # tel_send_message(chat_id,"https://hologate2.plus/xray/images/pages/buy-ssh/buy%20voucher%20cafearz.mp4 شما می توانید مثلا 2 دلار مطابق فیلم ذیل از کافه ارز بخرید و بعد در فروشگاه طبق فیلم بلافاصله اکانت را دریافت نمائید  ")
            # tel_send_message(chat_id, cafeArzLink )
            # # tel_send_message(chat_id, novin )
            # # tel_send_message(chat_id, novinLink )
            # tel_send_message(chat_id, select_payment+"\n"+tron )
            # # tel_send_message(chat_id, tron )
            # tel_send_message(chat_id, transaction_log_send)
            
        elif txt == "پشتیبانی 🙋‍♀️":
            tel_send_message(chat_id, fqf )
            support(chat_id)
        elif txt == "چت با پشتیبان" or txt == "چت با کارشناس 💬":
            tel_send_message(chat_id,"https://t.me/hologate5")
            
        elif txt == "سئوالات متداول ❓":
            tel_send_message(chat_id, fqf )
                
        elif txt == "پرداخت وجه 💰": 
            tel_send_message(chat_id,"از دو طریق می توانید اشتراک های هلوگیت را خریداری نمایید.\n\nخرید با ووچر پرفکت مانی\nراهنمای خرید ووچر پرفکت مانی در 3 دقیقه\nhttps://t.me/hologate6/513\n\nخرید با رمز ارز\nراهنمای خرید با رمز ارز\nhttp://hologate4.com/crypto-payment")
            # tel_send_message(chat_id,"https://hologate2.plus/xray/images/pages/buy-ssh/buy%20voucher%20cafearz.mp4 \nشما می توانید مثلا 2 دلار مطابق فیلم ذیل از کافه ارز بخرید و بعد در فروشگاه طبق فیلم بلافاصله اکانت را دریافت نمائید  ")
            # tel_send_message(chat_id, cafeArzLink )
            # # tel_send_message(chat_id, novin )
            # # tel_send_message(chat_id, novinLink )
            # tel_send_message(chat_id, select_payment+"\n"+tron)
            # # tel_send_message(chat_id, tron )
            # tel_send_message(chat_id, transaction_log_send)

        elif txt == "hi":
            #payment_tron(chat_id)
            tel_send_message(chat_id, str(udata2))
        elif txt == "image":
            tel_send_image(chat_id)
        elif txt == "audio":
            tel_send_audio(chat_id)
        elif txt == "video":
            tel_send_video(chat_id)
        elif txt == "file":
            tel_send_document(chat_id)
        elif txt == "poll":
            tel_send_poll(chat_id)
        elif txt == "inline":
            tel_send_inlinebutton(chat_id)
        elif "good" in txt:
            tel_send_image(chat_id)
        else:
            tel_send_message(chat_id, 'پیام شما معتبر نیست.')
    else:
        
        #اگر کاربر در استیت ایمیل باشد، این بخش اجرا میشود
        if state=="email":
            if txt is not None:
            #در صورتی که @ و . در وردی کاربر باشد به عنوان ایمیل شناخته شده و دریافت میشود و به عنوان بادی در ای پی آی فرستاده میشود
                if "@" and "." in txt:
                    # tel_send_message(chat_id, str(txt))
                    tel_send_message(chat_id, "ایمیل شما دریافت شد!")
                    send2(chat_id, txt)
                    #پس از دریافت ایمیل، استیت مجددا از ایمیل به هوم اپدیت میشود.
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                #مادامی که در استیت ایمیل می باشد، اگر کدام از کامندهای اصلی را صدا بزند، به استیت هوم اپدیت شده و انها اجرا میشوند   
                else: 
                    if txt == "/start" or txt == "صفحه 1 📄":
                        new_state = "home"
                        sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                        values = (new_state, chat_id)
                        mycursor.execute(sql, values)
                        db.get_commit()
                        result = mycursor.fetchone()
                        add_log(str(result), log_type=str(chat_id)+'home')
                        start_send_button(chat_id)
                    elif txt == "قیمت خدمات 💸":
                        new_state = "home"
                        sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                        values = (new_state, chat_id)
                        mycursor.execute(sql, values)
                        db.get_commit()
                        result = mycursor.fetchone()
                        add_log(str(result), log_type=str(chat_id)+'home')
                        tel_send_image(chat_id)
                        SendPrice(chat_id)
                    elif "مدیریت اشتراک ها 🔒" in txt :
                        new_state = "home"
                        sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                        values = (new_state, chat_id)
                        mycursor.execute(sql, values)
                        db.get_commit()
                        result = mycursor.fetchone()
                        add_log(str(result), log_type=str(chat_id)+'home')
                        login(chat_id)
                    #پس از انتخاب دکمه ی اکانت تست، از کاربر خواسته میشود ایمیلش را وارد کند 
                    
                    elif txt ==  "اکانت تست 🆓" :
                        new_state = "home"
                        sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                        values = (new_state, chat_id)
                        mycursor.execute(sql, values)
                        db.get_commit()
                        result = mycursor.fetchone()
                        add_log(str(result), log_type=str(chat_id)+'home')
                        tel_send_message(chat_id, 'برای دریافت اکانت تست فیلترشکن هلوگیت، ایمیل خود را وارد نمایید. \nاطلاعات کانکشن تست برای شما ارسال خواهد شد.' )
                        new_state = "email"
                        sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                        values = (new_state, chat_id)
                        mycursor.execute(sql, values)
                        db.get_commit()
                        result = mycursor.fetchone()
                        add_log(str(result), log_type=str(chat_id)+'email')
                    
                    elif "خرید اشتراک 🛒" in txt :
                        new_state = "home"
                        sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                        values = (new_state, chat_id)
                        mycursor.execute(sql, values)
                        db.get_commit()
                        result = mycursor.fetchone()
                        add_log(str(result), log_type=str(chat_id)+'home')
                        #tel_send_message(chat_id, f"موجودی کیف پول شما {x}$ می باشد؛گزینه مورد نظر خود را انتخاب نمایید:")
                        buy(chat_id)
                    elif txt == "نرم افزارهای لازم 📲":
                        new_state = "home"
                        sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                        values = (new_state, chat_id)
                        mycursor.execute(sql, values)
                        db.get_commit()
                        result = mycursor.fetchone()
                        add_log(str(result), log_type=str(chat_id)+'home')
                        tel_send_message(chat_id, fq8)
                        
                    elif (txt == "1 ماهه 2 دلار 🟢" or txt == "3 ماهه 5 دلار 🟢" or txt == "6 ماهه 10 دلار 🟢" or txt == "1 ساله 18 دلار 🟢"):  
                        new_state = "home"
                        sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                        values = (new_state, chat_id)
                        mycursor.execute(sql, values)
                        db.get_commit()
                        result = mycursor.fetchone()
                        add_log(str(result), log_type=str(chat_id)+'home')
                        
                        tel_send_message(chat_id,"از دو طریق می توانید اشتراک های هلوگیت را خریداری نمایید.\n\nخرید با ووچر پرفکت مانی\nراهنمای خرید ووچر پرفکت مانی در 3 دقیقه\nhttps://t.me/hologate6/513\n\nخرید با رمز ارز\nراهنمای خرید با رمز ارز\nhttp://hologate4.com/crypto-payment")
                        # tel_send_message(chat_id,"https://hologate2.plus/xray/images/pages/buy-ssh/buy%20voucher%20cafearz.mp4 شما می توانید مثلا 2 دلار مطابق فیلم ذیل از کافه ارز بخرید و بعد در فروشگاه طبق فیلم بلافاصله اکانت را دریافت نمائید  ")
                        # tel_send_message(chat_id, cafeArzLink )
                        # # tel_send_message(chat_id, novin )
                        # # tel_send_message(chat_id, novinLink )
                        # tel_send_message(chat_id, select_payment+"\n"+tron )
                        # # tel_send_message(chat_id, tron )
                        # tel_send_message(chat_id, transaction_log_send)
                            
                    elif txt == "پشتیبانی 🙋‍♀️":
                        new_state = "home"
                        sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                        values = (new_state, chat_id)
                        mycursor.execute(sql, values)
                        db.get_commit()
                        result = mycursor.fetchone()
                        add_log(str(result), log_type=str(chat_id)+'home')
                        tel_send_message(chat_id, fqf )
                        support(chat_id)
                    elif txt == "چت با پشتیبان" or txt == "چت با کارشناس 💬":
                        new_state = "home"
                        sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                        values = (new_state, chat_id)
                        mycursor.execute(sql, values)
                        db.get_commit()
                        result = mycursor.fetchone()
                        add_log(str(result), log_type=str(chat_id)+'home')
                        tel_send_message(chat_id,"https://t.me/hologate5")
                        
                    elif txt == "سئوالات متداول ❓":
                        new_state = "home"
                        sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                        values = (new_state, chat_id)
                        mycursor.execute(sql, values)
                        db.get_commit()
                        result = mycursor.fetchone()
                        add_log(str(result), log_type=str(chat_id)+'home')
                        tel_send_message(chat_id, fqf )
                            
                    elif txt == "پرداخت وجه 💰":
                        new_state = "home"
                        sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                        values = (new_state, chat_id)
                        mycursor.execute(sql, values)
                        db.get_commit()
                        result = mycursor.fetchone()
                        add_log(str(result), log_type=str(chat_id)+'home')
                        
                        tel_send_message(chat_id,"از دو طریق می توانید اشتراک های هلوگیت را خریداری نمایید.\n\nخرید با ووچر پرفکت مانی\nراهنمای خرید ووچر پرفکت مانی در 3 دقیقه\nhttps://t.me/hologate6/513\n\nخرید با رمز ارز\nراهنمای خرید با رمز ارز\nhttp://hologate4.com/crypto-payment")
                        # tel_send_message(chat_id,"https://hologate2.plus/xray/images/pages/buy-ssh/buy%20voucher%20cafearz.mp4 \nشما می توانید مثلا 2 دلار مطابق فیلم ذیل از کافه ارز بخرید و بعد در فروشگاه طبق فیلم بلافاصله اکانت را دریافت نمائید  ")
                        # tel_send_message(chat_id, cafeArzLink )
                        # # tel_send_message(chat_id, novin )
                        # # tel_send_message(chat_id, novinLink )
                        # tel_send_message(chat_id, select_payment+"\n"+tron)
                        # # tel_send_message(chat_id, tron )
                        # tel_send_message(chat_id, transaction_log_send)
                    
                    #-------------------------------------------------------------
                    else:
                        tel_send_message(chat_id, "ایمیل را به صورت صحیح وارد نمایید!") 
            
    
        #اگر در استیت کد تخفیف برای خرید اکانت اس اس اچ باشد، این بخش اجرا میشود        
        elif state=="s_discount":
            if txt is not None:
                #مادامی که در استیت کد تخفیف باشد و یکی از کامندهای اصلی صدا زده شود، به استیت هوم آپدیت شده و انها اجرا می شوند، به جز اکانت تست که به استیت ایمیل اپدیت میشود واجرا میشود
                # tel_send_message(chat_id, str(udata2))
                if txt == "/start" or txt == "صفحه 1 📄":
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    start_send_button(chat_id)
                elif txt == "قیمت خدمات 💸":
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    tel_send_image(chat_id)
                    SendPrice(chat_id)
                elif "مدیریت اشتراک ها 🔒" in txt :
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    login(chat_id)
                #پس از انتخاب دکمه ی اکانت تست، از کاربر خواسته میشود ایمیلش را وارد کند 
                elif txt ==  "اکانت تست 🆓" :
                    new_state = "email"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'email')
                    tel_send_message(chat_id, 'برای دریافت اکانت تست فیلترشکن هلوگیت، ایمیل خود را وارد نمایید. \nاطلاعات کانکشن تست برای شما ارسال خواهد شد.' )
                
                elif "خرید اشتراک 🛒" in txt :
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    buy(chat_id)
                elif txt == "نرم افزارهای لازم 📲":
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    tel_send_message(chat_id, fq8)
                    
                elif (txt == "1 ماهه 2 دلار 🟢" or txt == "3 ماهه 5 دلار 🟢" or txt == "6 ماهه 10 دلار 🟢" or txt == "1 ساله 18 دلار 🟢"):  
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    
                    tel_send_message(chat_id,"از دو طریق می توانید اشتراک های هلوگیت را خریداری نمایید.\n\nخرید با ووچر پرفکت مانی\nراهنمای خرید ووچر پرفکت مانی در 3 دقیقه\nhttps://t.me/hologate6/513\n\nخرید با رمز ارز\nراهنمای خرید با رمز ارز\nhttp://hologate4.com/crypto-payment")
                    # tel_send_message(chat_id,"https://hologate2.plus/xray/images/pages/buy-ssh/buy%20voucher%20cafearz.mp4 شما می توانید مثلا 2 دلار مطابق فیلم ذیل از کافه ارز بخرید و بعد در فروشگاه طبق فیلم بلافاصله اکانت را دریافت نمائید  ")
                    # tel_send_message(chat_id, cafeArzLink )
                    # tel_send_message(chat_id, select_payment+"\n"+tron )
                    # tel_send_message(chat_id, transaction_log_send)
                    
                elif txt == "پشتیبانی 🙋‍♀️":
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    tel_send_message(chat_id, fqf )
                    support(chat_id)
                elif txt == "چت با پشتیبان" or txt == "چت با کارشناس 💬":
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    tel_send_message(chat_id,"https://t.me/hologate5")
                    
                elif txt == "سئوالات متداول ❓":
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    tel_send_message(chat_id, fqf )
                        
                elif txt == "پرداخت وجه 💰":
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    
                    tel_send_message(chat_id,"از دو طریق می توانید اشتراک های هلوگیت را خریداری نمایید.\n\nخرید با ووچر پرفکت مانی\nراهنمای خرید ووچر پرفکت مانی در 3 دقیقه\nhttps://t.me/hologate6/513\n\nخرید با رمز ارز\nراهنمای خرید با رمز ارز\nhttp://hologate4.com/crypto-payment")
                    # tel_send_message(chat_id,"https://hologate2.plus/xray/images/pages/buy-ssh/buy%20voucher%20cafearz.mp4 \nشما می توانید مثلا 2 دلار مطابق فیلم ذیل از کافه ارز بخرید و بعد در فروشگاه طبق فیلم بلافاصله اکانت را دریافت نمائید  ")
                    # tel_send_message(chat_id, cafeArzLink )
                    # tel_send_message(chat_id, select_payment+"\n"+tron)
                    # tel_send_message(chat_id, transaction_log_send)
                #-------------------------------------------------------------
                #اگر در استیت کد تخیف باشد و هیچ کدام از کامندهای اصلی را وارد نکند، نوشته ی کاربر تحت عنوان کد تخفیف شناخته شده و دریافت میگردد و در بادی به سمت سرور فرستاده میشود.
                else:
                    servicenum=udata2[0]
                    providernum=udata2[1]
                    type=udata2[2].replace("-", "")
                    discount= txt
                    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
                    response = requests.post(env['buy-account'] , data={'servicenum':str(servicenum), 'providernum':str(providernum),'type':str(type), 'chat':str(chat_id), 'discount':str(discount)}, headers={'token':env['token']})
                    #response = requests.post('http://136.243.86.140:81/api/buy-account', data={'servicenum':str(servicenum), 'providernum':str(providernum),'type':str(type), 'chat':str(chat_id), 'vocher':str(vocher)}, headers={'token':'UGFGtZ.RkMfiqfy80O5EP0VoBiVrcs3GGcjJjGKAyr2UAxNtG'})
                    add_log(str(response.content), log_type='buy-account_with_discount_ssh')
                    if response.status_code == 200:
                        account= response.json() 
                        if "error1" in account:
                            tel_send_message(chat_id, str(account['error1']))
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                        elif "error2" in account:
                            tel_send_message(chat_id, str(account['error2']))
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                        elif "error3" in account:
                            tel_send_message(chat_id, str(account['error3']))
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                        elif "error4" in account:
                            tel_send_message(chat_id, str(account['error4']))
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                        elif "error5" in account:
                            tel_send_message(chat_id, str(account['error5']))
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                        elif "error6" in account:
                            tel_send_message(chat_id, str(account['error6']))
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                        elif "error7" in account:
                            tel_send_message(chat_id, str(account['error7']))
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                        elif "error8" in account:
                            tel_send_message(chat_id, str(account['error8']))
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                        else:
                        #در صورتی که از سمت سرور اروری دریافت نکنیم که همه ی انها در قسمت های بالایی چک شده اند، اکانت بااعمال کد تخفیف خریداریشده و اطلاعات ان به کاربر برمیگردد.
                            tel_send_message(chat_id, "کد تخفیف شما اعمال و "+str(account["message"])+"!")
                            #---------------------------------------------------
                            username = account["server"]["username"]
                            password = account["server"]["password"]
                            port = account["server"]["port"]
                            expiration_date = account["server"]["expiration_Date"]
                            serverAddress= account["server"]["serverAddress"]
                            number_of_devices= account["server"]["number_of_devices"]
                                
                            info_messages = [
                                            "نام کاربری:",
                                            f"{username}",
                                            "رمز عبور:",
                                            f"{password}",
                                            "پورت سرور:",
                                            f"{port}",
                                            "تاریخ انقضا:",
                                            f"{expiration_date}",
                                            "آدرس سرور",
                                            f"{serverAddress}",
                                            "تعداد دستگاه",
                                            f"{number_of_devices}",
                                            ]
                                
                            for info_message in info_messages:
                                payload = {
                                    'chat_id': chat_id,
                                    'text': info_message
                                }
                                
                                r = requests.post(url, json=payload)
                            #پس از خرید کامل اکانت و دریافت ان، مجددا استیت به حالت هوم آپدیت می شود.
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                    else:
                        tel_send_message(chat_id, "Server Error!")

        #اگر در استیت کد تخفیف برای خرید اکانت وی2ری باشد، این بخش اجرا میشود  
        elif state=="v_discount":
            if txt is not None:
                #مادامی که در استیت کد تخفیف باشد و یکی از کامندهای اصلی صدا زده شود، به استیت هوم آپدیت شده و انها اجرا می شوند، به جز اکانت تست که به استیت ایمیل اپدیت میشود واجرا میشود
                # tel_send_message(chat_id, str(udata2))
                if txt == "/start" or txt == "صفحه 1 📄":
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    start_send_button(chat_id)
                elif txt == "قیمت خدمات 💸":
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    tel_send_image(chat_id)
                    SendPrice(chat_id)
                elif "مدیریت اشتراک ها 🔒" in txt :
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    login(chat_id)
                #پس از انتخاب دکمه ی اکانت تست، از کاربر خواسته میشود ایمیلش را وارد کند 
                elif txt ==  "اکانت تست 🆓" :
                    new_state = "email"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'email')
                    tel_send_message(chat_id, 'برای دریافت اکانت تست فیلترشکن هلوگیت، ایمیل خود را وارد نمایید. \nاطلاعات کانکشن تست برای شما ارسال خواهد شد.' )
                
                elif "خرید اشتراک 🛒" in txt :
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    buy(chat_id)
                elif txt == "نرم افزارهای لازم 📲":
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    tel_send_message(chat_id, fq8)
                    
                elif (txt == "1 ماهه 2 دلار 🟢" or txt == "3 ماهه 5 دلار 🟢" or txt == "6 ماهه 10 دلار 🟢" or txt == "1 ساله 18 دلار 🟢"):  
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    
                    tel_send_message(chat_id,"از دو طریق می توانید اشتراک های هلوگیت را خریداری نمایید.\n\nخرید با ووچر پرفکت مانی\nراهنمای خرید ووچر پرفکت مانی در 3 دقیقه\nhttps://t.me/hologate6/513\n\nخرید با رمز ارز\nراهنمای خرید با رمز ارز\nhttp://hologate4.com/crypto-payment")
                    # tel_send_message(chat_id,"https://hologate2.plus/xray/images/pages/buy-ssh/buy%20voucher%20cafearz.mp4 شما می توانید مثلا 2 دلار مطابق فیلم ذیل از کافه ارز بخرید و بعد در فروشگاه طبق فیلم بلافاصله اکانت را دریافت نمائید  ")
                    # tel_send_message(chat_id, cafeArzLink )
                    # tel_send_message(chat_id, select_payment+"\n"+tron )
                    # tel_send_message(chat_id, transaction_log_send)
                    
                elif txt == "پشتیبانی 🙋‍♀️":
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    tel_send_message(chat_id, fqf )
                    support(chat_id)
                elif txt == "چت با پشتیبان" or txt == "چت با کارشناس 💬":
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    tel_send_message(chat_id,"https://t.me/hologate5")
                    
                elif txt == "سئوالات متداول ❓":
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    tel_send_message(chat_id, fqf )
                        
                elif txt == "پرداخت وجه 💰":
                    new_state = "home"
                    sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                    values = (new_state, chat_id)
                    mycursor.execute(sql, values)
                    db.get_commit()
                    result = mycursor.fetchone()
                    add_log(str(result), log_type=str(chat_id)+'home')
                    
                    tel_send_message(chat_id,"از دو طریق می توانید اشتراک های هلوگیت را خریداری نمایید.\n\nخرید با ووچر پرفکت مانی\nراهنمای خرید ووچر پرفکت مانی در 3 دقیقه\nhttps://t.me/hologate6/513\n\nخرید با رمز ارز\nراهنمای خرید با رمز ارز\nhttp://hologate4.com/crypto-payment")
                    # tel_send_message(chat_id,"https://hologate2.plus/xray/images/pages/buy-ssh/buy%20voucher%20cafearz.mp4 \nشما می توانید مثلا 2 دلار مطابق فیلم ذیل از کافه ارز بخرید و بعد در فروشگاه طبق فیلم بلافاصله اکانت را دریافت نمائید  ")
                    # tel_send_message(chat_id, cafeArzLink )
                    # tel_send_message(chat_id, select_payment+"\n"+tron)
                    # tel_send_message(chat_id, transaction_log_send)
                #-------------------------------------------------------------
                #اگر در استیت کد تخیف باشد و هیچ کدام از کامندهای اصلی را وارد نکند، نوشته ی کاربر تحت عنوان کد تخفیف شناخته شده و دریافت میگردد و در بادی به سمت سرور فرستاده میشو وپس از صحت سنجی کد؛ اطلاعات اکانت خریداری شده به کاربر بازمیگردد.
                else:
                    servicenum=udata3[0]
                    providernum=udata3[1]
                    type=udata3[2].replace("-", "")
                    discount= txt
                    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
                    response = requests.post(env['buy-account'] , data={'servicenum':str(servicenum), 'providernum':str(providernum),'type':str(type), 'chat':str(chat_id), 'discount':str(discount)}, headers={'token':env['token']})
                    #response = requests.post('http://136.243.86.140:81/api/buy-account', data={'servicenum':str(servicenum), 'providernum':str(providernum),'type':str(type), 'chat':str(chat_id), 'vocher':str(vocher)}, headers={'token':'UGFGtZ.RkMfiqfy80O5EP0VoBiVrcs3GGcjJjGKAyr2UAxNtG'})
                    add_log(str(response.content), log_type='buy-account_with_discount_v2ray')
                    if response.status_code == 200:
                        account= response.json() 
                        if "error1" in account:
                            tel_send_message(chat_id, str(account['error1']))
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                        elif "error2" in account:
                            tel_send_message(chat_id, str(account['error2']))
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                        elif "error3" in account:
                            tel_send_message(chat_id, str(account['error3']))
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                        elif "error4" in account:
                            tel_send_message(chat_id, str(account['error4']))
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                        elif "error5" in account:
                            tel_send_message(chat_id, str(account['error5']))
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                        elif "error6" in account:
                            tel_send_message(chat_id, str(account['error6']))
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                        elif "error7" in account:
                            tel_send_message(chat_id, str(account['error7']))
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                        elif "error8" in account:
                            tel_send_message(chat_id, str(account['error8']))
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                        else:
                        #در صورتی که از سمت سرور اروری دریافت نکنیم که همه ی انها در قسمت های بالایی چک شده اند، اکانت بااعمال کد تخفیف خریداری شده و اطلاعات ان به کاربر برمیگردد.
                            tel_send_message(chat_id, "کد تخفیف شما اعمال و "+str(account["message"])+"!")
                            tel_send_message(chat_id, str(account["message"]))
                            #---------------------------------------------------
                        #پس از خرید کامل اکانت و دریافت ان، مجددا استیت به حالت هوم آپدیت می شود.
                            new_state = "home"
                            sql = "UPDATE chat_states SET state = ? WHERE chat_id = ?"
                            values = (new_state, chat_id)
                            mycursor.execute(sql, values)
                            db.get_commit()
                            result = mycursor.fetchone()
                            add_log(str(result), log_type=str(chat_id)+'home')
                    else:
                        tel_send_message(chat_id, "Server Error!")

    return
       
#-----------------------------------------------------------------------------------------------------------------

# #تعریف تابع وبهوک برای هندل کردن تداخل فلاسک و اینلاین باتن            
def webhook():
    update = request.get_json()
    if "callback_query" in update:
        handle_callback(update)
    return "OK"
#-----------------------------------------------------------------------------------


@ app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #----------------------------------------------------------------
#فراخوانی وبهوک زمانی که متود از نوع پست است جهت هندل کردن تداخل فلاسک و دکمه های اینلاین
        webhook()
        #---------------------------------------------------------------
        msg = request.get_json() 
        try:

            chat_id, txt = tel_parse_message(msg)
            state_handling(chat_id,txt)
            #------------------------------------------------------
    
        except:
            try:
        # #-----------------------------------------------------------------------------------
                chat_id, file_id = tel_parse_get_message(msg)
                tel_upload_file(file_id)
                tel_send_message(chat_id,"فایل شما ذخیره شد")
            except Exception as e:
                print("from index-->" + str(e))
        return Response('ok', status=200)  
    else:
        return "<h1>Welcome!</h1>"
    return Response('ok', status=200)  


#-----------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run()