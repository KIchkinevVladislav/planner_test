from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model

User = get_user_model()

class Group(models.Model):
    """
    Class describing the fields of the "Group (group chat)" object 
    in the database
    """
    uuid = models.UUIDField(default=uuid4, editable=False, verbose_name='Идентификатор чата')
    members = models.ManyToManyField(User, verbose_name='Участники')
	
    def add_user(self, request, user):
        self.members.add(user)
        self.save()
        return

    def remove_user(self, request, user):
        self.members.remove(user)
        self.save()
        return
    
    def __str__(self):
        return f'{self.uuid}'

    class Meta:
            verbose_name = 'Групповой чат'
            verbose_name_plural = 'Групповые чаты'  


class Message(models.Model):
    """
    Class describing the fields of the "Message" object 
    in the database
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки')
    content = models.TextField(verbose_name='Текст сообщения')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Идентификатор чата')

    def __str__(self):
        return f'Сообшение из чата {self.group}: {self.content}. Время отправки {self.timestamp}'
    
    class Meta:
            verbose_name = 'Сообщение'
            verbose_name_plural = 'Сообщения' 