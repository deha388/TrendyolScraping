# Generated by Django 3.2.16 on 2022-12-08 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataToFetch',
            fields=[
                ('ScrapedId', models.AutoField(primary_key=True, serialize=False)),
                ('ProductName', models.CharField(max_length=500)),
                ('BrandName', models.CharField(max_length=500)),
                ('Price', models.CharField(max_length=500)),
                ('Category', models.CharField(max_length=500)),
                ('MerchantName', models.CharField(max_length=500)),
                ('MerchantScore', models.CharField(max_length=500)),
                ('OtherMerchant', models.CharField(max_length=500)),
            ],
        ),
    ]