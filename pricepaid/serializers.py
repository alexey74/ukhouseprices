from .models import PricePaidEntry, Town, District, County, PropertyType
from rest_framework import serializers


class PricePaidEntrySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PricePaidEntry
        fields = ('id', 'price', 'transfer_date', 'postcode', 'property_type', 'town')


class PricePaidStatsSerializer(serializers.HyperlinkedModelSerializer):

    def to_representation(self, instance):
        instance['property_type'] = PropertyType.label(instance['property_type'])
        return instance

    class Meta:
        model = PricePaidEntry
#        fields = ('max_price', 'min_price', 'avg_price', 'transaction_count')


class TownSerializer(serializers.HyperlinkedModelSerializer):

    full_name = serializers.CharField(source='__unicode__', read_only=True)

    class Meta:
        model = Town
        fields = ('id', 'name', 'district', 'full_name')


class DistrictSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = District
        fields = ('id', 'name', 'county')


class CountySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = County
        fields = ('id', 'name',)
