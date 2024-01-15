from django.db import models
from datetime import date
from django.contrib.auth.models import Group, Permission, AbstractBaseUser, PermissionsMixin, BaseUserManager

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
    Class describing the fields of the "Organization_Event" object 
    in the database
    To implement the connection of several organizations with one event.
    """        
    event_id = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE
    )
    organization_id = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return  f'Организатор мероприятия {self.event_id} - {self.organization_id}'
    
    class Meta():
        verbose_name = 'Связь организации и мероприятия'
        verbose_name_plural = 'Cвязи организацией и мероприятий'  



class UserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError()
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Class describing the fields of the "User" object 
    in the database
    """

    email = models.EmailField(unique=True, blank=False, verbose_name='Электронная почта')
    first_name = models.CharField(max_length=25, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=25, blank=True, null=True, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=12, blank=True, null=True, verbose_name='Номер телефона')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Организация, в которой работает пользователь')
    is_staff = models.BooleanField(default=False, verbose_name='Статус персонала сервиса')

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    class Meta:
            verbose_name = 'Пользователь'
            verbose_name_plural = 'Пользователи'


# class Events_User(models.Model):
#     """
#     Class describing the fields of the "Events_User" object 
#     in the database
#     To implement the connection of several enents with one user.
#     """        
#     event_id = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

#     def __str__(self) -> str:
#         return  f'{self.user_id} участвует в создании мероприятия {self.event_id}'
    
#     class Meta():
#         verbose_name = 'Связь участника организации и мероприятия'
#         verbose_name_plural = 'Cвязи участников организаций и мероприятий'   
