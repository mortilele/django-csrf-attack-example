# Create your views here.
from django.db.models import Q
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from core.serializers import AccountSerializer, TransactionSerializer, CreateTransactionSerializer
from core.models import Account, Transaction


class AccountViewSet(mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        return self.request.user.account

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class TransactionViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return self.queryset.filter(Q(sender_user=self.request.user) | Q(receiver_user=self.request.user))

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTransactionSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        print(self.request.user)
        return serializer.save(sender_user=self.request.user)
