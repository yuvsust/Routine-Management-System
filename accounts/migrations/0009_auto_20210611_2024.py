# Generated by Django 3.1.7 on 2021-06-11 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210604_0114'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Engagement',
            new_name='TeacherEngagement',
        ),
    ]