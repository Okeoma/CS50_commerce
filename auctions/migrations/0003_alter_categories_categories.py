# Generated by Django 3.2.6 on 2021-10-14 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_user_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='categories',
            field=models.CharField(choices=[('Electronics', 'Electronics'), ('Books', 'Books'), ('Fashion', 'Fashion'), ('Household', 'Household'), ('Food', 'Food')], max_length=68),
        ),
    ]
