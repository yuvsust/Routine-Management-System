from django.db import models
from accounts.models import Teacher, TimeTable
from django.utils.translation import ugettext_lazy as _


class CourseManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('preference', 'course_code')
        return queryset


class Course(models.Model):
    TYPE_CHOICES = (
        ('THEORY', 'Theory'),
        ('LAB', 'Lab')
    )

    PREFERENCE_CHOICES = (
        ('MAJOR', 'Major'),
        ('MINOR', 'Non-Major')
    )

    SEMESTER_CHOICES = (
        ('11', '1/1'),
        ('12', '1/2'),
        ('21', '2/1'),
        ('22', '2/2'),
        ('31', '3/1'),
        ('32', '3/2'),
        ('41', '4/1'),
        ('42', '4/2'),
    )

    course_name = models.CharField(_('Course Name'), max_length=60)
    course_code = models.CharField(
        _('Course Code'), max_length=10, unique=True)
    course_type = models.CharField(
        _('Course Type'), max_length=6, choices=TYPE_CHOICES)
    course_credit = models.DecimalField(
        _('Course Credit'), max_digits=2, decimal_places=1)
    preference = models.CharField(
        _('Department Preference'), max_length=5, choices=PREFERENCE_CHOICES)
    semester = models.CharField(
        _('Semester'), max_length=2, choices=SEMESTER_CHOICES)
    teacher = models.ForeignKey(Teacher, on_delete=models.RESTRICT)
    objects = CourseManager()

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')

    def __str__(self):
        return self.course_code


class Room(models.Model):
    TYPE_CHOICES = (
        ('THEORY', 'Theory'),
        ('LAB', 'Lab')
    )

    room_id = models.CharField(max_length=8, unique=True)
    room_type = models.CharField(
        _('Room Type'), max_length=6, choices=TYPE_CHOICES)
    time_table = models.ManyToManyField(
        TimeTable, through='RoomEngagement', blank=True)

    class Meta:
        verbose_name = _('room')
        verbose_name_plural = _('rooms')

    def __str__(self):
        return self.room_id


class RoomEngagement(models.Model):
    STATUS_CHOICES = (
        ('FREE', 'FREE'),
        ('ENG', 'ENGAGED')
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    time_table = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
    status = models.CharField(
        _("Engagement Status"), max_length=4, choices=STATUS_CHOICES)

    class Meta:
        unique_together = [['room', 'time_table']]

    def __str__(self):
        return self.room.room_id + "_" + self.time_table.get_id()


class Class(models.Model):
    SEMESTER_CHOICES = (
        ('11', '1/1'),
        ('12', '1/2'),
        ('21', '2/1'),
        ('22', '2/2'),
        ('31', '3/1'),
        ('32', '3/2'),
        ('41', '4/1'),
        ('42', '4/2'),
    )
    DAY_CHOICES = (
        ('SUN', 'Sunday'),
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednessday'),
        ('THU', 'Thursday')
    )
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('POSTPOND', 'Postpond')
    )

    semester = models.CharField(
        _('Semester'), max_length=2, choices=SEMESTER_CHOICES)
    day = models.CharField(_('day of the week'),
                           max_length=3, choices=DAY_CHOICES)
    time = models.CharField(_('time of the day'), max_length=5)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=9, choices=STATUS_CHOICES, default='SCHEDULED')

    class Meta:
        verbose_name = _('class')
        verbose_name_plural = _('classes')

    def __str__(self):
        return self.course.course_code + "_" + self.room.room_id + "_" + self.day + self.time
