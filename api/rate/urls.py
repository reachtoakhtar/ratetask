"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from rate.views import PriceView, CurrencyView, PopulateDBView, RateView, RateNullView

app_name = "rate"


urlpatterns = [
    path('currencies/', CurrencyView.as_view(), name="currencies"),
    path('populate_db/', PopulateDBView.as_view(), name="populate_db"),
    path('prices/', PriceView.as_view(), name="prices"),
    path('rates/', RateView.as_view(), name="rates"),
    path('rates_null/', RateNullView.as_view(), name="rates_null"),
]
