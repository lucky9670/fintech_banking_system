# Generated by Django 4.2.6 on 2023-10-08 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(upload_to='company/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='aadhar_card_back',
            field=models.ImageField(blank=True, null=True, upload_to='member/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='aadhar_card_front',
            field=models.ImageField(blank=True, null=True, upload_to='member/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gstin_pic',
            field=models.ImageField(blank=True, null=True, upload_to='member/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='pan_card_pic',
            field=models.ImageField(blank=True, null=True, upload_to='member/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='member/'),
        ),
    ]
