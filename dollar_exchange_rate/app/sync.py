
from vat_comply.api import GetRates

def SyncData():
    GetRates()
    print('Sync Data Last Five Days')