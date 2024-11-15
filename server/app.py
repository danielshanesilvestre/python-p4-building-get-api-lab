#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_dicts = []
    for bakery in bakeries:
        bakeries_dicts.append(bakery.to_dict())
    
    return make_response(
        bakeries_dicts,
        200
    )

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if bakery:
        return make_response(
            bakery.to_dict(),
            200
        )
    else:
        return make_response(
            { "message": f"Bakery {id} not found." },
            404
        )

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()
    baked_goods_dicts = []

    for baked_good in baked_goods:
        baked_goods_dicts.append(baked_good.to_dict())

    return make_response(baked_goods_dicts, 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(desc(BakedGood.price)).first()

    if baked_good:
        return make_response(
            baked_good.to_dict(),
            200
        )
    else:
        return make_response(
            { "message": f"Bakery {id} not found." },
            404
        )

if __name__ == '__main__':
    app.run(port=5555, debug=True)
