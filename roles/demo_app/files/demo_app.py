from flask import Flask, request, json, jsonify, Response
from flask.ext.pymongo import PyMongo
import datetime
import isodate
import hashlib

app_name = "mulloy_demo"

app = Flask(app_name)
mongo = PyMongo(app)

app.debug = True

@app.route("/clear_db")
def clear_db():
    mongo.db.events.remove()
    return ""

@app.route("/output_db")
def output_db():
    db_data = mongo.db.events.find()
    output = []
    for record in db_data:
        record_out = {}
        for key,value in record.iteritems():
            if isinstance(value, datetime.datetime):
                record_out[key] = value.isoformat()
            elif key == '_id': 
                record_out[key] = str(value)
            else: 
                 record_out[key] = value
#                record_out[key] = str(type(value))
#                record_out[key] = 'foobar'
        output.append(record_out)
    json_str = json.dumps(output, indent=4, separators=(',', ': '))
    return Response(json_str, mimetype='application/json')


@app.route("/get_count", methods=['GET'])
def get_count():
    #use mulloy_demo
    #db.events.find()
    #db.events.find( { "date": new Date("2015-05-13") } )
    #return "Get User\n"
    uid_param = request.args.get('uid')
    date_param = request.args.get('date')

    assert date_param != None
    assert uid_param != None

    uid = int(request.args.get('uid'))
    #date = isodate.parse_datetime(date_param)
    date = datetime.datetime.strptime(date_param, '%Y-%m-%d')
    #return "uid: " + uid + " date: " + date  
    output = ''
    cursor = mongo.db.events.find( { "date": date , "uid": uid} )
    for record in cursor:
        output = output + "_id: " + str(record['_id']) + " "
        output = output + "uid: " + str(record['uid']) + " "
        output = output + "timestamp: " + str(record['timestamp']) + "\n"
    return jsonify(count=cursor.count())

@app.route("/store", methods=['POST'])
def store():
    # TODO: Proper error page
    if request.content_type != "application/json":
        return "Invalid content type: \"" + request.content_type + "\""
    input_data = json.loads(request.data)
    output = ""
    req_keys = set(['uid', 'name', 'date', 'md5checksum'])
    if not isinstance(input_data, list):
        return "Invalid data, must provide array of objects"
    for item in input_data:
        # Very strict checking of keys
        if not req_keys == set(item.keys()):
            return "Invalid item (keys don't match required set): " + json.dumps(item)

        #TODO: Validate uid is integer
        uid = int(item['uid'])
        name = item['name']
        raw_date = item['date']
        #TODO: Validate checksum
        md5checksum = item['md5checksum']
        md5_str = '{"date": "' + item['date'] + '", "uid": "' + item['uid'] + '", "name": "' + item['name'] + '"}'
        m = hashlib.md5()
        m.update(md5_str)
        calc_md5 = m.hexdigest()

        if calc_md5 != md5checksum:
            return "Invalid md5checksum (" + calc_md5  + ") for: " + json.dumps(item), 400

        #TODO: Validate date is a valid timestamp
        timestamp = isodate.parse_datetime(raw_date)
        # Hack to convert timestamp to timestamp at midnight
        # Can't find a good way to make mongo return records by date
        date = datetime.datetime.combine(timestamp.date(), datetime.datetime.min.time())

        cursor = mongo.db.events.find( { "timestamp": timestamp , "uid": uid, "name": name} )
        if cursor.count() != 0:
            return "Item already exists in database: " + json.dumps(item)
        mongo_obj = {
            'uid': uid,
            'name': name,
            'md5checksum': md5checksum,
            'timestamp': timestamp,
            'date': date,
        }
        mongo.db.events.insert(mongo_obj)
        #output = output + " " + json.dumps(mongo_obj) 
        output = output + " " + str(timestamp)
    return output

if __name__ == "__main__":
    app.run(port=8080,host="0.0.0.0")
