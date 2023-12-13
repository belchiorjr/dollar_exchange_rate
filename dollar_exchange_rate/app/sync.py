
from vat_comply.api import GetRates
from datetime import date, datetime
from workalendar.america import  Brazil
from .models import ExchangeRate

def SyncData():
    for d in LastWorkingDays(date.today()):
        if ExchangeRate.objects.filter(rate_at=d).exists():
            continue

        dictData = GetRates(d)

        if len(dictData) > 0:
            er = ExchangeRate(
                rate_at=d,
                brl = dictData['rates']['BRL'], 
                eur= dictData['rates']['EUR'],
                jpy = dictData['rates']['JPY'],
                created_at = datetime.now(),
            )

            er.save()
               


def LastWorkingDays(dtBase = date.today()):
    cal = Brazil()
    lastDates = []
    
    for i in range(5):
        lastDates.append(cal.add_working_days(dtBase, -(i+1)))

    return lastDates