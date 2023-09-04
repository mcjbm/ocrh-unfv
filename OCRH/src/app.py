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

app = Flask(__name__)
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
              today = date.today()
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
              control_reg_instance = Control_reg()
              control_reg_instance.insertar_reg(db, codper, iduser, aneuno, anedos, hrsci, hrscni, tothrs, hrsdes, observacion, anoreg, mesreg, diareg)
       
       # Si se envía una solicitud de búsqueda
       if 'query' in request.args:
              query = request.args.get('query', '')
              control_reg_instance = Control_reg()
              results = control_reg_instance.buscar_reg(db, query)  # Modificar la función buscar_reg
              return jsonify(results)

       lista = Control_reg.obtener_reg(db)
       return render_template('laborales.html', lista = lista)

       #return render_template('laborales.html')

@app.route('/perfil-laboral')
def perfil_laboral():
       return render_template('perfil_laboral.html')

@app.route('/escalofon')
def escalofon():
       return render_template('escalofon.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()