import json
import telebot

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from listam_bot.settings import BOT_TOKEN, NGROK_IP
from .models import Subscription

WEBHOOK_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/setwebhook?url=https://{NGROK_IP}/"
#https://api.telegram.org/bot5264023566:AAG_N4w6aNc45yOE0fHiLzMC17dpJK88-6U/setwebhook?url=https://e4b9-46-71-44-15.eu.ngrok.io/

bot = telebot.TeleBot(BOT_TOKEN)


@csrf_exempt
def web_hook(request):
    print(123, request.body)
    json_string = request.body.decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return HttpResponse()


# @csrf_exempt
# def web_hook(request):
#     print(123)
#     payload = json.loads(request.body.decode('utf-8'))
#     update = telebot.types.Update.de_json(payload)
#     bot.process_new_updates([update])
#     return HttpResponse()


@csrf_exempt
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Hi user!')
    bot.send_message(message.chat.id, "Please /subscribe or /unsubscribe")


@csrf_exempt
@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    Subscription.get_or_create(chat_id=int(message.chat.id))


@csrf_exempt
@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    try:
        subscription = Subscription.objects.get(chat_id=message.chat.id)
        subscription.delete()
    except Subscription.DoesNotExist:
        pass
