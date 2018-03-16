# -*- coding: UTF-8 -*-
from flask import Flask
from redis import Redis
from flask import request
from flask import jsonify
from flask import abort
from flask import make_response
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import os
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
redis = Redis(host='redis',port=6379)

now = datetime.datetime.now()
@app.route('/')
def hello():
	redis.incr('counter')
	return 'Viso lankytojų: %s. TV programa %s/%s/%s.' % (redis.get('counter'),now.year, now.month, now.day)

tv_db = [
	{
		'id' : 1,
		'television' : 'LRT TELEVIZIJA',
		'type' : 'Vaidybinis serialas',
		'title' : 'Seserys',
		'start_time' : '05:00',
		'description' : '',
		'release_year' : '2016',
		'legal_age' : 'N-7'
	},
	{
		'id' : 2,
		'television': 'LRT TELEVIZIJA',
		'type' : 'Žinios',
		'title' : 'Žinios',
		'start_time' : '06:30',
		'description' : '',
		'release_year' : '',
		'legal_age' : ''
	},
	{
		'id' : 3,
		'television': 'LNK',
		'type' : 'Animacinis serialas',
		'title' : "Tomas ir Džeris",
		'start_time' : '15:30',
		'description' : '',
		'release_year' : '1980',
		'legal_age' : ''
	},
        {
                'id' : 4,
                'television': 'TV3',
                'type' : 'Kriminalinė drama',
                'title' : 'Specialioji jūrų policijos tarnyba',
                'start_time' : '01:20',
                'description' : '',
                'release_year' : '2011',
                'legal_age' : 'N-7'
        },
        {
                'id' : 5,
                'television': 'Viasat Sport Baltic',
                'type' : 'Krepšinio rungtynės',
                'title' : 'Baskonia-Žalgiris',
                'start_time' : '21:30',
                'description' : 'Eurolygos rungtynės',
                'release_year' : '',
                'legal_age' : ''
        },
        {
                'id' : 6,
                'television': 'BTV',
                'type' : 'Kriminalinė drama',
                'title' : 'Sunkūs laikai',
                'start_time' : '21:00',
                'description' : 'Vaidina Charles Bronson, James Cpburn',
                'release_year' : '1975',
                'legal_age' : ''
        }
]
#404 and 400 error handling
@app.errorhandler(404)
def not_found(error):
    	return make_response(jsonify({'error': 'Not found'}), 404)
@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error': 'Bad request'}), 400)

#GET
#curl -i http://localhost:80/tv_program
@app.route('/tv_program', methods=['GET'])
def program():
        return jsonify(tv_db)
#GET/<OPTION>
#curl -i http://localhost:80/tv_program/<id>
@app.route('/tv_program/<int:id>', methods=['GET'])
def tv_program_element_by_id(id):
	element = []
	for i in tv_db:
		if i['id'] == id:
			element = i
	if len(element) == 0:
		abort(404)
	return jsonify(element)

#POST
#curl -i -H "Content-Type: application/json" - X POST -d '{"title":"<>", "television":"<>","start_time":"<>", etc <optional>}' https://localhost:80/tv_program 
@app.route('/tv_program', methods=['POST'])
def new_element():
    if not request.json or not 'title' in request.json  or not 'television' in request.json or not 'start_time' in request.json:
       abort(400)
    element = {
        'id': tv_db[-1]['id'] + 1,
	'television': request.json['television'],
	'type': request.json.get('type',""),
	'title': request.json['title'],
        'description': request.json.get('description', ""),
	'release_year': request.json.get('release_year', ""),
	'legal_age': request.json.get('legal_age', ""),
	'start_time': request.json['start_time']
    }
    tv_db.append(element)
    response = jsonify({'CREATED':'true'})
    response.status_code = 201
    id=tv_db[-1]['id'] + 1
    response.headers['location'] = '/tv_program/%s' %id
    return response

#PUT
#curl -i -H "Content-Type: application/json" - X PUT -d '{"<>":"<>"}' https://localhost:80/tv_program/<element_id>
@app.route('/tv_program/<int:id>', methods=['PUT'])
def update_element(id):
	element = []
	for i in tv_db:
        	if i['id'] == id:
                        element = i
	if len(element) == 0:
		abort(404)
	if not request.json:
		abort(400)
	element['title'] = request.json.get('title', element['title'])
	element['description'] = request.json.get('description', element['description'])
	element['television'] = request.json.get('television', element['television'])
	element['type'] = request.json.get('type', element['type'])
	element['start_time'] = request.json.get('start_time', element['start_time'])
	element['release_year'] = request.json.get('release_year', element['release_year'])
	element['legal_age'] = request.json.get('legal_age', element['legal_age'])
	return jsonify({'UPDATED':'true'}), 201
#DELETE
#curl -i -H "Content-Type: application/json" -X DELETE http://localhost:80/tv_program/<element_id>
@app.route('/tv_program/<int:id>', methods=['DELETE'])
def delete_element(id):
        element = []
        for i in tv_db:
                if i['id'] == id:
                        element = i
        if len(element) == 0:
                abort(404)
        tv_db.remove(element)
        return jsonify({'DELETED':'true'})

if __name__== "__main__":
	app.run(host="0.0.0.0",debug=True)
