from django import forms
from .models import Photo, SendMessage, NewsletterUsers, InMail

class PostForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('photo_title', 'photo_file')

class MsgForm(forms.ModelForm):
    class Meta:
        model = SendMessage
        fields = ('useremail', 'msgtitle', 'msg')


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterUsers
        fields = ('useremail', 'rodo')

class InMailForm(forms.ModelForm):
    class Meta:
        model = InMail
        fields = ('to_user', 'title_txt', 'message_txt')