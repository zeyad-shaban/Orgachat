"""orgachat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from chat import views as chat_views
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webpush/', include('webpush.urls')),
    path('', chat_views.home, name="home"),
    # Service Worker PWA
    path('sw.js', TemplateView.as_view(template_name='chat/sw.js',
                                       content_type='application/javascript'), name='sw.js',),
    path('random-response', chat_views.random_response),

    # Include
    path('users/', include('users.urls')),
    path('chat/', include('chat.urls')),
    path("info/", include("info.urls")),

    # AUTHENTICATION
    path('signup/', users_views.signupuser, name="signupuser"),
    path('login/', users_views.loginuser, name="loginuser"),
    path('logout/', users_views.logoutuser, name="logoutuser"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
