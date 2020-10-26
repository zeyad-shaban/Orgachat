from . import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('', views.profile, name="profile"),
    path('view/<int:user_id>', views.view_user, name="view_user"),
    path('all/', views.all_users, name='all_users'),
    path('add-friend/<int:user_id>/', views.add_friend, name='add_friend'),
    path('remove-friend/<int:user_id>/',
         views.remove_friend, name='remove_friend'),
    path("about/", views.about, name="about"),
    path('search_users/', views.search_users, name="search_users"),
]
