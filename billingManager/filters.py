from django_filters import DateRangeFilter, DateFilter
from .models import Bill, Provider
import django_filters

class BillFilter(django_filters.FilterSet):
    entry_date = django_filters.DateRangeFilter(name='entry_date',
                                                        label='Date (Between)')
    class Meta:
        model = Bill
        fields = ['bill_num',  'provider', 'service', 'district', 'entry_date']


class ProviderFilter(django_filters.FilterSet):
    provider_last_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Provider
        fields = ['provider_last_name',  'town']

