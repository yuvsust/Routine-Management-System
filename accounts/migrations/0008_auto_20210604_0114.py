# Generated by Django 3.1.7 on 2021-06-03 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210604_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='designation',
            field=models.CharField(blank=True, choices=[('PR', 'Professor'), ('ASc', 'Associate Professor'), ('ASt', 'Assistant Professor'), ('LT', 'Lecturer')], default='Lecturer', max_length=3),
        ),
    ]
