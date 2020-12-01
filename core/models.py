from django.db import models, transaction
from django.contrib.auth.models import User

# Create your models here.
from core import constants


class AccountManager(models.Manager):

    def deposit(self, user, amount):
        if amount < 0:
            return None

        if not self.filter(user=user).exists():
            self.create(user=user)

        with transaction.atomic():
            account = self.select_for_update().get(user=user)
            account.balance += amount
            account.save(update_fields=[
                'balance',
            ])
        return account

    def withdraw(self, user, amount):
        if amount < 0:
            return None

        if not self.filter(user=user).exists():
            self.create(user=user)

        with transaction.atomic():
            account = self.select_for_update().get(user=user)
            if account.balance - amount < 0:
                print('balance can not be less than ')
                return None
            account.balance -= amount
            account.save(update_fields=[
                'balance',
            ])
        return account

    def make_transaction(self, sender_user, receiver_user, amount):
        try:
            sender_account = self.withdraw(sender_user, amount)
            receiver_account = self.deposit(receiver_user, amount)
            if sender_account and receiver_account:
                return constants.SUCCESS
            return constants.FAILURE
        except Exception as e:
            print(str(e))
            return constants.FAILURE


class Account(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='account',
                                verbose_name='Пользователь')
    balance = models.PositiveIntegerField(verbose_name='Баланс пользователя', default=0)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    modified_at = models.DateTimeField(blank=True, auto_now=True)

    objects = AccountManager()

    class Meta:
        verbose_name = 'Баланс пользователя'
        verbose_name_plural = 'Баланс пользователя'

    def __str__(self):
        return f'{self.user} - {self.balance}'


class Transaction(models.Model):
    sender_user = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    related_name='withdrawn_transactions',
                                    verbose_name='Отправитель транзакции')
    receiver_user = models.ForeignKey(User,
                                      on_delete=models.CASCADE,
                                      related_name='deposited_transactions',
                                      verbose_name='Приниматель транзакции')
    amount = models.IntegerField()
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    modified_at = models.DateTimeField(blank=True, auto_now=True)
    status = models.CharField(verbose_name='Статус',
                              max_length=20,
                              choices=constants.TRANSACTION_STATUSES,
                              default=constants.CREATED)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return f'{self.sender_user} -> {self.receiver_user} : {self.amount}'

    def save(self, **kwargs):
        if self.status == constants.CREATED:
            self.status = Account.objects.make_transaction(self.sender_user, self.receiver_user, self.amount)
        super().save(**kwargs)
