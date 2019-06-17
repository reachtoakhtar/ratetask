import datetime

import requests
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response

from rate.models import Price, Region, Port

APP_ID = "c6f23902babe4392adbe0ca00a08f8e1"


class CurrencyView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        currencies = requests.get("https://openexchangerates.org/api/currencies.json")
        currencies = currencies.json()
        return Response(currencies, status=status.HTTP_200_OK)


class PopulateDBView(CreateAPIView):
    def create(self, request, *args, **kwargs):
        china_main, created = Region.objects.get_or_create(slug="china_main", name="China Main", parent_slug=None)
        northern_europe, created = Region.objects.get_or_create(slug="northern_europe", name="Northern Europe", parent_slug=None)
        scandinavia = Region.objects.create(slug="scandinavia", name="Scandinavia", parent_slug=northern_europe)
        norway_north_west = Region.objects.create(slug="norway_north_west", name="Norway North East", parent_slug=scandinavia)
        norway_south_east = Region.objects.create(slug="norway_south_east", name="Norway South East", parent_slug=scandinavia)
        norway_south_west = Region.objects.create(slug="norway_south_west", name="Norway South West", parent_slug=scandinavia)

        Port.objects.create(code="NOFRK", name="Fredrikstad", parent_slug=norway_south_east)
        Port.objects.create(code="NOFUS", name="Fusa", parent_slug=scandinavia)
        Port.objects.create(code="NOSVG", name="Stavanger", parent_slug=norway_south_west)
        Port.objects.create(code="FRLRH", name="La Rochelle", parent_slug=norway_north_west)
        Port.objects.create(code="CNNBO", name="Ningbo", parent_slug=china_main)

        return Response(
            {"message": "Successfully populated db."},
            status=status.HTTP_201_CREATED)


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

        try:
            origin_code = Port.objects.get(pk=origin_code)
            destination_code = Port.objects.get(pk=destination_code)

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

        except Port.DoesNotExist as e:
            return Response(
                {"message": "Invalid orig/dest code."},
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"message": "Error"},
                status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "Successfully saved prices."},
            status=status.HTTP_201_CREATED)


class RateView(ListAPIView):
    """
    Returns average price for a day.
    """

    def get_response(self, price_dict):
        return [
            {
                "day": datetime.datetime.strftime(key, "%Y-%m-%d"),
                "average_price": int(value["price"] / value["count"])
            }
            for key, value in price_dict.items()
        ]

    def get_price_dict(self, request, *args, **kwargs):
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")
        origin = self.request.query_params.get("origin")
        destination = self.request.query_params.get("destination")

        try:
            date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d")
            date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d")

            if date_to < date_from:
                raise ValueError("date_to must be greater than or equal to date_from.")
        except ValueError as e:
            return Response(
                {"message": e.args[0]},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            origin_code = Port.objects.get(pk=origin)
            origin_code_list = [origin_code]
        except Port.DoesNotExist as e:
            try:
                origin_region = Region.objects.get(pk=origin)
                origin_code_list = list(Port.objects.filter(parent_slug=origin_region))
            except Region.DoesNotExist as e:
                return Response(
                    {"message": "Invalid origin code/region."},
                    status=status.HTTP_400_BAD_REQUEST)

        try:
            destination_code = Port.objects.get(pk=destination)
            destination_code_list = [destination_code]
        except Port.DoesNotExist as e:
            try:
                destination_region = Region.objects.get(pk=destination)
                destination_code_list = list(Port.objects.filter(parent_slug=destination_region))
            except Region.DoesNotExist as e:
                return Response(
                    {"message": "Invalid destination code/region."},
                    status=status.HTTP_400_BAD_REQUEST)

        qs = Price.objects.filter(
            orig_code__in=origin_code_list,
            dest_code__in=destination_code_list,
            day__gte=date_from,
            day__lte=date_to).values_list("price", "day")

        price_dict = {}
        for q in qs:
            price = q[0]
            date = q[1]
            try:
                obj = price_dict[date]
                price_dict[date] = {
                    "price": price_dict[date]["price"] + price,
                    "count": price_dict[date]["count"] + 1
                }
            except KeyError as e:
                price_dict[date] = {
                    "price": price,
                    "count": 1
                }
        return price_dict

    def list(self, request, *args, **kwargs):
        price_dict = self.get_price_dict(request, *args, **kwargs)
        resp = self.get_response(price_dict)
        return Response(resp, status=status.HTTP_201_CREATED)


class RateNullView(RateView):
    def get_response(self, price_dict, display_null=False):
        return [
            {
                "day": datetime.datetime.strftime(key, "%Y-%m-%d"),
                "average_price": None if value["count"] < 3 else int(value["price"] / value["count"])
            }
            for key, value in price_dict.items()
        ]
