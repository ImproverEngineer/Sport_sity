import requests
from json import *
import pprint as p
import time
import sched as sehed

class Сhampionships(object):
    '''Класс для хранения результатов'''
    def __init__(self,name_cmp, evts):
        self.name_cmp =name_cmp
        self.evts = evts

    def get_count_score(self)->None:
         for values in self.evts:
            for val in self.evts[values]:
                match val:
                    case "name_ht":
                        name_ht = self.evts[values][val]
                        print(name_ht)
                    case "name_at":
                        name_at= self.evts[values][val]
                        print(name_at)
                    case "sc_ev_cmx":
                        sc_ev_cmx = self.evts[values][val]
                        acum = 0
                        for sc_ev in sc_ev_cmx['ext']:
                            acum+=1
                            print('Количество очков в '+self.Alphabetic_notation(acum)+' матче ' + str(sc_ev[0]) +':'+ str(sc_ev[1])+'='+str(sc_ev[0]+sc_ev[1]))

    def Alphabetic_notation(self, number:int)->str:
        match int:
            case 1:
                return 'первый'
            case 2:
                return 'второй'
            case 3:
                return 'третий'
            case _:
                return ''


def parseJson(json:str, championat:str = 46, eventid:bool=False)->'dict':
    '''Распасиваем JSON строку и переводим ее в нужный формат для получения данных по нужным матчам, возврашаем словарь, eventid если нужно включать его в ключ'''
    '''По умалчанию выставляем 46 это настольный тенис, отстольные нужно смотреть в не распарсеном фале'''
    replay = json['reply']
    sports = replay['sports']
    chmps = sports[championat]['chmps'] # настольный тенис, список чемпионатов
    pdict={}
    for chm in chmps: # получаем список чемпионатов
        if eventid:
            pdict[chm+'=>'+chmps[chm]['name_ch']] = chmps[chm] # пишем их в отдельный словарь
        else:
            pdict[chmps[chm]['name_ch']] = chmps[chm]
    return pdict


def get_evts(cmp:dict)->'''dict''':
    '''получить события по чемпионатам'''
    evts=list()
    cmp_list = [v for k, v in cmp.items()]
    cmp_name = ''
    for cmp in cmp_list:
        for key, v in cmp.items():
            if key =='name_ch':
                cmp_name = cmp['name_ch']
            if key=='evts':
                evts.append(Сhampionships(cmp_name,cmp['evts']))
    return evts

def get_calculation_match(chmps:'''list("Сhampionships")''')->object:
    '''Работаем с классом'''
    sc_ev_cmx = dict()
    for chmp in chmps:
        name_ht = ''
        name_at = ''
        gluing_string =''
        for values in chmp.evts:
            for val in chmp.evts[values]:
                match val:
                    case "name_ht":
                        name_ht = chmp.evts[values][val]
                        # print(name_ht)
                    case "name_at":
                        name_at= chmp.evts[values][val]
                        # print(name_at)
                    case "sc_ev_cmx":
                        sc_ev_cmx = chmp.evts[values][val]
                        acum = 0
                        for sc_ev in sc_ev_cmx['ext']:
                            acum+=1
                            gluing_string +='Количество очков в '+str(acum)+' матче ' + str(sc_ev[0]) +':'+ str(sc_ev[1]) +'\n'
                        # print(sc_ev_cmx['main'], sc_ev_cmx['ext'])
            print(chmp.name_cmp)
            print(name_at +' '+ name_ht+'\n' + gluing_string)

##Выполнение основного кода
def main_function():
    try:
        url ='https://ad.betcity.ru/d/on_air/events' # Берем данные с сайта 
        response = requests.get(url, timeout=(5.0,5.0))
    except requests.ConnectionError as e:        
        print("Ошибка подключения")
        return False
    
    body_dict =response.json()
    # with open('Event.txt','w') as file:
    # file.write(body_dict)
    # p.pprint(parseJson(body_dict,'46',eventid=False)) # number: 46 (настольный тенис)
    get_calculation_match(get_evts(parseJson(body_dict,'46',eventid=False)))


    #main_function() # выполнение основного кода
sehedule = sehed.scheduler(time.time,time.sleep)
def discription_shed():
    sehedule.enter(10,2,discription_shed)
    try:
        main_function()
    except Exception as e:
        print("Второе исключение" + e)
## Запуск программы
if __name__ == '__main__':
        discription_shed()
        sehedule.run()
