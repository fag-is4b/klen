# This Python file uses the following encoding: utf-8
from django.conf import settings
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.template import RequestContext
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect, render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from BeautifulSoup import BeautifulSoup
import xlsxwriter
import urllib2, sys
from decimal import *
import datetime
import ast
import re
import json as json

from klen.main.models  import Main, MainModelForm

'''
key_value_list={'dollar':'Доллар','euro':'Евро','ag':'Серебро','pt':'Платина','pd':'Палладий',
"_dji":"(США)DJIA", "_gspc":"(США)S&P 500", "_ndx":"(США)NASDAQ 100", "_ixic":"(США)NASDAQ Composite",
"_n225":"(Япония)Nikkei 225", "_ftse":"(Англия)FTSE 100", "_fchi":"(Франция)CAC 40", "_gdaxi":"(Германия)DAX",
"_bvsp":"(Бразилия)Bovespa", "_hsi":"(Гонконг)Hang Seng", "_merv":"(Аргентина)Merval", "_mxx":"(Мексика)IPC",
"_sti":"(Сингапур)Straits Times", "_ks11":"(Южная Корея)Seoul Composite", "_atx":"(Австрия)ATX",
"_ssmi":"(Швейцария)Swiss Market", "rts_rs":"(Россия)РТС", "_gsptse":"(Канада)S&P/TSX", "aex_as":"(Нидерланды) AEX",
"_ibex":"(Испания) IBEX 35", "_omx":"(Швеция) OMXS30", "_axjo":"(Австралия)S&P/ASX 200",
"000001_ss":"(Китай) Shanghai Composite", "_bsesn":"(Индия) SENSEX", "_twii":"(Тайвань)TSEC", "_ta100":"(Израиль)Tel Aviv Ta-100",

"TQBR_VTBR":"ВТБ ао","TQBR_GAZP":"ГАЗПРОМ ао","TQBR_GMKN":"ГМКНорНик","TQBR_LKOH":"Лукойл","TQBR_ROSN":"Роснефть",
"TQBR_NVTK":"Новатэк ао","TQBR_HYDR":"РусГидро","TQBR_SBER":"Сбербанк","TQBR_CHMF":"СевСт-ао","TQBR_SNGS":"Сургнфгз","TQBR_URKA":"Уркалий-ао",

"pid-8831-last":"Медь","pid-8910-last":"Платина", "pid-8883-last":"Палладий", "pid-8849-last":"Нефть WTI",
"pid-8833-last":"Нефть Brent","pid-8862-last":"Природ. Газ", "pid-8988-last":"Мазут", "pid-8861-last":"Газойль Лондон",
"pid-8848-last":"CO2", "pid-8917-last":"Пшеница США", "pid-8912-last":"Пшеница Лондон", "pid-13916-last":"Грубый рис",
"pid-8918-last":"Кукуруза США", "pid-8916-last":"Соевые Бобы США", "pid-8915-last":"Соевое масло США",
"pid-8851-last":"Хлопок США No.2", "pid-8894-last":"Какао США", "pid-8860-last":"Какао Лондон", "pid-8832-last":"Кофе США С",
"pid-8911-last":"Кофе Лондон", "pid-8869-last":"Сахар США No11", "pid-8834-last":"Сахар Лондон", "pid-8891-last":"Апельсиновый Сок",
"pid-8914-last":"Живой Скот"
}
'''

name_list=[u'Доллар',u'Евро',u'Серебро',u'Платина',u'Палладий',
u'ВТБ ао',u'ГАЗПРОМ ао',u'ГМКНорНик',u'Лукойл',u'Роснефть',u'Новатэк ао',u'РусГидро',u'Сбербанк',u'СевСт-ао',u'Сургнфгз',u'Уркалий-ао',

u"(США)DJIA",u"(США)S&P 500",u"(США)NASDAQ 100",u"(США)NASDAQ Composite",
u"(Япония)Nikkei 225",u"(Англия)FTSE 100",u"(Франция)CAC 40",u"(Германия)DAX",
u"(Бразилия)Bovespa",u"(Гонконг)Hang Seng",u"(Аргентина)Merval",u"(Мексика)IPC",
u"(Сингапур)Straits Times",u"(Южная Корея)Seoul Composite",u"(Австрия)ATX",
u"(Швейцария)Swiss Market",u"(Россия)РТС",u"(Канада)S&P/TSX",u"(Нидерланды) AEX",
u"(Испания) IBEX 35",u"(Швеция) OMXS30",u"(Австралия)S&P/ASX 200",
u"(Китай) Shanghai Composite",u"(Индия) SENSEX",u"(Тайвань)TSEC",u"(Израиль)Tel Aviv Ta-100",

u"Медь",u"Платина",u"Палладий",u"Нефть WTI",
u"Нефть Brent",u"Природ. Газ",u"Мазут",u"Газойль Лондон",
u"CO2",u"Пшеница США",u"Пшеница Лондон",u"Грубый рис",
u"Кукуруза США",u"Соевые Бобы США",u"Соевое масло США",
u"Хлопок США No.2",u"Какао США",u"Какао Лондон",u"Кофе США С",
u"Кофе Лондон",u"Сахар США No11",u"Сахар Лондон",u"Апель-синовый Сок",u"Живой Скот"
]


key_list1=['dollar','euro','ag','pt','pd',
'TQBR_VTBR','TQBR_GAZP','TQBR_GMKN','TQBR_LKOH','TQBR_ROSN','TQBR_NVTK','TQBR_HYDR','TQBR_SBER','TQBR_CHMF','TQBR_SNGS','TQBR_URKA',
]
key_list2=[
"_dji", "_gspc", "_ndx", "_ixic",
"_n225", "_ftse", "_fchi", "_gdaxi",
"_bvsp", "_hsi", "_merv", "_mxx",
"_sti", "_ks11", "_atx",
"_ssmi", "rts_rs", "_gsptse", "aex_as",
"_ibex", "_omx", "_axjo",
"000001_ss", "_bsesn", "_twii", "_ta100",
]
key_list4=[
"pid-8831-last","pid-8910-last", "pid-8883-last", "pid-8849-last",
"pid-8833-last","pid-8862-last", "pid-8988-last", "pid-8861-last",
"pid-8848-last", "pid-8917-last", "pid-8912-last", "pid-13916-last",
"pid-8918-last", "pid-8916-last", "pid-8915-last",
"pid-8851-last", "pid-8894-last", "pid-8860-last", "pid-8832-last",
"pid-8911-last", "pid-8869-last", "pid-8834-last", "pid-8891-last",
"pid-8914-last"
]


def xls_write(request):
    print 'xls_write'
    # Create a workbook and add a worksheet.
    dt=datetime.datetime.today()
    filename='media/abc-%s-%s-%s.xlsx'%(dt.day, dt.hour, dt.minute)
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:BR', 15)

    format0 = workbook.add_format({'align': 'right'})
    format1 = workbook.add_format({'num_format': 'dd.mm.yyyy hh:mm',
                                      'align': 'right'})

    bold = workbook.add_format({'align': 'center', 'bold': True})

    print 'xls created', filename
    try:
        aRows = Main.objects.order_by('-pk')[0:5000]
        row = 0

        worksheet.write(row, 0, u'Дата', bold)
        worksheet.write(row, 1, u'Золото', bold)
        worksheet.write(row, 2, u'Доллар', bold)
        worksheet.write(row, 3, u'Евро', bold)
        #
        col = 4
        for item in name_list:
            #print item
            worksheet.write(row, col, item+'/Au', bold)
            col += 1
        #
        row = 1
        for item in aRows:
            #print item.date_time
            worksheet.write(row, 0, item.date_time, format1)
            worksheet.write(row, 1, item.au, format0)
            worksheet.write(row, 2, item.dollar, format0)
            worksheet.write(row, 3, item.euro, format0)
            col = 4
            ldic=json.loads(item.data)
            #print ldic
            for key,val in ldic:
                worksheet.write(row, col, val, format0)
                col += 1
            row += 1
        #
    except Exception as ex:
        print ex
    #
    print 'close', filename
    workbook.close()
    print '==== ok ==='
    return HttpResponse(filename)

def main_show(request):
    print 'main_show'
    login_message=''
    if request.POST  and  request.POST.get('login'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print 'login', username
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
            else:
                # Return a 'disabled account' error message
                login_message='Это имя не активно'
        else:
            # Return an 'invalid login' error message.
            login_message='Неверное имя или пароль'
        print login_message
    redirect='main/index.html'
    all_rows=[]
    try:
        #strs = Main.objects.all()
        #Ексколько последних
        strs = Main.objects.order_by('-pk')[0:500]
        for str1 in list(strs):
            #print type(str1)
            #print str1.id
            row1=[]
            row1.append(str1.date_time)
            row1.append('%.4f'%str1.au)
            row1.append('%.4f'%str1.dollar)
            row1.append('%.4f'%str1.euro)
            ldic=json.loads(str1.data)
            row1.append(ldic)
            #all_rows.append(row1)
            all_rows.append([str1.id,row1])


    except Exception as ex:
        print ex
        all_rows=[]

    #print all_rows
    key_list=key_list1+key_list2+key_list4


    dic={'user':request.user,'strs':all_rows, 'name_list':name_list, 'key_list':key_list, 'login_message':login_message}
    return direct_to_template(request, redirect, dic,
                               context_instance=RequestContext(request))


def get_soup(url):
    #hdr = {'User-Agent': 'Mozilla/5.0','Accept' : 'text/html'}
    #req = urllib2.Request(url,headers=hdr)
    #page = urllib2.urlopen(req)
    try:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(url)
        page=response.read()
        soup = BeautifulSoup(page)
        return soup
    except Exception as ex:
        print ex
        return None

def get_soup4(url):
    hdr = {'User-Agent': 'Mozilla/5.0','Accept' : 'text/html'}
    req = urllib2.Request(url,headers=hdr)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
    return soup


def parse(request):
    print 'parse'
    dic=parse1(True)
    print '==ok=='
    #mdic={'user':request.user,'main':"y",}
    #dic.update(mdic)
    return redirect("/")
    #print dic
    #redirect='main/index.html'
    #return direct_to_template(request, redirect, dic,
    #                           context_instance=RequestContext(request))


def parse1(isSave):
    print 'parse-1'
    dollar=-1
    euro=-1
    au=-1
    ag=-1
    pt=-1
    pd=-1
    print 'get from http://www.cbr.ru/'
    doc = get_soup('http://www.cbr.ru/')
    print 'ok'
    for x in doc.findAll('div', attrs={'class':'w_data_wrap'}):
        w_str='%s'%x.findPrevious('td',attrs={'class':'title'} )
        x_str='%s'%x
        try:
            if w_str.find('Доллар')>0:
                dollar=Decimal(x_str[-13:-6].replace(' ','').replace(',','.'))
            elif w_str.find('Евро')>0:
                euro=Decimal(x_str[-13:-6].replace(' ','').replace(',','.'))
            elif w_str.find('Золото')>0:
                #print x_str, x_str[-21:-13]
                au=Decimal(x_str[-21:-13].replace(' ','').replace(',','.'))
            elif w_str.find('Серебро')>0:
                #print x_str, x_str[-21:-13]
                ag=Decimal(x_str[-18:-13].replace(' ','').replace(',','.'))
            elif w_str.find('Платина')>0:
                #print x_str, x_str[-21:-13]
                pt=Decimal(x_str[-21:-13].replace(' ','').replace(',','.'))
            elif w_str.find('Палладий')>0:
                #print x_str, x_str[-21:-13]
                pd=Decimal(x_str[-21:-13].replace(' ','').replace(',','.'))

        except Exception as ex:
            print ex

    date = datetime.datetime.today()

    print '%s-%s: $=%.4f, E=%.4f, Au=%.4f'%(date.time().hour, date.time().minute,dollar,euro, au)
    wi=[]
    bf=[]
    kot=[]

    wi=parse2()
    bf=parse3()
    kot=parse4(dollar)
    #-----------------------------
    getcontext().prec = 6
    getcontext().rounding = ROUND_FLOOR
    print '----------------------------------'
    rezult=[]
    try:
        #Доллар
        key="dollar"
        val=Decimal(dollar/au)
        s_val='%s'%val
        rezult.append([key,s_val])
        #Евро
        key="euro"
        val=Decimal(euro/au)
        s_val='%s'%val
        rezult.append([key,s_val])
        #Серебро
        key="ag"
        val=Decimal(ag/au)
        s_val='%s'%val
        rezult.append([key,s_val])
        #Платина
        key="pt"
        val=Decimal(pt/au)
        s_val='%s'%val
        rezult.append([key,s_val])
        #Палладий
        key="pd"
        val=Decimal(pd/au)
        s_val='%s'%val
        rezult.append([key,s_val])
        #--
        for  key, val in bf:
            #print key, val
            n_val=0
            try:
                n_val=Decimal(val)/au
            except:
                pass
            s_val='%s'%n_val
            rezult.append([key,s_val])
        #--
        for  key, val in wi:
            #print key, val
            n_val=0
            try:
                n_val=Decimal(val)/au
            except:
                pass

            s_val='%s'%n_val
            rezult.append([key,s_val])
        #--
        for  key, val in kot:
            #print key, val
            n_val=0
            if Decimal(val)>0:
                try:
                    n_val=Decimal(val)/au
                except:
                    pass
            s_val='%s'%n_val
            rezult.append([key,s_val])
    except Exception as ex:
        print ex
    #print rezult
    if len(rezult)>0:
        data=json.dumps(rezult)
        if isSave :
            print '>> %s save to db'%date
            mMain = Main(dollar=dollar, euro=euro, au=au, data=data)
            mMain.save()

    return {'dt':date, 'au':au, 'dollar':dollar, 'euro':euro, 'rezult':rezult}



def parse2():
    print 'parse-2'
    print 'get from http://stockpost.ru/quote/parse.php'
    doc = get_soup('http://stockpost.ru/quote/parse.php')
    print 'ok'
    dic=ast.literal_eval('{0:s}'.format(doc))
    wi=[]
    #for key, value in key_value_list.items():
    for key in key_list2:
        try:
            idxvalue='0'
            if dic.get(key):
                idxvalue=dic.get(key).get('value').replace(',', '')
            wi.append([key,idxvalue])
            #print key_value_list.get(key),key,idxvalue
        except Exception as ex:
            print ex
    print '--',len(wi)
    return wi

def parse3():
    print 'parse-3'
    print 'get from http://bcs-express.ru/key_value_list-i-grafiki'
    doc=get_soup('http://bcs-express.ru/key_value_list-i-grafiki')
    print 'ok'
    bf=[]
    key=''
    value='0'
    try:
        for x in doc.findAll(id=re.compile("^TQBR_")):
            #print x
            key=x['id']
            #key_str=x.findNext('a').string
            value=x.findNext('p',attrs={'class':'price'}).string.replace(',','.')
            #print key_str, key, value
            bf.append([key,value])
    except Exception as ex:
        print ex

    print '--',len(bf)

    return bf

def parse4(dollar):
    print 'parse-4'
    print 'get from http://ru.investing.com/commodities/...'
    doc=get_soup4("http://ru.investing.com/commodities/%D0%A4%D1%8C%D1%8E%D1%87%D0%B5%D1%80%D1%81%D1%8B-%D0%B2-%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%BC-%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%B8")
    print 'ok'
    kot=[]
    #for key, value in key_value_list.items():
    try:
        for key in key_list4:
            try:
                kot_price=doc.find('td', attrs={'class':key}).string.replace('.','').replace(',','.')
                kotirovka=Decimal(kot_price)*dollar
                kot.append([key,kotirovka])
            except:
                pass
            #print value,kot_price,kotirovka
    except Exception as ex:
        print ex

    print '--',len(kot)

    return kot

def row_delete(request, row_id):
    print'row_delete:', row_id
    rezult='ok'
    try:
        row = Main.objects.get(pk=row_id)
        row.delete()
    except Exception as ex:
        print ex
        return HttpResponse(ex)

    print rezult
    return HttpResponse(rezult)

def row_edit(request, row_id):
    print 'row_edit'
    row = Main.objects.get(pk=row_id)
    print row.id

    if request.POST  and  request.POST.get('save'):
        print 'row.save'
        lvalues=request.POST.getlist('sdata_values')
        key_list=key_list1+key_list2+key_list4
        #print '>>',lvalues
        ldata=[]
        j=0
        for value in lvalues:
            ldata.append([key_list[j],value])
            j += 1
        data=json.dumps(ldata)
        form = MainModelForm(request.POST, instance=row)
        #if form.is_valid():
        form.data['data'] = data

        form.save()

        return redirect("/")
    else:
        print 'row.edit'
        form = MainModelForm(instance=row)
        ldata=json.loads(row.data)
        #print 'data:',type(ldata)
        sdata=[]
        j=0
        for key, value in ldata:
            sdata.append([name_list[j],value])
            j += 1

        #form.fields['data'].initial = sdata
        return direct_to_template(request, 'main/row_edit.html',
                                  {'form':form, 'sdata':sdata,
                                   'user':request.user},
                                       context_instance=RequestContext(request))



def logout_view(request):
    print 'user logout'
    logout(request)
    return redirect("/")

def parse_sind(uri):
    site="http://sindika.ru/"
    #uri="magaziny/stroitelnyie-materialyi/metallocherepicza/"
    url=site+uri
    #print 'parse-sind'
    print 'get from ', url
    doc=get_soup(url)
    bf=[]
    if doc:
        #print 'ok'
        key_cat='category'
        value_cat=get_cat(doc)
        #print key,value
        #bf.append([key,value])
        for section in doc.findAll('div', attrs={'class':'shop-tpl '}):
            bf1=[]
            for x in section.findAll('div', attrs={'class':'par'}):
                value=x.string
                key=''
                if value:
                    key='description'
                else:
                    try:
                        str='%s'%x
                        key=x.find('strong').string
                        idx1=str.index('</strong>')
                        idx2=str.index('</div>')
                        value=str[idx1+9:idx2]
                    except:
                        value=''
                if len(key)>0:
                    #print 'key:',key,' value:',value,'\n'
                    bf1.append([key,value])
            bf.append([value_cat,bf1])

    return bf

def get_cat(doc):
    doc2=doc.find('div',attrs={'class':'content'})
    ret=doc2.find('span').string
    return ret

nmlist={
'magaziny/elektrotovaryi-i-osveshhenie/',
'magaziny/elektrotovaryi-i-osveshhenie/aksessuaryi-dlya-elektromontazha/',
'magaziny/elektrotovaryi-i-osveshhenie/avtomaticheskie-vyiklyuchateli/',
'magaziny/elektrotovaryi-i-osveshhenie/differenczialnyie-avtomaticheskie-vyiklyuchateli/',
'magaziny/elektrotovaryi-i-osveshhenie/izmeritelnyie-priboryi/',
'magaziny/elektrotovaryi-i-osveshhenie/korobki-i-shhitki-elektromontazhnyie/',
'magaziny/elektrotovaryi-i-osveshhenie/lotki-metallicheskie/',
'magaziny/elektrotovaryi-i-osveshhenie/magazin-elektriki-teplyus.html/',
'magaziny/elektrotovaryi-i-osveshhenie/provoda-i-kabeli-elektricheskie/',
'magaziny/elektrotovaryi-i-osveshhenie/raspredelitelnyie-shkafyi-i-shhityi/',
'magaziny/elektrotovaryi-i-osveshhenie/rele-i-kontaktoryi/',
'magaziny/elektrotovaryi-i-osveshhenie/rozetki-i-vyiklyuchateli/',
'magaziny/elektrotovaryi-i-osveshhenie/schetchiki-elektroenergii/',
'magaziny/elektrotovaryi-i-osveshhenie/sistemyi-kabel-kanalov/',
'magaziny/elektrotovaryi-i-osveshhenie/trubyi-gladkie/',
'magaziny/elektrotovaryi-i-osveshhenie/trubyi-gofrirovannyie/',
'magaziny/elektrotovaryi-i-osveshhenie/ustrojstva-plavnogo-puska/',
'magaziny/elektrotovaryi-i-osveshhenie/ustrojstva-zashhitnogo-otklyucheniya/',
'magaziny/elektrotovaryi-i-osveshhenie/vyiklyuchateli-nagruzki-rubilniki/',
'magaziny/furnitura-osnastka-krepezh/',
'magaziny/furnitura-osnastka-krepezh/diski-otreznyie/',
'magaziny/furnitura-osnastka-krepezh/furnitura-mebelnaya/',
'magaziny/furnitura-osnastka-krepezh/gvozdi/',
'magaziny/furnitura-osnastka-krepezh/mebelnaya-funitura.html/',
'magaziny/furnitura-osnastka-krepezh/ogranichiteli-dvernyie/',
'magaziny/furnitura-osnastka-krepezh/petli-dvernyie/',
'magaziny/furnitura-osnastka-krepezh/ruchki-dvernyie/',
'magaziny/furnitura-osnastka-krepezh/samorezyi/',
'magaziny/furnitura-osnastka-krepezh/ugolok-metallicheskij/',
'magaziny/furnitura-osnastka-krepezh/zamki-dvernyie/',
'magaziny/instrument-elektricheskij-i-benzinovyij/',
'magaziny/instrument-elektricheskij-i-benzinovyij/benzorezyi/',
'magaziny/instrument-ruchnoj-i-izmeritelnyij/',
'magaziny/instrument-ruchnoj-i-izmeritelnyij/applikatoryi-malyarnyie/',
'magaziny/instrument-ruchnoj-i-izmeritelnyij/kisti-malyarnyie/',
'magaziny/instrument-ruchnoj-i-izmeritelnyij/lotki-i-vedra-dlya-kraski/',
'magaziny/instrument-ruchnoj-i-izmeritelnyij/shhetki-i-skrebki-malyarnyie/',
'magaziny/instrument-ruchnoj-i-izmeritelnyij/valiki-malyarnyie/',
'magaziny/instrument-stroitelnyij-i-sadovyij/',
'magaziny/instrument-stroitelnyij-i-sadovyij/vozduxoduvki/',
'magaziny/obustrojstvo-doma-i-interera/',
'magaziny/obustrojstvo-doma-i-interera/avtomatika-dlya-vorot/',
'magaziny/obustrojstvo-doma-i-interera/chasyi/',
'magaziny/obustrojstvo-doma-i-interera/dekorirovanie-okon/',
'magaziny/obustrojstvo-doma-i-interera/karnizyi-dekorativnyie/',
'magaziny/obustrojstvo-doma-i-interera/tekstilnaya-studiya-violet.html/',
'magaziny/obustrojstvo-doma-i-interera/zerkala/',
'magaziny/okna-dveri-lestniczyi/',
'magaziny/okna-dveri-lestniczyi/balyasinyi-dlya-lestnicz/',
'magaziny/okna-dveri-lestniczyi/belorusskie-okna.html/',
'magaziny/okna-dveri-lestniczyi/dveri-belorussii.html/',
'magaziny/okna-dveri-lestniczyi/dveri-mezhkomnatnyie/',
'magaziny/okna-dveri-lestniczyi/dveri-razdvizhnyie/',
'magaziny/okna-dveri-lestniczyi/dveri-torex.html/',
'magaziny/okna-dveri-lestniczyi/dveri-vxodnyie/',
'magaziny/okna-dveri-lestniczyi/lestniczyi-cherdachnyie-krovelnyie/',
'magaziny/okna-dveri-lestniczyi/lestniczyi-marshevyie/',
'magaziny/okna-dveri-lestniczyi/lestniczyi-s-gusinyim-shagom/',
'magaziny/okna-dveri-lestniczyi/lestniczyi-vintovyie/',
'magaziny/okna-dveri-lestniczyi/okna-mansardnyie/',
'magaziny/okna-dveri-lestniczyi/perila-dlya-lestnicz/',
'magaziny/okna-dveri-lestniczyi/salon-dverej-intekron.html/',
'magaziny/okna-dveri-lestniczyi/salon-dverej-iz-massiva-alvero.html/',
'magaziny/okna-dveri-lestniczyi/salon-dverej-volxovecz.html/',
'magaziny/okna-dveri-lestniczyi/salon-magazin-elit-dveri.html/',
'magaziny/okna-dveri-lestniczyi/stalnyie-dveri-gardian.html/',
'magaziny/okna-dveri-lestniczyi/stolbyi-dlya-lestnicz/',
'magaziny/okna-dveri-lestniczyi/stupeni-dlya-lestnicz/',
'magaziny/okna-dveri-lestniczyi/tetiva-dlya-lestniczyi/',
'magaziny/okna-dveri-lestniczyi/union-italyanskie-dveri.html/',
'magaziny/otdelochnyie-materialyi/',
'magaziny/otdelochnyie-materialyi/dekorativnyie-kraski/',
'magaziny/otdelochnyie-materialyi/dekorativnyie-shtukaturki/',
'magaziny/otdelochnyie-materialyi/don-keram.html/',
'magaziny/otdelochnyie-materialyi/emali/',
'magaziny/otdelochnyie-materialyi/firmennyij-magazin-dekoplast.html/',
'magaziny/otdelochnyie-materialyi/firmennyij-magazin-kerama-marazzi.html/',
'magaziny/otdelochnyie-materialyi/germetiki/',
'magaziny/otdelochnyie-materialyi/gruntovki/',
'magaziny/otdelochnyie-materialyi/ip-grigorev.html/',
'magaziny/otdelochnyie-materialyi/kamennyij-aglomerat/',
'magaziny/otdelochnyie-materialyi/keramogranit/',
'magaziny/otdelochnyie-materialyi/kirpich-obliczovochnyij/',
'magaziny/otdelochnyie-materialyi/klei-i-mastiki/',
'magaziny/otdelochnyie-materialyi/klinkernaya-keramika.html/',
'magaziny/otdelochnyie-materialyi/klinkernaya-plitka/',
'magaziny/otdelochnyie-materialyi/kolor-studiya-simfoniya-krasok.html/',
'magaziny/otdelochnyie-materialyi/kraska-kolerovka.html/',
'magaziny/otdelochnyie-materialyi/kraski-dlya-vnutrennix-rabot/',
'magaziny/otdelochnyie-materialyi/kraski-fasadnyie/',
'magaziny/otdelochnyie-materialyi/laki/',
'magaziny/otdelochnyie-materialyi/laminat/',
'magaziny/otdelochnyie-materialyi/lepnina.html/',
'magaziny/otdelochnyie-materialyi/lepnoj-dekor/',
'magaziny/otdelochnyie-materialyi/logotip.html/',
'magaziny/otdelochnyie-materialyi/lp-smart-side.html/',
'magaziny/otdelochnyie-materialyi/morilki-propitki-antiseptiki/',
'magaziny/otdelochnyie-materialyi/mozaika-i-mozaichnyie-panno/',
'magaziny/otdelochnyie-materialyi/naturalnyij-kamen/',
'magaziny/otdelochnyie-materialyi/oboi/',
'magaziny/otdelochnyie-materialyi/otdelochnyij-profil/',
'magaziny/otdelochnyie-materialyi/paneli-stenovyie/',
'magaziny/otdelochnyie-materialyi/plintusa-napolnyie/',
'magaziny/otdelochnyie-materialyi/plintusa-potolochnyie/',
'magaziny/otdelochnyie-materialyi/plitka-ceramicstile.html/',
'magaziny/otdelochnyie-materialyi/plitka-keramicheskaya/',
'magaziny/otdelochnyie-materialyi/plityi-potolochnyie/',
'magaziny/otdelochnyie-materialyi/porogi/',
'magaziny/otdelochnyie-materialyi/sajding-czokolnyij/',
'magaziny/otdelochnyie-materialyi/sajding-metallicheskij/',
'magaziny/otdelochnyie-materialyi/sajding-vinilovyij/',
'magaziny/otdelochnyie-materialyi/salon-oboev-soffitta.html/',
'magaziny/otdelochnyie-materialyi/steklo-i-mir.html/',
'magaziny/otdelochnyie-materialyi/tetrum-laminat-praktik-i-parafloor.html/',
'magaziny/otdelochnyie-materialyi/vitrazhi-iz-czvetnogo-stekla/',
'magaziny/otdelochnyie-materialyi/zatirki-dlya-mezhplitochnyix-shvov/',
'magaziny/otoplenie/',
'magaziny/otoplenie/biokaminyi/',
'magaziny/otoplenie/cistemyi-obogreva-truboprovodov/',
'magaziny/otoplenie/kaminyi-drovyanyie/',
'magaziny/otoplenie/kaminyi-elektricheskie/',
'magaziny/otoplenie/pechi-drovyanyie/',
'magaziny/otoplenie/polotenczesushiteli-vodyanyie/',
'magaziny/otoplenie/salon-dizajn-radiatorov-polotenczesushitelej-lyuks-komfort.html/',
'magaziny/otoplenie/salon-kaminov-mrkamin.html/',
'magaziny/otoplenie/sistemyi-obogreva-krovli-i-vodostokov/',
'magaziny/otoplenie/teplyie-polyi-elektricheskie/',
'magaziny/otoplenie/topki-kaminnyie/',
'magaziny/santexnika/',
'magaziny/santexnika/aksessuaryi-dlya-kuxni/',
'magaziny/santexnika/aksessuaryi-vannoj-komnatyi-i-tualeta/',
'magaziny/santexnika/izmelchiteli-pishhevyix-otxodov/',
'magaziny/santexnika/market-santex.html/',
'magaziny/santexnika/mebel-i-aksessuaryi-dlya-vannoj/',
'magaziny/santexnika/mojki-dlya-kuxni/',
'magaziny/santexnika/nasosyi/',
'magaziny/santexnika/radiatoryi/',
'magaziny/santexnika/rakovinyi-unitazyi-bide/',
'magaziny/santexnika/santexnika.html/',
'magaziny/santexnika/sistemyi-ventilyaczii/',
'magaziny/santexnika/smesiteli-dlya-kuxni/',
'magaziny/santexnika/smesiteli-i-dushevoe-oborudovanie/',
'magaziny/santexnika/vannyi-dushevyie-kabinyi/',
'magaziny/santexnika/vodonagrevateli-kotlyi/',
'magaziny/santexnika/vodosnabzhenie-filtryi/',
'magaziny/speczodezhda-xozyajstvennyij-inventar/',
'magaziny/speczodezhda-xozyajstvennyij-inventar/pyilesosyi-dlya-suxoj-uborki/',
'magaziny/speczodezhda-xozyajstvennyij-inventar/pyilesosyi-dlya-vlazhnoj-uborki/',
'magaziny/stroitelnyie-materialyi/',
'magaziny/stroitelnyie-materialyi/bitumnaya-myagkaya-gibkaya-cherepicza/',
'magaziny/stroitelnyie-materialyi/blok-xaus/',
'magaziny/stroitelnyie-materialyi/brus-kleennyij/',
'magaziny/stroitelnyie-materialyi/brus-obreznoj/',
'magaziny/stroitelnyie-materialyi/brusok-obreznoj/',
'magaziny/stroitelnyie-materialyi/brusok-strogannyij/',
'magaziny/stroitelnyie-materialyi/brus-strogannyij/',
'magaziny/stroitelnyie-materialyi/czement/',
'magaziny/stroitelnyie-materialyi/czementno-peschanaya-cherepicza/',
'magaziny/stroitelnyie-materialyi/doska-obreznaya/',
'magaziny/stroitelnyie-materialyi/doska-palubnaya/',
'magaziny/stroitelnyie-materialyi/doska-polovaya/',
'magaziny/stroitelnyie-materialyi/doska-strogannaya/',
'magaziny/stroitelnyie-materialyi/doska-terrasnaya/',
'magaziny/stroitelnyie-materialyi/eko-lajf-pilomaterialyi-derevoobrabotka.html/',
'magaziny/stroitelnyie-materialyi/evropol/',
'magaziny/stroitelnyie-materialyi/evrovagonka/',
'magaziny/stroitelnyie-materialyi/fanera/',
'magaziny/stroitelnyie-materialyi/gidroizolyacziya/',
'magaziny/stroitelnyie-materialyi/gipsokarton/',
'magaziny/stroitelnyie-materialyi/gipsovolokno/',
'magaziny/stroitelnyie-materialyi/gruntovki-stroitelnyie/',
'magaziny/stroitelnyie-materialyi/imitacziya-brusa/',
'magaziny/stroitelnyie-materialyi/keramicheskaya-cherepicza/',
'magaziny/stroitelnyie-materialyi/kompozitnaya-cherepicza/',
'magaziny/stroitelnyie-materialyi/krovelnyie-materialyi.html/',
'magaziny/stroitelnyie-materialyi/kryishki-dlya-stolbov/',
'magaziny/stroitelnyie-materialyi/lentyi-uplotnitelnyie/',
'magaziny/stroitelnyie-materialyi/les-angar.html/',
'magaziny/stroitelnyie-materialyi/magazin-sklad-suxie-smesi.html/',
'magaziny/stroitelnyie-materialyi/mebelnyij-shhit/',
'magaziny/stroitelnyie-materialyi/metallocherepicza/',
'magaziny/stroitelnyie-materialyi/mineralnaya-vata/',
'magaziny/stroitelnyie-materialyi/orientirovanno-struzhechnyie-plityi-osp-osb/',
'magaziny/stroitelnyie-materialyi/paroizolyaczionnyie-materialyi/',
'magaziny/stroitelnyie-materialyi/pazogrebnevyie-plityi-pgp/',
'magaziny/stroitelnyie-materialyi/penobloki/',
'magaziny/stroitelnyie-materialyi/peskobeton/',
'magaziny/stroitelnyie-materialyi/planken/',
'magaziny/stroitelnyie-materialyi/plitka-trotuarnaya-bruschatka/',
'magaziny/stroitelnyie-materialyi/podvesyi-dlya-gipsokartona/',
'magaziny/stroitelnyie-materialyi/polyi-nalivnyie/',
'magaziny/stroitelnyie-materialyi/profil-dlya-gipsokartona/',
'magaziny/stroitelnyie-materialyi/profnastil/',
'magaziny/stroitelnyie-materialyi/setki-malyarnyie-shtukaturnyie/',
'magaziny/stroitelnyie-materialyi/smesi-kleevyie/',
'magaziny/stroitelnyie-materialyi/smesi-shpaklevochnyie/',
'magaziny/stroitelnyie-materialyi/smesi-shtukaturnyie/',
'magaziny/stroitelnyie-materialyi/smesi-zatirochnyie/',
'magaziny/stroitelnyie-materialyi/sofityi-krovelnyie/',
'magaziny/stroitelnyie-materialyi/strojmet.html/',
'magaziny/stroitelnyie-materialyi/svajnyie-fundamentyi/',
'magaziny/stroitelnyie-materialyi/ugolok-derevyannyij/',
'magaziny/stroitelnyie-materialyi/vagonka/',
'magaziny/stroitelnyie-materialyi/vagonka-shtil/',
'magaziny/stroitelnyie-materialyi/vestmet.html/',
'magaziny/stroitelnyie-materialyi/vodostoki-metallicheskie/',
'magaziny/stroitelnyie-materialyi/vodostoki-plastikovyie/',
'magaziny/stroitelnyie-materialyi/volnistyie-bitumnyie-listyi-evroshifer/',
'magaziny/uslugi-i-servis/',
'magaziny/uslugi-i-servis/izgotovlenie-vitrazhej/',
'magaziny/uslugi-i-servis/krovelnyie-rabotyi/',
'magaziny/uslugi-i-servis/makita-servis-plus.html/',
'magaziny/uslugi-i-servis/montazh-sajdinga/',
'magaziny/uslugi-i-servis/remont-elektricheskogo-i-benzinovogo-instrumenta/',
'magaziny/uslugi-i-servis/zapchasti-dlya-elektricheskogo-i-benzinovogo-instrumenta/',
'magaziny/ventilyacziya-i-kondiczionirovanie/',
'magaziny/ventilyacziya-i-kondiczionirovanie/dyimoxodyi-iz-keramiki/',
'magaziny/ventilyacziya-i-kondiczionirovanie/dyimoxodyi-iz-stali/',
'magaziny/ventilyacziya-i-kondiczionirovanie/krovelnaya-ventilyacziya/',
'magaziny/ventilyacziya-i-kondiczionirovanie/ventilyacziya-promyishlennaya/',
'magaziny/vodosnabzhenie-i-vodootvedenie/',
'magaziny/vodosnabzhenie-i-vodootvedenie/drenazhnyie-sistemyi/',
'magaziny/zdaniya-sooruzheniya-konstrukczii/',
'magaziny/zdaniya-sooruzheniya-konstrukczii/pechi-barbekyu-sadovyie/',
'magaziny/zdaniya-sooruzheniya-konstrukczii/zaboryi-i-ograzhdeniya/'
}

def show_sind(request):
    print 'show_sind'
    dic=[]
    i=1
    lenlist=len(nmlist)
    for uri in nmlist:
        print '%d of %d' % (i,lenlist)
        dic1=parse_sind(uri)
        dic.append(dic1)
        i += 1
    #for key,value in dic:
    #    print key,value
    print '==ok=='
    xls_sind(dic)
    return redirect("/")

def xls_sind(bf):
    print 'xls_sind'
    # Create a workbook and add a worksheet.
    #dt=datetime.datetime.today()
    #filename='media/sind-%s-%s-%s.xlsx'%(dt.day, dt.hour, dt.minute)
    filename='media/sindika.xlsx'
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:D', 25)

    format0 = workbook.add_format({'align': 'left'})


    bold = workbook.add_format({'align': 'left', 'bold': True})

    print 'xls created', filename
    try:
        row = 0
        worksheet.write(row, 0, u'Категория', bold)
        worksheet.write(row, 1, u'Павильон', bold)
        worksheet.write(row, 2, u'Описание', bold)
        worksheet.write(row, 3, u'Бренды', bold)
        worksheet.write(row, 4, u'Телефоны', bold)
        #
        row = 1
        for url1 in bf:
            for key_cat,v in url1:
                col = 0
                worksheet.write(row, col, key_cat, format0)
                for key,value in v:
                    col += 1
                    print row,col, key,value
                    if isinstance(value, str):
                        #print "--ordinary string--"
                        uvalue=value.decode('utf-8')
                    elif isinstance(value, unicode):
                        #print "--unicode string--"
                        uvalue=value
                    else:
                        print "--not a string--"

                    #uvalue=u'юникод строка'
                    try:
                        worksheet.write(row, col, uvalue, format0)
                    except Exception as ex:
                        print ex

                row += 1
        #
    except Exception as ex:
        print ex
    #
    print 'close', filename
    workbook.close()
