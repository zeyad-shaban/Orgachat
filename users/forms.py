from django.core.exceptions import ImproperlyConfigured
from django.forms import ModelForm
from django.contrib.auth import get_user_model
User = get_user_model()

class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'avatar', 'bio', 'country')