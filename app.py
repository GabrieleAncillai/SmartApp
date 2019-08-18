# Integrantes del grupo:
# MABEL FABRE 0921722062
# GABRIELE ANCILLAI YB0415159
# MARIELIS MORALES  8-952-345
# YINIVA QUINTERO 9-755-651
# CARLOS NARANJO 4-742-651

from flask import Flask, render_template, request, redirect, url_for, session  # For flask implementation
from bson import ObjectId  # For ObjectId to work
from pymongo import MongoClient
import os
import datetime

app = Flask(__name__)

title = "Smart Accounting"
heading = "Smart Accounting"

client = MongoClient("mongodb://127.0.0.1:27017")  # host uri
db = client.MyAccount  # Select the database

# Collections
Users = db.Users  # Select the collection name
Ingresos = db.Ingresos  # Ingresos
Gastos = db.Gastos # Gastos
Items = db.Items  # Artículos
BankAccounts = db.BankAccounts  # Cuentas de banco


def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')


app.secret_key = 'gay'


# ------------------------------- Renders -------------------------------
@app.route("/")
@app.route("/registro")
def render_register():
    return render_template('register.html')


@app.route("/acceso")
def render_login():
    return render_template('login.html')


# ------------------------------- Funciones de Registro y Login -------------------------------
@app.route("/register", methods=['POST'])
def register():
    # Creating a user
    name = request.values.get("name")
    username = request.values.get("username")
    identification = request.values.get("identification")
    password = request.values.get("password")
    mail = request.values.get("mail")
    gender = request.values.get("gender")
    birthday = request.values.get("birthday")
    birthmonth = request.values.get("birthmonth")
    birthyear = request.values.get("birthyear")
    date = datetime.datetime.now()
    year = int(date.strftime("%Y"))
    month = int(date.strftime("%m"))
    day = int(date.strftime("%d"))
    if (year > int(birthyear) and month >= int(birthmonth) and day >= int(birthday)) or (
            year > int(birthyear) and month > int(birthmonth) and day < int(birthday)):
        age = year - int(birthyear)
    else:
        age = year - int(birthyear) - 1
    Users.insert(
        {"name": name, "username": username, "identification": identification, "password": password, "mail": mail,
         "gender": gender, "age": age})
    return redirect("/acceso")


@app.route("/login", methods=['GET'])
def login():
    # Comprobar que existe el usuario
    ID = request.values.get("ID")
    key = request.values.get("key")
    app.secret_key = key
    session['username'] = ID
    MyUser = Users.find({"identification": ID, "password": key})
    all_l = Iostream.find({"user": session['username'], "password": app.secret_key})
    return render_template('menu.html', a1="active", all=all_l, MyUser=MyUser, title="Bienvenido")


# ------------------------------- Componentes de tabla de opciones superior -------------------------------
@app.route("/home")
def home():
    # Display the all IOStreams
    MyUser = Users.find({"identification": session['username'], "password": app.secret_key})
    title = "Smart Accounting: Inicio"
    a0 = "active"
    return render_template('menu.html', a0=a0, title=title, MyUser=MyUser)

@app.route("/ingresos")
def ingresos():
    # Display the all IOStreams
    MyUser = Users.find({"identification": session['username'], "password": app.secret_key})
    all_l = Ingresos.find({"user": session['username'], "password": app.secret_key})
    title = "Smart Accounting: Ingresos"
    a1 = "active"
    return render_template('menu.html', a1=a1, all=all_l, title=title, MyUser=MyUser)

@app.route("/gastos")
def ingresos():
    # Display the all IOStreams
    MyUser = Users.find({"identification": session['username'], "password": app.secret_key})
    all_l = Gastos.find({"user": session['username'], "password": app.secret_key})
    title = "Smart Accounting: Gastos"
    a1 = "active"
    return render_template('menu.html', a1=a1, all=all_l, title=title, MyUser=MyUser)


@app.route("/banks")
def banks():
    # Display the Uncompleted Tasks
    MyUser = Users.find({"identification": session['username'], "password": app.secret_key})
    all_l = BankAccounts.find({"user": user, "password": password, "state": "undone"})
    title = "Smart Accounting: Bancos"
    a2 = "active"
    return render_template('menu.html', a2=a2, all=all_l, title=title, MyUser=MyUser)

# @app.route("/completed_iostreams")
# def completed_iostreams():
#     # Display the Completed Tasks
#     all_l = Iostream.find({"user": user, "password": password, "state": "done"})
#     a3 = "active"
#     return render_template('menu.html', a3=a3, all=all_l, title=title, heading=heading)
#
#
# @app.route("/provider_iostreams")
# def stats():
#     # Shows the current stats of the event
#     all_l = Iostream.find({"user": user, "password": password, "persontype": "Proveedor"})
#     a4 = "active"
#     return render_template('menu.html', a4=a4, all=all_l, title=title, heading=heading)

# ------------------------------- Condition Done or Undone -------------------------------
@app.route("/done")
def done():
    # Done-or-not ICON
    id = request.values.get("_id")
    task = Iostream.find({"_id": ObjectId(id)})
    if task[0]["state"] == "done":
        Iostream.update({"_id": ObjectId(id)}, {"$set": {"state": "undone"}})
    else:
        Iostream.update({"_id": ObjectId(id)}, {"$set": {"state": "done"}})
    return redirect(redirect_url())


# ------------------------------- IOSTREAMS -------------------------------
@app.route("/addIostream", methods=['POST'])
def addIostream():
    # Adding an Iostream
    product = request.values.get("product")
    ammount = request.values.get("ammount")
    persontype = request.values.get("persontype")
    personname = request.values.get("personname")
    detail = request.values.get("detail")
    account = request.values.get("account")
    state = request.values.get("state")
    cost = request.values.get("cost")
    if persontype == "Proveedor":
        cost = 0 - int(cost)
    date = datetime.datetime.now()
    fecha = date.strftime("%x")
    hora = date.strftime("%X")
    user = session['username']
    password = app.secret_key
    Iostream.insert(
        {"user": user, "password": password, "product": product, "ammount": ammount, "persontype": persontype,
         "personname": personname, "detail": detail, "account": account, "fecha": fecha, "hora": hora, "state": state,
         "cost": cost})
    return redirect("/iostream")


@app.route("/removeIostream")
def removeIostream():
    # Deleting a Task with various references
    key = request.values.get("_id")
    Iostream.remove({"_id": ObjectId(key)})
    return redirect("/iostream")


@app.route("/updateIostream")
def updateIostream():
    id = request.values.get("_id")
    task = Iostream.find({"_id": ObjectId(id)})
    return render_template('update.html', tasks=task, heading=heading, title=title)


@app.route("/updateTaskIostream", methods=['POST'])
def updateTaskIostream():
    # Updating a Task with various references
    product = request.values.get("product")
    persontype = request.values.get("persontype")
    personname = request.values.get("personname")
    detail = request.values.get("detail")
    account = request.values.get("account")
    cost = request.values.get("cost")
    if persontype == "Proveedor":
        cost = 0 - int(cost)
    date = datetime.datetime.now()
    fecha = date.strftime("%x")
    hora = date.strftime("%X")
    user = session['username']
    password = app.secret_key
    id = request.values.get("_id")
    Iostream.update({"_id": ObjectId(id)}, {
        '$set': {"user": user, "password": password, "product": product, "persontype": persontype,
                 "personname": personname, "detail": detail, "account": account, "fecha": fecha, "hora": hora,
                 "cost": cost}})
    return redirect("/iostream")


@app.route("/searchIostream", methods=['GET'])
def searchIostream():
    # Searching a Task with various references
    key = request.values.get("key")
    refer = request.values.get("refer")
    if key == "_id":
        all_l = Iostream.find({refer: ObjectId(key)})
    else:
        all_l = Iostream.find({refer: key})
    return render_template('searchlist.html', all=all_l, title=title, heading=heading)


if __name__ == "__main__":
    app.run(host='192.168.137.188')
    # Code developers: Gabriele Ancillai, Rene de León, Juan García
