
from vat_comply.api import GetRates
from datetime import date, datetime
from workalendar.america import  Brazil
from .models import ExchangeRate
from django.db.models import F

def SyncData(dates):

    for dt in dates:
        if ExchangeRate.objects.filter(rate_at=dt).exists():
            continue

        dictData = GetRates(dt)

        if len(dictData) > 0:
            er = ExchangeRate(
                rate_at=dt,
                brl = dictData['rates']['BRL'], 
                eur= dictData['rates']['EUR'],
                jpy = dictData['rates']['JPY'],
                created_at = datetime.now(),
            )

            er.save()

def GetListRates(dates, currency):
    list = []

    arg =  f'{currency}'

    for dt in dates:
        r = ExchangeRate.objects.filter(rate_at=dt).values('rate_at').order_by('rate_at').annotate(value = F(f'{currency}'))
        list.append(r[0])

    return list

def LastWorkingDays(dtBase = date.today()):
    cal = Brazil()
    lastDates = []
    
    for i in range(5):
        lastDates.append(cal.add_working_days(dtBase, -(i+1)))

    return lastDates