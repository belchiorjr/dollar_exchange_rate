
from datetime import date
import requests

def GetRates(dt = date.today()):
    url = f'https://api.vatcomply.com/rates?date={dt.year}-{dt.month}-{dt.day}&base=USD'
    response = requests.get(url)
    return response.json()