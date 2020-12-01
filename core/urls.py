from django.conf.urls import url
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from core import views

router = routers.DefaultRouter()

router.register(r'accounts', views.AccountViewSet)
router.register(r'transactions', views.TransactionViewSet)

urlpatterns = [
    url(r'^docs/', include_docs_urls(
        title='CSRF api docs',
        authentication_classes=[],
        permission_classes=[]))
]

urlpatterns += router.urls
