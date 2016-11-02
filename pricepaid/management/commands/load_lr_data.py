
import logging
import datetime
import dateutil.parser
import urllib2
import csv

from django.db import transaction
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from pricepaid.models import PricePaidEntry, County, District, Town, PropertyType

BATCH_SIZE = 2000
URL = 'http://publicdata.landregistry.gov.uk/market-trend-data/price-paid-data/a/pp-%d.csv'

L = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Loads Price Paid data from the Land Registry into the DB'

    def add_arguments(self, parser):
        parser.add_argument('--years',
                            action='append',
                            dest='years',
                            default=3,
                            help='Number of years back to load data for')

    #@transaction.atomic
    def handle(self, **options):
        years = options['years']
        # transaction.set_autocommit(False)
        year = datetime.datetime.utcnow().year
        L.info('year=%s', year)
        created = 0
        skipped = 0
        start = timezone.now()
        end = timezone.now()
        rownum = 0
        batch = []
        for i in range(years):
            f = urllib2.urlopen(URL % year)
            #f = open('Downloads/pp-%d.csv' % year)
            for row in csv.reader(f):
                rownum += 1
                if rownum % BATCH_SIZE == 0:
                    now = timezone.now()
                    elapsed = (now - start).total_seconds()
                    L.info('year: %d; processed: %d; created: %d; skipped: %d; elapsed: %.2f sec; speed: %.2f rec/s; avg speed: %.2f rec/s' % (
                        year, rownum, created, skipped, elapsed, BATCH_SIZE / (now - end).total_seconds(), rownum / (now - start).total_seconds()))
                    end = timezone.now()
                    if batch:
                        PricePaidEntry.objects.bulk_create(batch)
                        batch = []
                    # transaction.commit()
                L.debug('row=%s', row)
                status = row[15]

                if status == 'A' and PricePaidEntry.objects.filter(id=row[0]).exists():
                    L.debug('skip existing record id=%s' % row[0])
                    skipped += 1
                    continue

                if status != 'D':
                    county, _ = County.objects.get_or_create(name=row[13])
                    district, _ = District.objects.get_or_create(county=county, name=row[12])
                    town, _ = Town.objects.get_or_create(district=district, name=row[11])
                    ptk = [k for k in PropertyType.__dict__.keys() if k[0] == row[4]][0]
                    pt = getattr(PropertyType,
                                 ptk)

                    newrec = dict(
                        price=int(row[1]),
                        transfer_date=timezone.make_aware(dateutil.parser.parse(row[2])),
                        postcode=row[3],
                        property_type=pt,
                        town=town
                    )

                try:
                    rec = PricePaidEntry.objects.get(id=row[0])
                    if status == 'D':
                        rec.delete()
                    elif status == 'C':
                        rec.update(**newrec)
                    else:
                        if 0:
                            L.error('Bad status %s for existing record: %s' % (status, row))
                except PricePaidEntry.DoesNotExist:
                    if status == 'A':
                        batch.append(PricePaidEntry(id=row[0], **newrec))
                        created += 1
                    else:
                        L.error('Invalid status for missing record: %s' % row)

            year -= 1
            # transaction.commit()
