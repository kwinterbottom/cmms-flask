# app.py

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///workorders.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class WorkOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='new')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/workorders', methods=['GET'])
def get_orders():
    orders = WorkOrder.query.all()
    return jsonify([
        {'id': o.id, 'title': o.title, 'description': o.description, 'status': o.status}
        for o in orders
    ])

@app.route('/api/workorders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = WorkOrder(title=data['title'], description=data['description'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Work order created!'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
