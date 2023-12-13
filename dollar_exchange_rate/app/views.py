from django.shortcuts import render,redirect
from django.http import HttpResponse
from datetime import date, datetime
from workalendar.america import  Brazil
from app.sync import SyncData

# Create your views here.
def home(request):
     # SyncData()
     return render(request, 'home.html')

def search(request):
     dtStart = datetime.strptime(request.POST.get('dt_start'), '%Y-%m-%d').date()
     dtEnd = datetime.strptime(request.POST.get('dt_end'), '%Y-%m-%d').date()

     errorsColect = periodIsValid(dtStart, dtEnd)
     errorsColect += workingDaysLimit(dtStart, dtEnd)

     if len(errorsColect) > 0 :
          url = f'/errors?err={','.join(errorsColect)}'
          return redirect(url)

     return render(request, 'search.html')

def periodIsValid(dtStart, dtEnd = date):
     errorsColect = []
     today = date.today()

     if dtStart == None or dtEnd == None:
          errorsColect.append('3')

     if dtStart >= today or dtEnd >= today:
          errorsColect.append('3')

     if dtEnd <= dtStart:
          errorsColect.append('2')

     return errorsColect

def workingDaysLimit(dtStart, dtEnd = date):
     errorsColect = []
     delta = abs((dtStart-dtEnd).days)
   
     cal = Brazil()
     count = 0

     for i in range(delta):
          if cal.add_working_days(dtStart, i):
               print(cal.add_working_days(dtStart, i))
               count+=1
   
          if count > 5:
              errorsColect.append('1')
              break
         
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
