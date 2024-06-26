"""Flask app for Cupcakes"""
from models import db, connect_db, Cupcake
from flask import Flask, redirect, render_template, session, request, jsonify, flash
from forms import AddCupcakeForm
import requests
from pdb import set_trace

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'

app.app_context().push()
connect_db(app)

@app.route('/')
def home():
    form = AddCupcakeForm()
    return render_template('index.html', form=form)

@app.route('/', methods=['POST'])
def add_cupcake():
    form = AddCupcakeForm()
    if form.validate_on_submit():
        flash('Cupcake successfully added!')
        return redirect('/')
    else:
        return render_template('index.html', form=form)

@app.route('/cupcakes/search')
def find_cupcakes():
    search_term = request.args.get('cupcake')
    results = db.session.query(Cupcake).filter(Cupcake.flavor.ilike(f'%{search_term}%')).all()
    cupcakes = [{'id': cupcake.id, 'flavor': cupcake.flavor, 'size': cupcake.size, 'rating': cupcake.rating, 'image': cupcake.image} for cupcake in results]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes')
def get_all_cupcakes():
    '''Returns data about each cupcake instance'''
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return (jsonify(cupcakes=all_cupcakes), 200)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    '''Returns data about certain cupcake'''
    cupcake = Cupcake.query.get_or_404(id)
    return (jsonify(cupcake=cupcake.serialize()), 200)
    

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    '''Create cupcake with flavor, size, rating, and image data'''
    flavor, size, rating, image = request.json['flavor'], request.json['size'], request.json['rating'], request.json.get('image', 'https://tinyurl.com/demo-cupcake')
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()
    return (jsonify(cupcake=new_cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    '''Update cupcake'''
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return (jsonify(cupcake=cupcake.serialize()), 200)

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    '''Delete Cupcake'''
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return (jsonify(result='Cupcake successfully deleted'), 200)