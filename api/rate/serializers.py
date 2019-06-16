from rest_framework import serializers

from rate.models import Price


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = "__all__"

    def validate(self, attrs):
        return attrs
