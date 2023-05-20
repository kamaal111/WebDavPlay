from django.contrib import admin
from rest_framework import routers
from django.urls import include, path

from webdav.accounts import views as accounts_views


accounts_router = routers.DefaultRouter()
accounts_router.register(r"accounts", accounts_views.UserViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(accounts_router.urls)),
]
