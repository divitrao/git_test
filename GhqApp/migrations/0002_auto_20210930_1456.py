# Generated by Django 3.2.7 on 2021-09-30 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GhqApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserAnswer',
            new_name='QuizAttemptAnswer',
        ),
        migrations.AddField(
            model_name='options',
            name='marks',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
