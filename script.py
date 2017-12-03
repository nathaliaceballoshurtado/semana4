#!/usr/bin/python

import requests
import json
import subprocess
import datetime
#
# Monitoring Upload
#
time = {'time': '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())}
who = requests.get('http://localhost:5000/who')
os = requests.get('http://localhost:5000/os/kernel')
swap = requests.get('http://localhost:5000/swap/so')
mem = requests.get('http://localhost:5000/mem/free')
cpu = requests.get('http://localhost:5000/cpu/sy')
disk = requests.get ('http://localhost:5000/disk')
dicSwap = swap.json()
dicWho = who.json()
dicOs = os.json()
dicMem = mem.json()
dicCpu = cpu.json()
dicDisk = disk.json()
datos = {**dicWho, **dicOs, **dicSwap, **dicMem, **dicCpu, **dicDisk, **time}
print (datos)
post = requests.post('https://intranet-heroku.herokuapp.com/monitoring', json = datos)
print (post.status_code)









##--------------------------------------------
keys = ['ID', 'progress', 'downloaded' ,'unit' , 'time','timeunit', 'speedup', 'speeddown', 'ratio', 'up', 'y', 'status-1', 'name']
keysAux = ['ID' ,'progress',  'downloaded', 'unit','ETA', 'speedup', 'speeddown', 'ratio', 'status-1',  'name']
keys2 = ['ID', 'progress', 'downloaded' ,'ETA', 'speedup', 'speeddown', 'ratio', 'status-1', 'name']
##--------------------------------------------
urls = requests.get('https://intranet-heroku.herokuapp.com/consultasDescargas')
dicUrls = urls.json()
values = dicUrls.values()

for link in values:
  ##  print (link)
    subprocess.check_output(["transmission-remote", '--auth', 'transmission:transmission' , "-a", link])
##----------------------------------------------
def listar (value):

    transmission = subprocess.Popen(['transmission-remote', '--auth', 'transmission:transmission' , '-l'],stdout = subprocess.PIPE)
    tail = subprocess.Popen(['tail', '-n' , '+2'], stdin = transmission.stdout,stdout = subprocess.PIPE)
    tr = subprocess.Popen(['tr', '-s' , ' '], stdin = tail.stdout, stdout = subprocess.PIPE)

    output = subprocess.check_output(['cut' , '-d', '\n', '-f', str(value)], stdin = tr.stdout).decode('utf-8').strip()
    return output

def hacerURLs():
    x = 1
    datos = []
    while True:
        aux = listar(x)
        print ("listar: " + str (aux) ) 
        if ((aux.find("Sum:")) != -1)  :
            break
        else:
            x += 1

        data = {}

      
        if ((aux.find("Up & Down")) == -1):
            values = aux.split(" ")
            print ("values 1\n " )
            print (str(values))
            for i in range (0 , 10): 
                    data[keysAux[i]] = values[i]
                  
        

        elif ((aux.find ("None")) != -1):
            values = aux.split(" ")
            print ("values 2 \n" )
            for j in range (0,8)  : 
                data[keys2[i]] = values [j]   
                  

        else:
            values = aux.split(" ")    
            print ("values 3 \n" ) 
            for j in range (0, 13): ##12
                data[keys[j]] = values[j]
        datos.append(data)
        print ( "\n") 
        print (str (values) + "\n")
        for key in data :
            print ( key +": "+  data[key])
    return datos


post = requests.post('https://intranet-heroku.herokuapp.com/estadoDescargas', json = hacerURLs())
print (post.status_code	)

