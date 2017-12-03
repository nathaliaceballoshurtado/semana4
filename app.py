#!/usr/bin/python3
from flask import Flask, request
from flask import render_template
import datetime
from flask import jsonify, make_response
import psycopg2
import urllib.parse as urlparse
import os

urlbd = urlparse.urlparse(os.environ['DATABASE_URL'])
db = urlbd.path[1:]
user = urlbd.username
passw = urlbd.password
host = urlbd.hostname
port = urlbd.port

conn = psycopg2.connect(
            database =db,
            user=user,
            password=passw,
            host=host,
            port=port
            )


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("inicio.html")

@app.route('/monitoring', methods = ['POST'])
def insertarMonitoreo():
    datos = request.get_json(force=True)
    time = datos.get('time')
    user =  datos.get("users")
    os = datos.get('kernel')
    mem = datos.get('mem free')
    swap = datos.get('swap so')
    cpu = datos.get('cpu sy')
    size = datos.get('Disk Size')
    free = datos.get('Free Disk Space')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO monitoring (hora,Memoria , CPU, Swap, Usuario, Sistema, Total, Libre ) VALUES('"""+ time + """ ' , '""" + mem + """ ' , '""" + cpu + """ ' , ' """
                 + swap + """  ' , ' """ + user + """ ' , ' """ + os + """ ' , ' """ + size + """ ' , ' """
                 + free + """ ')""")
    cursor.execute(""" COMMIT """)

    return "Se ha monitoreado el equipo"

@app.route('/consultarMonitoreo', methods = ['GET'])
def consultarMonitoreo():
    cursor = conn.cursor()
    cursor.execute("""Select * from monitoring""")
    rows=cursor.fetchall()
    return render_template("monitoreo.html", rows=rows)

@app.route ('/estadoDescargas' , methods = ['GET', 'POST'] ) 
def estatusDownload() : 
    if request.method == 'POST':
        datos = request.get_json(force=True)
        cur = conn.cursor()
        cur.execute("""DELETE FROM status""")
        cur.execute(""" COMMIT """)
        n = 0
        for dic in datos:
            dic = datos [n]
            name = dic.get('name')
            progress = dic.get('progress')
            ETA = dic.get('ETA')
            status = dic.get('status-1')
            print ("\nname  " + str(name) + "\n progress" + str(progress) + "\n eta " + str (ETA) + "\n status "+  str(status) )  
            cur.execute("""INSERT INTO status (id , procentaje, eta, status, name) VALUES ('""" + str(n+1) + """ ' , ' """
                        + str(progress) + """ ' , ' """ +str(ETA)  + """ ' , ' """
                        + str (status) + """ ' , ' """+ str (name) + """'  ) """ )
            cur.execute("""COMMIT""")

            n += 1
        return "Status upload Successful"

    cur = conn.cursor()
    cur.execute("""SELECT id, name, procentaje, eta, status FROM status""")
    rows = cur.fetchall()
   ## cur.execute("""SELECT uploadtime FROM downloads GROUP BY uploadtime""")
    ##time = cur.fetchone()[0]
    return render_template('descargas.html', rows = rows )



  
@app.route('/insertar', methods = ['GET', 'POST'])
def insertar ():
    cursor = conn.cursor()
    if request.method == 'POST':
        url =  request.form['url']
        id = request.form['id']
        cursor.execute("""INSERT INTO torrent (id, url) VALUES ('""" + id +"""' , '""" + url + """')""")
        cursor.execute(""" COMMIT """)
        return render_template('exito.html')
    else: 
 
        return render_template('subir.html')

def convertirAJson(datosFetch) : 
    n = 1 
    links = {}
    for fetch in datosFetch:
        links ['link ' + str (n) ] = fetch[1]
        n+=1 
    return jsonify (links) 		 
	

@app.route('/consultasDescargas', methods = ['GET', 'POST'] )
def consultarDescarga ():
     cursor = conn.cursor()
     cursor.execute("""SELECT * FROM torrent""")
     filas = cursor.fetchall()
     convertirAJson(filas)  
     cursor.execute("""DELETE FROM torrent""")
     cursor.execute("""COMMIT""") 
     return convertirAJson(filas) 

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port = 5001)
