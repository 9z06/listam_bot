import json
import telebot

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator

from listam_bot.settings import BOT_TOKEN, NGROK_IP
from .models import Subscription
from .tasks import add_crawling_task, remove_crawling_task

WEBHOOK_URL = (
    f"https://api.telegram.org/bot{BOT_TOKEN}/setwebhook?url=https://{NGROK_IP}/"
)

bot = telebot.TeleBot(BOT_TOKEN)


@method_decorator(csrf_exempt, name="dispatch")
class ProcessHookView(View):
    def post(self, request, *args, **kwargs):
        json_string = json.loads(request.body)
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return HttpResponse()


@csrf_exempt
@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "Hi user!")
    bot.send_message(message.chat.id, "Please /subscribe or /unsubscribe")


@csrf_exempt
@bot.message_handler(commands=["subscribe"])
def subscribe(message):
    subscription, created = Subscription.objects.get_or_create(
        chat_id=int(message.chat.id)
    )
    add_crawling_task(subscription.id)
    if created:
        bot.send_message(message.chat.id, "You subscribed")
    else:
        bot.send_message(message.chat.id, "Subscription was already created")


@csrf_exempt
@bot.message_handler(commands=["unsubscribe"])
def unsubscribe(message):
    try:
        subscription = Subscription.objects.get(chat_id=message.chat.id)
        remove_crawling_task(subscription.id)
        subscription.delete()
        bot.send_message(message.chat.id, "You unsubscribed")
    except Subscription.DoesNotExist:
        bot.send_message(message.chat.id, "You don't have subscription")
        pass
