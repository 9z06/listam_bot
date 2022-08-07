from django.contrib import admin
from .models import Subscription

# Register your models here.


class AdminSubscription(admin.ModelAdmin):
    list_display = ('pk', 'chat_id', 'last_ad')


admin.site.register(Subscription, AdminSubscription)
