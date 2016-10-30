from flask import request, url_for
from flask_api import FlaskAPI
import postgresql
import json 

db = postgresql.open("pq://plancourse:plancourse@plancourse.cwa7n3dmojfl.us-west-2.rds.amazonaws.com")


app = FlaskAPI(__name__)

#tablename : masterlist
@app.route('/get/classes')
def get_classes():
	ps = db.prepare("SELECT DISTINCT(name) from masterlist")
	return (json.dumps(ps()))

@app.route('/get/info/<string:name>')
def get_info(name):
	# WHERE name='{}'".format(str(name))
	ps = db.prepare("SELECT * FROM masterlist WHERE substring(name FROM 1 FOR {})= '{}' ORDER BY uniqueid ASC".format(len(name),str(name)))
	#print("SELECT * FROM masterlist WHERE substring(name FROM 1 FOR {})= '{}'".format(len(name),str(name)))
	return (json.dumps(ps()))

@app.route('/get/info/<string:name>/')
def get_sortedinfo(name):
	#use time to filter results by specified time
	#use select: 0=all classes sorted by time, 1=only classes <= time, 2=only classes >= time
	intime = request.args.get('time')
	select = request.args.get('select')
	if int(select)==0:
		ps = db.prepare("SELECT * FROM masterlist WHERE substring(name FROM 1 FOR {})= '{}' ORDER BY to_timestamp(starttime,'HH:MIAM') ASC".format(len(name),str(name)))
	elif int(select)==1:
		ps = db.prepare("SELECT * FROM masterlist WHERE substring(name FROM 1 FOR {})= '{}' AND to_timestamp(starttime,'HH:MIAM')::time <= '{}' ORDER BY to_timestamp(starttime,'HH:MIAM') ASC"
			.format(len(name),str(name),str(intime)))
	else:
		ps = db.prepare("SELECT * FROM masterlist WHERE substring(name FROM 1 FOR {})= '{}' AND to_timestamp(starttime,'HH:MIAM')::time >= '{}' ORDER BY to_timestamp(starttime,'HH:MIAM') ASC"
			.format(len(name),str(name),str(intime)))
	return (json.dumps(ps()))

if __name__ == "__main__":
    app.run(debug=True)
