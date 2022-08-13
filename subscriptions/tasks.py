import json

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from listam_bot.celery import app
from subscriptions.models import Subscription
from spider import crawl_and_send_new_ads_to_user


def add_crawling_task(subscription_id):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=120,
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.create(
        interval=schedule,
        name="Send new ads for subscription {}".format(subscription_id),
        task="subscriptions.tasks.send_new_ads",
        kwargs=json.dumps({"subscription_id": subscription_id}),
    )


def remove_crawling_task(subscription_id):
    PeriodicTask.objects.filter(
        name="Send new ads for subscription {}".format(subscription_id)
    ).delete()


@app.task
def send_new_ads(subscription_id):
    subscription = Subscription.objects.get(id=subscription_id)
    crawl_and_send_new_ads_to_user(
        chat_id=subscription.chat_id,
        last_ad=subscription.last_ad,
        subscription_id=subscription_id,
    )
