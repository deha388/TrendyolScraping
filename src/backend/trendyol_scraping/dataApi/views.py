from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from dataApi.models import DataToFetch
from dataApi.serializers import DataToFetchSerializer
import requests
from bs4 import BeautifulSoup
# Create your views here.

def fetch_data(url_to_req: str):
    r = requests.get(url=url_to_req)
    soup = BeautifulSoup(r.content, features="html.parser")
    data_to_scraped = {
        "ProductName": soup.find(class_="pr-new-br").find('span').text,
        "BrandName":soup.find(class_="pr-new-br").find(href=True).text,
        "Price":soup.find(class_="prc-dsc").text,
        "Category": soup.find(class_="category-gender-desc").text,
        "MerchantName":soup.find(class_="merchant-text").text,
        "MerchantScore":"None",
        "OtherMerchant":','.join([element.text for element in soup.find_all(class_="seller-container")])
    }
    return data_to_scraped

@csrf_exempt
def add_data(request, id=0):
    if request.method=='GET':
        employees = DataToFetch.objects.all()
        employees_serializer=DataToFetchSerializer(employees,many=True)
        return JsonResponse(employees_serializer.data,safe=False)
    if request.method == 'POST':
        fetched_data= JSONParser().parse(request)

        data_to_save = fetch_data(url_to_req=fetched_data['url'])
        data_serializer=DataToFetchSerializer(data=data_to_save)

        if data_serializer.is_valid():
            data_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Failed to Add",safe=False)