from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from dataApi.models import DataToFetch
from dataApi.serializers import DataToFetchSerializer
import requests
from bs4 import BeautifulSoup


# Create your views here.

def create_connection(url_to_req):
    r = requests.get(url=url_to_req)
    soup = BeautifulSoup(r.content, features="html.parser")
    return soup


def fetch_data(url_to_req: str):
    soup = create_connection(url_to_req=url_to_req)

    data_to_scraped = {
        "ProductName": soup.find(class_="pr-new-br").find('span').text,
        "BrandName": soup.find(class_="pr-new-br").find(href=True).text,
        "Price": soup.find(class_="prc-dsc").text,
        "Category": soup.find(class_="category-gender-desc").text,
        "Merchant": {
            "MerchantName": "",
            "MerchantScore": "",
            "MerchantCity": ""
        },
        "OtherMerchant": []
    }

    base_url = "https://www.trendyol.com/magaza/profil/"
    merchant = soup.find(class_="merchant-text")
    data_to_scraped["Merchant"]["MerchantName"] = merchant.text

    new_req = base_url + merchant["href"].split("/")[-1]
    soup1 = create_connection(url_to_req=new_req)

    data = soup1.find(class_="seller-store__score score-actual ss-header-score").text
    data_to_scraped["Merchant"]["MerchantScore"] = data

    data = soup1.find_all(class_="seller-info-container__wrapper__text-container__value")
    data_to_scraped["Merchant"]["MerchantCity"] = data[1].text

    other_merchant = [element for element in soup.find_all(class_="seller-container")]

    for element in other_merchant:
        other_merc = {}
        other_merc["name"] = element.text
        t = element.text.lower().replace("ı", "i").replace(" ", "-") + "-m-" + \
            element.find('a', href=True)["href"].split("=")[-1]
        new_req = base_url + t
        soup1 = create_connection(url_to_req=new_req)
        data = soup1.find(class_="seller-store__score score-actual ss-header-score").text
        other_merc["score"] = data

        data = soup1.find_all(class_="seller-info-container__wrapper__text-container__value")
        other_merc["city"] = data[1].text
        data_to_scraped["OtherMerchant"].append(other_merc)

    data_to_scraped["OtherMerchant"] = str(data_to_scraped["OtherMerchant"])
    data_to_scraped["Merchant"] = str(data_to_scraped["Merchant"])

    return data_to_scraped


@csrf_exempt
def add_data(request):
    if request.method == 'GET':
        employees = DataToFetch.objects.all()
        employees_serializer = DataToFetchSerializer(employees, many=True)
        return JsonResponse(employees_serializer.data, safe=False)
    if request.method == 'POST':
        fetched_data = JSONParser().parse(request)

        data_to_save = fetch_data(url_to_req=fetched_data['url'])
        data_serializer = DataToFetchSerializer(data=data_to_save)

        if data_serializer.is_valid():
            data_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
