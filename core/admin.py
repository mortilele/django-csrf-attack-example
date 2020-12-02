from django.contrib import admin
from core.models import Account, Transaction


# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    icon_name = 'account_balance'
    readonly_fields = ('user', 'balance', 'created_at', 'modified_at')
    list_display = ('id', 'user', 'balance', 'created_at', 'modified_at')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    icon_name = 'attach_money'
    readonly_fields = ('status', 'sender_user', 'receiver_user', 'amount', 'created_at', 'modified_at')
    list_display = ('id', 'sender_user', 'receiver_user', 'amount', 'status', 'created_at', 'modified_at')
    list_filter = ('status', )
