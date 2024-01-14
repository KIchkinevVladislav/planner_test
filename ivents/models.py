from django.db import models


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

    class Meta():
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'