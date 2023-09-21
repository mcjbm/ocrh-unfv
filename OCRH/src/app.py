from flask import Flask, render_template, request, redirect, url_for, flash,jsonify

from flask_mysqldb import MySQL

from datetime import date

from config import config

#models
from models.ModelUser import ModelUser

#entities
from models.entities.User import User

#controladores
from controlador_reg import Control_reg
from controlador_escalofon import Control_escalofon

app = Flask(__name__)
app.config.from_object(config['development'])
db = MySQL(app)

@app.route('/')
def index():
       return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
        if request.method == 'POST':
                
                user = User(1,request.form['email'],request.form['password'])
                logged_user = ModelUser.login(db,user)
                if logged_user != None:
                        if logged_user.password:
                                return redirect(url_for('modules'))
                        else:
                                flash('Usuario inválido...')
                                return render_template('auth/login.html')
                else:
                       flash('Usuario no encontrado...')
                       return render_template('auth/login.html')   
        else:
                return render_template('auth/login.html')

@app.route('/home')
def home():
       return render_template('home.html')

@app.route('/modules')
def modules():
       return render_template('modules.html')

@app.route('/laborales',methods=['GET','POST'])
def laborales():
       if request.method == 'POST':
              today = date.today() # PARA COPTURAR LA FECHA
              codper = request.form["codper"]
              iduser = 1
              aneuno = request.form.get("aneuno","")
              anedos = request.form.get("anedos","")
              hrsci = int(request.form["hrsci"])
              hrscni = int(request.form["hrscni"])
              tothrs = int(request.form["tot_hrs_dict"])
              hrsdes = int(request.form["hrsdes"])
              observacion = request.form["observ"]
              anoreg = today.year
              mesreg = today.month
              diareg = today.day
              numnt = request.form.get("num_nt","")
              comentario = request.form.get("comentario","")
              tiptotrei = request.form.get("tip-totrei","")
              totrei = float(request.form.get("totrei",""))
              destotrei = request.form.get("descrip-totrei","")
              fmes = request.form.get("fmes_reg","")
              fano = int(request.form.get("fano_reg",""))
              control_reg_instance = Control_reg()
              control_reg_instance.insertar_reg(db, codper, iduser, aneuno, anedos, hrsci, hrscni, tothrs, hrsdes, observacion, anoreg, mesreg, diareg, numnt, comentario, tiptotrei, totrei, destotrei, fmes, fano)
       
       #Se selecciona los valores para el combobox 
       # Si se envía una solicitud de búsqueda
       if 'query' in request.args:
              query = request.args.get('query', '')
              control_reg_instance = Control_reg()
              results = control_reg_instance.buscar_reg(db, query)  # Modificar la función buscar_reg
              return jsonify(results)

       lista = Control_reg.obtener_reg(db)
       lista_empleados = Control_reg.obtener_empleado(db)
       return render_template('laborales.html', lista = lista, lista_e = lista_empleados)

       #return render_template('laborales.html')

#AUTOCOMPLETAR FORMULARIO NUEVO REGISTRO

@app.route('/autocompletar', methods=['GET','POST'])
def autocompletar():
    try:
       nombre = request.form.get('search_reg')  # Obtén el valor seleccionado del campo de entrada
       cursor= db.connection.cursor()
       # Ejecuta una consulta SQL para obtener los valores de código e id_clase
       cursor.execute("SELECT e.nombre AS nombre, codigo, dni, id_clase, id_cat, id_tipo, hrs_sem, hrs_men, f.nombre AS nombre_facultad FROM empleado e LEFT JOIN facultades f ON e.id_facultad = f.id_facultad WHERE e.nombre = %s", (nombre,))
       result = cursor.fetchone()
       print(result)
       # Comprueba si se encontraron resultados
       if result:
              
              nombre, codigo, dni, id_clase, id_cat, id_tipo, hrs_sem, hrs_men, nombre_facultad = result
       else:
              nombre, codigo, dni, id_clase, id_cat, id_tipo, hrs_sem, hrs_men, nombre_facultad = "", "", "", "", "", "", "", "", ""
       # Devuelve los valores como una respuesta JSON
       response = {'nombre': nombre,'codigo': codigo, 'dni': dni,'id_clase': id_clase, 'id_cat':id_cat, 'id_tipo': id_tipo, 'hrs_sem':hrs_sem, 'hrs_men':hrs_men, 'nombre_facultad': nombre_facultad}
       cursor.close()
       return jsonify(response)
    
    except Exception as e:
        # Manejo de excepciones
        return jsonify({'error': str(e)})


@app.route('/perfil-laboral')
def perfil_laboral():
       return render_template('perfil_laboral.html')

@app.route('/escalofon',methods=['GET','POST'])
def escalofon():
       #Se selecciona los valores para el combobox 
       # Si se envía una solicitud de búsqueda
       if 'query' in request.args:
              query = request.args.get('query', '')
              control_esc_instance = Control_escalofon()
              results = control_esc_instance.buscar_esc(db, query)  # Modificar la función buscar_reg
              return jsonify(results)
       
       
       lista_empleados = Control_escalofon.obtener_empleado(db)
       control_esc_instance = Control_escalofon()
       lista_facultades = control_esc_instance.combobox_esc(db)
       return render_template('escalofon.html', lista = lista_empleados, facultades = lista_facultades)

#COMBOBOX-ESCALOFON


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()

