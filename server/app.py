#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Bakery, BakedGood  # Adjusted to import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    name = request.form['name']
    price = request.form['price']
    bakery_id = request.form.get('bakery_id')  # Assuming it's optional
    new_baked_good = BakedGood(name=name, price=price, bakery_id=bakery_id)
    db.session.add(new_baked_good)
    db.session.commit()
    return jsonify(new_baked_good.to_dict()), 201

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    if 'name' in request.form:
        bakery.name = request.form['name']
        db.session.commit()
    return jsonify(bakery.to_dict()), 200

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get_or_404(id)
    db.session.delete(baked_good)
    db.session.commit()
    return jsonify({'message': 'The baked good has been successfully deleted.'}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
