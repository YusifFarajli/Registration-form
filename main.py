from flask import Flask, render_template, request,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail,Message
app=Flask(__name__)
app.config["SECRET_KEY"]="myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "fyuskas@gmail.com"
app.config["MAIL_PASSWORD"] = "pkayflynyessxhmn"

db = SQLAlchemy(app)

mail = Mail(app)


class Form(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    Ad = db.Column(db.String(80))
    Soyad = db.Column(db.String(80))
    Telefon_number= db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))

@app.route("/",methods=["GET","POST"])

def index():
    if request.method == "POST":
        Ad = request.form["Ad"]
        Soyad = request.form["Soyad"]
        Telefon_number = request.form["Telefon nömrəniz"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj= datetime.strptime(date,"%Y-%m-%d")
        occupation = request.form["occupation"]

        form=Form(Ad=Ad,Soyad=Soyad,Telefon_number=Telefon_number,
                  email=email,date=date_obj,occupation=occupation)
        db.session.add(form)
        db.session.commit()

        message_body=f"Thank you for your submisson,{Ad}."
        message=Message(subject="New form submission",
                        sender=app.config["MAIL_USERNAME"],
                        recipients=[email],
                        body=message_body)
        mail.send(message)



        flash(f"{Ad},müraciətiniz qeydə alındı!","success")

    return render_template ("index.html")

if __name__== "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)