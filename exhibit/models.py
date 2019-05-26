from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone



class Photo(models.Model):
    add_date = models.DateTimeField(auto_now_add=True)
    photo_title = models.CharField(max_length=100)
    photo_file = models.FileField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    photo_like = models.IntegerField(default=0)

    def was_published_recently(self):
        return self.add_date >= timezone.now() - datetime.timedelta(days=1)


    def __str__(self):
        return self.photo_title

class Like(models.Model):
    like_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    like_photo = models.ForeignKey(Photo, on_delete=models.CASCADE, blank=True)

class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name="rel_from_set", on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name="rel_to_set", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} obserwuje {}'.format(self.user_from, self.user_to)

User.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name="followers", symmetrical=False))

class SendMessage(models.Model):
    userfrom = models.ForeignKey(User, related_name="rel_from", on_delete=models.CASCADE)
    useremail = models.EmailField(default='type@youremail.here')
    msgtitle = models.CharField(max_length=100, default="Wiadomość ze strony")
    msg = models.TextField()
    senton = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Wiadomość od {} wysłana {}, temat: {} '.format(self.userfrom, self.senton, self.msgtitle)


class NewsletterUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    useremail = models.EmailField(default='type@yourmail.here')
    rodo = models.BooleanField(default=False, blank=False, verbose_name="Czy zgadasz się na newsletter?")
    news_from = models.DateTimeField(auto_now_add=True)


class InMail(models.Model):
    from_user = models.ForeignKey(User, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE)
    send = models.DateTimeField(auto_now_add=True, db_index=True)
    title_txt = models.CharField(max_length=100, default="Nowa wiadomość InMail")
    message_txt = models.TextField()