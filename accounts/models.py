from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def send_email_to_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # def __str__(self):
    #     return self.get_full_name()


class TimeTable(models.Model):
    DAY_CHOICES = (
        ('SUN', 'Sunday'),
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednessday'),
        ('THU', 'Thursday')
    )
    day = models.CharField(_('day of the week'),
                           max_length=3, choices=DAY_CHOICES)
    time = models.CharField(_('time of the day'), max_length=5)

    def get_id(self):
        '''
        A unique Id by merging day and time
        '''
        return self.day + self.time

    def __str__(self):
        return self.get_id()


class Teacher(models.Model):
    DESIGNATION_CHOICES = (
        ('PR', 'Professor'),
        ('ASc', 'Associate Professor'),
        ('ASt', 'Assistant Professor'),
        ('LT', 'Lecturer'),

    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    priority = models.IntegerField(_('priority'), default=1)
    designation = models.CharField(max_length=3, choices=DESIGNATION_CHOICES)
    time_table = models.ManyToManyField(TimeTable, through='Engagement')

    class Meta:
        verbose_name = _('teacher')
        verbose_name_plural = _('teachers')

    def __str__(self):
        return self.user.get_full_name()


class Engagement(models.Model):
    STATUS_CHOICES = (
        ('ACT', 'ACTIVE'),
        ('ENG', 'ENGAGED')
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    time_table = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
    status = models.CharField(
        _("active status"), max_length=3, choices=STATUS_CHOICES)

    class Meta:
        unique_together = [['teacher', 'time_table']]

    def __str__(self):
        return self.teacher.user.get_short_name() + "_" + self.time_table.get_id()


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    reg_no = models.CharField(_("registration number"), max_length=15)
    semester = models.CharField(_("semester"), max_length=5)
    session = models.CharField(_("session"), max_length=10)
    section = models.CharField(_("section"), max_length=3)

    class Meta:
        verbose_name = _('student')
        verbose_name_plural = _('students')
