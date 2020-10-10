from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class CreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CreationForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
        #self.fields['username'].help_text = 'Имя пользователя и пароль не совпадают. Введите правильные данные.'
      #  self.fields['password1'].help_text=None


    class Meta(UserCreationForm.Meta):
        password2 = None
        model = User
        fields = ("first_name", "username", "email")


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)