from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask_jsonpify import jsonify

db_connect = create_engine('sqlite:///forecast.db')
app = Flask(__name__)
api = Api(app)


class Cities(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from city")  # This line performs query and returns json result
        return {'cities': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID

    def post(self):
        conn = db_connect.connect()
        rId = request.form['id']
        rName = request.form['name']
        conn.execute("insert into City values (?, ?)", (rId, rName))  # This line performs query and returns json result

        query = conn.execute("select * from city where City =%d " % int(rId))
        result = {'city': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class Cities_Name(Resource):
    def get(self, city_id):
        conn = db_connect.connect()
        query = conn.execute("select * from city where City =%d " % int(city_id))
        result = {'city': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)



api.add_resource(Cities, '/cities')  # Route_1
api.add_resource(Cities_Name, '/cities/<city_id>')  # Route_2

if __name__ == '__main__':
    app.run(port='5002')
