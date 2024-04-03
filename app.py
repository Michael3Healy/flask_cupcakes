"""Flask app for Cupcakes"""
from models import db, connect_db, Cupcake
from flask import Flask, redirect, render_template, session, request, jsonify
import requests
from pdb import set_trace

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'

app.app_context().push()
connect_db(app)

@app.route('/api/cupcakes')
def get_all_cupcakes():
    '''Returns data about each cupcake instance'''
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return (jsonify(cupcakes=all_cupcakes), 200)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    return (jsonify(cupcake=cupcake.serialize()), 200)
    '''Returns data about certain cupcake'''

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    '''Create cupcake with flavor, size, rating, and image data'''
    flavor, size, rating, image = request.json['flavor'], request.json['size'], request.json['rating'], request.json['image']
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()
    return (jsonify(cupcake=new_cupcake.serialize()), 201)

