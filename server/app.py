#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource, abort

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        """Return list of all plants as JSON list of dicts."""
        plants = Plant.query.all()
        # Use to_dict() to ensure image is included and price is float
        plants_serialized = [p.to_dict() for p in plants]
        return plants_serialized, 200

    def post(self):
        """Create a new Plant from JSON and return the new plant JSON."""
        data = request.get_json()
        if not data:
            return {"error": "Request must contain JSON body"}, 400

        # Extract fields
        name = data.get('name')
        image = data.get('image')
        price = data.get('price')

        # Validate presence of required fields
        missing = []
        if name is None:
            missing.append('name')
        if image is None:
            missing.append('image')
        if price is None:
            missing.append('price')
        if missing:
            return { "error": f"Missing field(s): {', '.join(missing)}" }, 400

        # Create and commit
        new_plant = Plant(name=name, image=image, price=price)
        db.session.add(new_plant)
        db.session.commit()

        return new_plant.to_dict(), 201

class PlantByID(Resource):
    def get(self, plant_id):
        """Return one Plant by ID, or 404 if not found."""
        plant = Plant.query.get(plant_id)
        if plant is None:
            abort(404, message=f"Plant with id {plant_id} not found")
        return plant.to_dict(), 200

# Register resources
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:plant_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)


