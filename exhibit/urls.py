from django.urls import path
from . import views


urlpatterns = [

    path('', views.index, name='index'),
    path('user/<username>', views.user, name='user'),
    path('me/', views.me, name='me'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_request, name='login'),
    path("logout", views.logout_request, name="logout"),
    path("add/", views.photo_add, name="photo-add"),
    path("search/", views.search, name="search"),
    path("follow/", views.follow, name="follow"),
    path("contacts/", views.contacts, name="contacts"),
    path("contact_form/", views.send_message, name="send_message"),
    path("newsletter/", views.newsletter, name="newsletter"),
    path("inmails/", views.inmails, name="inmails"),
    path("inmail/<int:inmail_id>", views.inmail, name="inmail"),



]

