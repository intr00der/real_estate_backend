# Generated by Django 3.1.7 on 2021-04-10 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionalestateimage',
            name='title',
            field=models.CharField(default='image', max_length=50),
            preserve_default=False,
        ),
    ]
