import flask
from flask import Flask, render_template,request
import sqlite3

from werkzeug.utils import redirect

app1 = Flask(__name__)

con = sqlite3.connect("hospitalmangsystem.db",check_same_thread=False)

listOfTables = con.execute("SELECT name from sqlite_master WHERE type='table' AND name='PATIENT' ").fetchall()

if listOfTables!=[]:
    print("Table Already Exists ! ")

else:
    con.execute(''' CREATE TABLE PATIENT(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT,
    MOBILENO TEXT,
    AGE TEXT,
    ADDRESS TEXT,
    DOB INTEGER,
    PLACE TEXT,
    PINCODE TEXT); ''')
    print("Table has created")


@app1.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        getUname = request.form["username"]
        getppass = request.form["password"]

        if getUname == "admin":
            if getppass == "12345":
                return redirect("/dashboard")
    return render_template("login.html")


@app1.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        getMobno = request.form["mobno"]
        cur2 = con.cursor()
        cur2.execute("SELECT * FROM PATIENT WHERE MOBILENO = '"+getMobno+"' ")
        res2 = cur2.fetchall()
        return render_template("searchview.html", patients2=res2)
    return render_template("search.html")


@app1.route("/update", methods=["GET","POST"])
def detup():
    if request.method == "POST":
        getMobileNO = request.form["mobileeno"]
        getNewname = request.form["newname"]
        getNewAge = request.form["newage"]
        getNewAddress = request.form["newaddress"]
        getNewPlace = request.form["newplace"]
        getNewPincode = request.form["newpincode"]
        con.execute("UPDATE PATIENT SET NAME = '"+getNewname+"',AGE = '"+getNewAge+"',ADDRESS='"+getNewAddress+"',PLACE = '"+getNewPlace+"',PINCODE = '"+getNewPincode+"' WHERE MOBILENO = '"+getMobileNO+"' ")
        print("successfully Updated !")
        con.commit()
        return redirect("/view")
    return render_template("detailsupdate.html")


@app1.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        getMobno = request.form["mobno"]
        cur3 = con.cursor()
        cur3.execute("DELETE FROM PATIENT WHERE MOBILENO = '"+getMobno+"' ")
    return render_template("delete.html")


@app1.route("/view")
def view():
    cur = con.cursor()
    cur.execute("SELECT * FROM PATIENT")
    res = cur.fetchall()
    return render_template("viewall.html", patients=res)


@app1.route("/dashboard", methods=["GET", "POST"])
def dash():
    if request.method == "POST":
        getName = request.form["name"]
        getMobileno = request.form["mobileno"]
        getAge = request.form["age"]
        getAddress = request.form["address"]
        getDob = request.form["dob"]
        getPlace = request.form["place"]
        getPincode = request.form["pincode"]
        print(getName)
        print(getMobileno)
        print(getAge)
        print(getAddress)
        print(getDob)
        print(getPlace)
        print(getPincode)
        try :
            con.execute("INSERT INTO PATIENT(NAME,MOBILENO,AGE,ADDRESS,DOB,PLACE,PINCODE) VALUES('"+getName+"','"+getMobileno+"','"+getAge+"','" +getAddress+"','"+getDob+"','"+getPlace+"','"+getPincode+"')")
            print("successfully inserted !")
            con.commit()
            return redirect("/view")
        except Exception as e:
            print(e)
    return render_template("dashboard.html")


if __name__ == "__main__":
    app1.run()