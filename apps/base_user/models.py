from django.contrib.auth.base_user import BaseUserManager

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta


USER_MODEL = settings.AUTH_USER_MODEL

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class MyUser(AbstractBaseUser, PermissionsMixin):
    class Types(models.TextChoices):
        MODERATOR = "moderator", _('Moderator')
        REGULAR = "regular", _('Sadə')

    type = models.CharField(_('İstifadəçi tipi'), max_length=55, choices=Types.choices, default=Types.REGULAR,
                            editable=False)

    email = models.EmailField(_('Email Address'), unique=True, error_messages={
        'unique': _("A user with that email already exists."),
    })

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        }, null=True, blank=True
    )

    first_name = models.CharField(_('First Name'), max_length=50, default='')
    last_name = models.CharField(_('Last Name'), max_length=150, default='')
    phone = models.CharField(_('Phone Number'), max_length=25, default='+994(55) 555 55 55',
                             help_text='+994(55) 555 55 55')

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as active. ''Unselect this instead of deleting accounts.'), )
    date_joined = models.DateTimeField(_('date joined'), auto_now=True)
    last_password_forgot_request = models.DateTimeField(_('Last password request date'), auto_now_add=True)

    showed_password = models.CharField(_('Parol (Gorunen)'), max_length=250, null=True, blank=True)

    objects = CustomUserManager()
    EMAIL_FIELD = 'username'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def user_fields_by_type(self):
        if self.type == self.Types.REGULAR:
            return self.regular_user_fields
        return None

    def __str__(self):
        try:
            return f'Email : {self.email} - - - Tel : {self.user_fields_by_type.phone} - - - Istifadəçi tipi : {self.get_type_display()}'
        except:
            return f'Moderator : {self.first_name}'

User = MyUser()
