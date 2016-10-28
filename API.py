from flask import request, url_for
from flask.ext.api import FlaskAPI
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
	ps = db.prepare("SELECT * FROM masterlist WHERE name LIKE '{}'".format(str(name)))
	print("SELECT * FROM masterlist WHERE name = '{}'".format(str(name)))
	return (json.dumps(ps()))

if __name__ == "__main__":
    app.run(debug=True)