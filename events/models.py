from django.db import models
from datetime import date


class Organization(models.Model):
    """
    Class describing the fields of the "Organization" object 
    in the database
    """
    title = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Название организации'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание организации'
    )
    address = models.CharField(
        max_length=128,
        verbose_name='Адрес организации'
    )
    postcode = models.CharField(
        max_length=6,
        verbose_name='Почтовый индекс'
    )

    def __str__(self) -> str:
        return self.title

    class Meta():
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Event(models.Model):
    """
    Class describing the fields of the "Ivent" object 
    in the database
    """
    title = models.CharField(
        max_length=128,
        verbose_name='Название мероприятия'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание мероприятия'
    )
    organizations = models.ManyToManyField(
        Organization,
        through='Organization_Event',
        verbose_name='Организовывающие организации'
    )
    image = models.ImageField(
        upload_to='events_images',
        verbose_name='Афиша мероприятия'
        )
    date = models.DateField(
        default=date.today,
        verbose_name='Дата проведения мероприятия'
        )

    def __str__(self) -> str:
        return self.title
    
    class Meta():
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    
class Organization_Event(models.Model):
    """
    Class describing the fields of the "Organization_Ivent" object 
    in the database
    To implement the connection of several organizations with one ivent.
    """        
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Организатор мероприятия {self.event_id} - {self.organization_id}'
    
    class Meta():
        verbose_name = 'Связь организации и мероприятия'
        verbose_name_plural = 'Cвязи организацией и мероприятий'     