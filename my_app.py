from uuid import uuid4
from flask import Flask, jsonify, request
from flask.views import MethodView
from jsonschema import validate, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

import schema


app = Flask('test')
app.config.from_mapping(SQLALCHEMY_DATABASE_URI='postgresql://admin:1234@127.0.0.1:5431/flask_hw')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AdvertModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, index=True)
    body = db.Column(db.String,)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    password = db.Column(db.String, unique=True)
    adverts = db.relationship('AdvertModel', backref='user')


# def health():
#     response = jsonify({'status': 'OK'})
#     # print(response)
#     return response


class UserView(MethodView):

    def get(self, user_id):
        user = UserModel.query.get(int(user_id))
        if not user:
            response = jsonify({'status': 'error', 'message': 'not found'})
            response.status_code = 404
            return response
        return jsonify({
            'id': user_id,
            'name': user.name
        })

    def post(self):
        user_data = request.json
        try:
            validate(request.json, schema.USER)
        except ValidationError as er:
            response = jsonify({'succsess': False, 'error': er.message})
            response.status_code = 400
            return response
        new_user = UserModel(**user_data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(
            {
                'id': new_user.id
            }
        )


class AdvertView(MethodView):

    def get(self, advert_id):
        advert = AdvertModel.query.get(int(advert_id))
        if not advert:
            response = jsonify({'status': 'error', 'message': 'not found'})
            response.status_code = 404
            return response
        return jsonify({
            'id': advert_id,
            'title': advert.title,
            'body': advert.body,
            'owner': advert.owner,
            'created_on': advert.created_on
        })

    def post(self):
        advert_data = request.json
        new_advert = AdvertModel(**advert_data)
        db.session.add(new_advert)
        db.session.commit()
        return jsonify(
            {
                'id': new_advert.id,
                'status': 'ok',
            }
        )

    def delete(self, advert_id):
        advert = AdvertModel.query.get(int(advert_id))
        if not advert:
            response = jsonify({'status': 'error', 'message': 'not found'})
            response.status_code = 404
            return response
        db.session.delete(advert)
        db.session.commit()
        return jsonify({
            'status': 'delete'
        })


# app.add_url_rule('/health', view_func=health, methods=['GET'])
app.add_url_rule('/user/<int:user_id>', view_func=UserView.as_view('get_user'), methods=['GET'])
app.add_url_rule('/user', view_func=UserView.as_view('create_user'), methods=['POST'])

app.add_url_rule('/advert/<int:advert_id>', view_func=AdvertView.as_view('get_advert'), methods=['GET'])
app.add_url_rule('/advert', view_func=AdvertView.as_view('create_advert'), methods=['POST'])
app.add_url_rule('/advert/<int:advert_id>', view_func=AdvertView.as_view('delete_advert'), methods=['DELETE'])

app.run(host='0.0.0.0', port=8080)
