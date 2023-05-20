from django.contrib import admin
from rest_framework import routers
from django.urls import include, path

from webdav.accounts import views as accounts_views
from webdav.contacts import views as contacts_views


accounts_router = routers.DefaultRouter()
accounts_router.register(r"accounts", accounts_views.UsersViewSet)

contacts_router = routers.DefaultRouter()
contacts_router.register(r"contacts", contacts_views.ContactsViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(accounts_router.urls)),
    path("", include(contacts_router.urls)),
]
