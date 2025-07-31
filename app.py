from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rezerwacja_user:bezpieczne_haslo@localhost/rezerwacja_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELE
class Sprzet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(100))
    typ = db.Column(db.String(50))
    status = db.Column(db.String(20))

class Uzytkownik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(50))
    nazwisko = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)

class Rezerwacja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_urzadzenia = db.Column(db.Integer, db.ForeignKey('sprzet.id'))
    id_uzytkownika = db.Column(db.Integer, db.ForeignKey('uzytkownik.id'))
    data_start = db.Column(db.DateTime)
    data_koniec = db.Column(db.DateTime)
    status = db.Column(db.String(20))

# ROUTES
@app.route("/sprzet", methods=["GET"])
def get_sprzet():
    sprzety = Sprzet.query.all()
    return jsonify([{"id": s.id, "nazwa": s.nazwa, "typ": s.typ, "status": s.status} for s in sprzety])

@app.route("/rezerwacja", methods=["POST"])
def zloz_rezerwacje():
    data = request.json
    nowa = Rezerwacja(
        id_urzadzenia=data["id_urzadzenia"],
        id_uzytkownika=data["id_uzytkownika"],
        data_start=datetime.strptime(data["data_start"], '%Y-%m-%d'),
        data_koniec=datetime.strptime(data["data_koniec"], '%Y-%m-%d'),
        status="oczekujaca"
    )
    db.session.add(nowa)
    db.session.commit()
    return jsonify({"message": "Rezerwacja złożona"}), 201

if __name__ == "__main__":
    app.run(debug=True)
