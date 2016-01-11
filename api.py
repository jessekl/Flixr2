from flask import Flask, jsonify, make_response,abort, redirect, url_for,render_template
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy
from sqlitedict import SqliteDict

auth = HTTPBasicAuth()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

flixrdb = SqliteDict('./movies.sqlite', autocommit=True)
db = SQLAlchemy(app)

class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)

@app.route('/api/v1.0/movies/<int:movie_id>', methods=['GET','POST'])
@auth.login_required
def get_movie(movie_id):
	try:
		return jsonify({'movie':flixrdb[movie_id]})
	except:
		return make_response(jsonify({'error':'Movie not found'}),404)


@app.route('/api/v1.0/movies', methods=['GET','POST'])
# @auth.login_required
def get_movies():
	return jsonify({'movies':flixrdb[0]})

@auth.get_password
def get_password(username):
	#some logic 
	if username == 'jesse':
		return 'password'
	return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error':'You shall not pass'}),404)




if __name__=='__main__':
	db.create_all()
	app.run(debug=True)
