from rest_framework import serializers
from dataApi.models import DataToFetch

class DataToFetchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataToFetch
        fields = ('ScrapedId','ProductName','BrandName','Price','Category','MerchantName','MerchantScore','OtherMerchant')