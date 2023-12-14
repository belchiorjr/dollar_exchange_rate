
from vat_comply.api import GetRates
from datetime import date, datetime
from workalendar.america import  Brazil
from .models import ExchangeRate

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

def GetListRates(dates):
    list = []

    for dt in dates:
        list.append(ExchangeRate.objects.filter(rate_at=dt))

    return list

def LastWorkingDays(dtBase = date.today()):
    cal = Brazil()
    lastDates = []
    
    for i in range(5):
        lastDates.append(cal.add_working_days(dtBase, -(i+1)))

    return lastDates