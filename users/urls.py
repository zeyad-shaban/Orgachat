from . import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    # ------------Users------------
    path('', views.profile, name="profile"),
    path('view/<int:user_id>/', views.view_user, name="view_user"),
    path('all/', views.all_users, name='all_users'),
    # ----------Actions------------
    path('add-friend/<int:user_id>/', views.add_friend, name='add_friend'),
    path('remove-friend/<int:user_id>/',
         views.remove_friend, name='remove_friend'),
    # ------------Auth Validation--------------–
    path("send_validation/", views.send_validation, name="send_validation"),
    path("check_validation/", views.check_validation, name="check_validation"),
    # ----------About-------------
    path("about/", views.about, name="about"),
]
