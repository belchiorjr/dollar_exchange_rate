from django.shortcuts import render,redirect
from datetime import date, datetime
from workalendar.america import  Brazil
from app.sync import SyncData, GetListRates
import json

# Create your views here.
def home(request):
     return render(request, 'home.html')

def search(request):

     errorsColect = []

     try:
          currency = request.POST.get('currency')
          _dtStart = request.POST.get('dt_start')
          _dtEnd = request.POST.get('dt_end')
          dtStart = datetime.strptime(_dtStart, '%Y-%m-%d').date()
          dtEnd = datetime.strptime(_dtEnd, '%Y-%m-%d').date()
          errorsColect = periodIsValid(dtStart, dtEnd)
          dates = workingDays(dtStart, dtEnd)
          errorsColect += workingDaysLimit(dates)
     except ValueError:
          errorsColect += ['5']

     if len(errorsColect) > 0 :
          url = f'/errors?err={','.join(errorsColect)}'
          return redirect(url)

     SyncData(dates)
     rates = GetListRates(dates, currency)
     
     cat = [] 
     val = []

     for r in rates :
          cat.append(f'\'{str(r['rate_at'].strftime('%d/%m/%Y'))}\'')
          val.append(str(round(r['value'],2)))


     categories = ','.join(cat)
     values = ','.join(val)

     upCurrency = f'{currency}'.upper()
     lbl = f'Resultado para o período de {dtStart.day}/{dtStart.month}/{dtStart.year} a {dtEnd.day}/{dtEnd.month}/{dtEnd.year} com a moeda {upCurrency}'
 
     return render(request, 'search.html', {'label_result':lbl, 'currency':upCurrency, 'rates':rates, 'categories': categories, 'values': values })


def periodIsValid(dtStart, dtEnd = date):
     errorsColect = []
     today = date.today()

     if dtStart == '' or dtEnd == '':
          errorsColect.append('3')

     elif dtStart >= today or dtEnd >= today:
          errorsColect.append('3')

     elif dtEnd <= dtStart:
          errorsColect.append('2')

     return errorsColect



def workingDays(dtStart, dtEnd = date):
     dates = []
     delta = abs((dtEnd-dtStart).days)+1
     cal = Brazil()
     
     for i in range(delta):
          dt = cal.add_working_days(dtStart, i) 

          if dt != None and dt <= dtEnd:
               dates.append(dt)
     
     return dates


def workingDaysLimit(dates):
     errorsColect = []
   
     if len(dates) > 5:
          errorsColect.append('1')
        
     return errorsColect


def error(request):
     errorsDic = {
          '1':'Período não permitido, máximo somente de 5 dias úteis.',
          '2':'A data inicial, não pode ser maior ou igual a data final para período a ser pesquisado.',
          '3':'A data inicial ou final, deve ser uma anterior ao dia de hoje para realizar a pesquisa.',
          '4':'A data final, não pode ser menor ou igual a data inicial para período a ser pesquisado.',          
          '5':'Preencha os dados necessários, tente novamente.',          
     }

     errStr = request.GET.get('err')
     errors = errStr.split(',')

     showErrors = []
          
     for e in errors:
          showErrors.append(errorsDic[e])

     return render(request, 'error.html',{'showErrors':showErrors})
