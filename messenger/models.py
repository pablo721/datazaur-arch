from django.db import models
import datetime


class Message(models.Model):
    sender = models.ForeignKey('website.Account', on_delete=models.CASCADE, unique=False, related_name='message_sender')
    recipient = models.ForeignKey('website.Account', on_delete=models.CASCADE, unique=False,
                                  related_name='message_recipient')
    content = models.TextField(max_length=1000, blank=False)
    timestamp = models.DateTimeField()
    delivered = models.BooleanField(default=False)
    read = models.BooleanField(default=False)


    def __str__(self):
        return str(self.timestamp) + ' ' + self.sender.username + ': ' + str(self.content)

