from flask import Flask, render_template, request
import subprocess
app = Flask(__name__)

claves = {'isaac':'trubia4', "ines":"ines"}
peticiones = 0

def procs(re):
    global peticiones, claves
    usuario = re['usuario']
    clave = re['clave']
    seleccion = re['seleccion']
    print(usuario+" "+clave+" "+seleccion)
    if not usuario in claves:
        return 'error'
    if claves[usuario] == clave:
        print("login correcto")
        if seleccion == "ENCENDER-RSTUDIO":
            peticiones = peticiones + 1
            if peticiones == 1:
                subprocess.call("scripts/"+seleccion+".sh")
        if seleccion == "APAGAR-RSTUDIO":
            peticiones -= 1
            if peticiones < 0:
                peticiones = 0
            if peticiones == 0:
                subprocess.call("scripts/"+seleccion+".sh")
        return 'ok peticiones= ' + str(peticiones)
    else:
        return 'error'

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/execute', methods=['POST','GET'])
def execute():
    result = request.form
    re = procs(result)
    if re[:2] == 'ok':
        return render_template("result.html",result={'resultado':re})
    else:
        return render_template("result.html",result={'resultado':'clave incorrecta'})
