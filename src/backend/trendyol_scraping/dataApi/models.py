from django.db import models

class DataToFetch(models.Model):
    ScrapedId = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=500)
    BrandName = models.CharField(max_length=500)
    Price = models.CharField(max_length=500)
    Category = models.CharField(max_length=500)
    MerchantName = models.CharField(max_length=500)
    MerchantScore = models.CharField(max_length=500)
    OtherMerchant = models.CharField(max_length=500)
