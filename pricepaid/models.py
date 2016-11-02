from django.db import models
from django_enumfield import enum

# Create your models here.


class PropertyType(enum.Enum):
    DETACHED = 0
    SEMI_DETACHED = 1
    TERRACED = 2
    FLATS_MAISONETTES = 3
    OTHER = 4


class County(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    county = models.ForeignKey(County, db_index=True)

    def __unicode__(self):
        return '%s, %s' % (self.name, self.county)


class Town(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    district = models.ForeignKey(District, db_index=True)

    def __unicode__(self):
        return '%s, %s' % (self.name, self.district)


class PricePaidEntry(models.Model):
    id = models.UUIDField(primary_key=True)
    price = models.PositiveIntegerField(db_index=True)
    transfer_date = models.DateTimeField(db_index=True)
    postcode = models.CharField(max_length=8, db_index=True)
    property_type = enum.EnumField(PropertyType, default=PropertyType.OTHER, db_index=True)
    town = models.ForeignKey(Town, db_index=True)

    def __unicode__(self):
        return '%s: date: %s price: %s type; %s town: %s' % (self.id, self.transfer_date, self.price, self.property_type, self.town)
