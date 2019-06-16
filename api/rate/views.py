import datetime

import requests
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from rate.models import Price

APP_ID = "c6f23902babe4392adbe0ca00a08f8e1"


class CurrencyView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        currencies = requests.get("https://openexchangerates.org/api/currencies.json")
        currencies = currencies.json()
        return Response(currencies, status=status.HTTP_200_OK)


class PriceView(CreateAPIView):
    """
    Takes input price on a date range and saves them in the database.
    """
    def create(self, request, *args, **kwargs):
        date_from = self.request.data.get("date_from")
        date_to = self.request.data.get("date_to")

        try:
            date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d")
            date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d")

            if date_to < date_from:
                raise ValueError("date_to must be greater than or equal to date_from.")
        except ValueError as e:
            return Response(
                {"message": e.args[0]},
                status=status.HTTP_400_BAD_REQUEST)

        delta = date_to - date_from
        date_list = [date_from + datetime.timedelta(days=i) for i in range(delta.days + 1)]

        origin_code = self.request.data.get("origin_code")
        destination_code = self.request.data.get("destination_code")
        price = self.request.data.get("price")
        currency = self.request.data.get("currency", "USD").upper()

        resp = requests.get(
            "https://openexchangerates.org/api/latest.json?app_id={0}".
            format(APP_ID)).json()
        rates = resp.get("rates")
        rate = rates.get(currency)
        price_in_usd = int(price/rate)

        price_list = []
        price_obj = Price.objects.last()
        latest_id = 1 if not price_obj else price_obj.pk + 1

        for day in date_list:
            obj = {
                "id": latest_id,
                "orig_code": origin_code,
                "dest_code": destination_code,
                "price": price_in_usd,
                "day": day
            }
            price_list.append(Price(**obj))
            latest_id += 1

        Price.objects.bulk_create(price_list)

        return Response(
            {"message": "Successfully saved prices."},
            status=status.HTTP_201_CREATED)
