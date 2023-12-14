from django.shortcuts import render,redirect
from datetime import date, datetime
from workalendar.america import  Brazil
from app.sync import SyncData, GetListRates

# Create your views here.
def home(request):
     return render(request, 'home.html')

def search(request):
     currency = request.POST.get('currency')
     _dtStart = request.POST.get('dt_start')
     _dtEnd = request.POST.get('dt_end')

     dtStart = datetime.strptime(_dtStart, '%Y-%m-%d').date()
     dtEnd = datetime.strptime(_dtEnd, '%Y-%m-%d').date()
     dates = workingDays(dtStart, dtEnd)
     
     errorsColect = periodIsValid(dtStart, dtEnd)
     errorsColect += workingDaysLimit(dates)
     
     if len(errorsColect) > 0 :
          url = f'/errors?err={','.join(errorsColect)}'
          return redirect(url)

     SyncData(dates)
     rates = GetListRates(dates)


     lbl = f'Resultado para o período de {dtStart.day}/{dtStart.month}/{dtStart.year} a {dtEnd.day}/{dtEnd.month}/{dtEnd.year} com a moeda {currency}'

     return render(request, 'search.html', {'label_result':lbl, 'currency':currency, 'rates':rates})



def periodIsValid(dtStart, dtEnd = date):
     errorsColect = []
     today = date.today()

     if dtStart == None or dtEnd == None:
          errorsColect.append('3')

     elif dtStart >= today or dtEnd >= today:
          errorsColect.append('3')

     elif dtEnd <= dtStart:
          errorsColect.append('2')

     return errorsColect


def workingDaysLimit(delta):
     errorsColect = []
     errorsColect.append('1')


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
          '5':'Tente novamente depois.',          
     }

     errStr = request.GET.get('err')
     errors = errStr.split(',')

     showErrors = []
          
     for e in errors:
          showErrors.append(errorsDic[e])

     return render(request, 'error.html',{'showErrors':showErrors})
