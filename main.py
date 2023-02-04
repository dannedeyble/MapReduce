# map.json time sleep 5 s
# reduce.json time sleep 10800
import json
import os
import requests
from datetime import datetime, timedelta
from time import sleep

re = requests

# Url de requisição
url = 'https://hcomunicaapi.cnj.jus.br/api/v1/comunicacao'
conttrole_time = datetime.now()
cont = 1
# time i segundos
req_ps = 2
# time em horas
reduce_rt = 10
def dormir(sec=1):
    for x in range(1, sec):
        print("\n", end='')
        print(f'estou no segundo:  ', x, end='')
        sleep(1)

def reduce():
    with open(f'map.txt', 'r') as arq:
        filename=arq.name
        list_erros=[]
        while True:
            read=arq.readline()
            if read == '':
                break
            print(read)
            read = json.loads(read)
            if read['status_code'] != 200:
                list_erros.append(read['uuid'])
        if len(list_erros) > 0:
            status_ok = False
        else:
            status_ok = True

        line={'filename' : arq.name,
              'status_ok' : status_ok,
              'list_erros' : list_erros
              }
    with open('reduce.txt', 'a') as arq:
        line = json.dumps(line)
        print(line)
        arq.write(line)



    pass

def map():
    re = requests

    # Url de requisição
    url = 'https://hcomunicaapi.cnj.jus.br/api/v1/comunicacao'
    conttrole_time = datetime.now()
    cont = 1
    # time i segundos
    req_ps = 2
    # time em horas
    reduce_rt = 30

    while True:
        response = re.get(url=url)
        with open(f'map.txt', 'a') as arq:
            resut = json.loads(response.text)
            if f'{response.status_code}'[-1] != "0":
                sud_status = response.status_code
            else:
                sub_status = 0

            line = {
                'uuid': cont,
                'time': str(datetime.now()),
                'status_code': response.status_code,
                'sub_statuscode': sub_status,
                'headers' : str(response.headers),
                'content': response.text
            }
            line = json.dumps(line)
            arq.write(line)
            arq.write('\n')
        if conttrole_time + timedelta(seconds = reduce_rt) <= datetime.now():
            reduce()
            conttrole_time=datetime.now()
        cont += 1
        dormir(req_ps)


if __name__ == '__main__':
    # map()
    reduce()