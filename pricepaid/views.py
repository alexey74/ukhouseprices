import django_filters
from django.db.models import Max, Min, Avg, Count
from django.shortcuts import render
from rest_framework import viewsets, generics, filters
from .models import PricePaidEntry, Town, District, County, PropertyType
from .serializers import (PricePaidEntrySerializer, PricePaidStatsSerializer,
                          TownSerializer, DistrictSerializer, CountySerializer)

# REST API


class PricePaidEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PricePaidEntry.objects.all().order_by('-transfer_date')
    serializer_class = PricePaidEntrySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('transfer_date', 'price', 'property_type',)


class TownFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = Town
        fields = ['name']


class TownViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Town.objects.all()
    serializer_class = TownSerializer
    #filter_backends = (filters.DjangoFilterBackend,)
    #filter_class = TownFilter

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'district__name', 'district__county__name')


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class CountyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = County.objects.all()
    serializer_class = CountySerializer


class PricePaidStatsFilter(django_filters.FilterSet):
    transfer_date = django_filters.DateFromToRangeFilter()
    property_type = django_filters.MultipleChoiceFilter(choices=PropertyType.choices())

    class Meta:
        model = PricePaidEntry
        fields = ['property_type', 'town', 'transfer_date']


class PricePaidStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PricePaidEntry.objects.values('property_type').annotate(
        max_price=Max('price'),
        min_price=Min('price'),
        avg_price=Avg('price'),
        transaction_count=Count('*'))

    serializer_class = PricePaidStatsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PricePaidStatsFilter

#
# class PricePaidStatsView(generics.ListAPIView):
#     queryset = PricePaidEntry.objects.values('property_type').annotate(
#         max_price=Max('price'),
#         min_price=Min('price'),
#         avg_price=Avg('price'),
#         transaction_count=Count('*'))
#
#     serializer_class = PricePaidEntrySerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filter_class = PricePaidStatsFilter


# UI

def index(request):
    return render(request, 'index.djhtml', vars())
