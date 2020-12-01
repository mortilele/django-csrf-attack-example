from django.contrib import admin
from core.models import Account, Transaction


# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'balance', 'created_at', 'modified_at')
    list_display = ('id', 'user', 'balance', 'created_at', 'modified_at')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('sender_user', 'receiver_user', 'amount', 'created_at', 'modified_at')
    list_display = ('id', 'sender_user', 'receiver_user', 'amount', 'created_at', 'modified_at')
