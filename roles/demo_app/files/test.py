import requests
import json

base_url = "http://localhost:8080"

pass_count = 0
fail_count = 0

def pretty_json(input):
    return json.dumps(input, indent=4, separators=(',', ': '))

def check_response(response, expected_json, expected_status_code = 200):
    global pass_count
    global fail_count

    if response.status_code != expected_status_code:
        pass # Exit if block, return Fail
    elif expected_json == None or response.json() == expected_json:
        pass_count += 1
        print "Pass"
        return True
    fail_count += 1
    print "Fail"
    print "Status Code: " + str(response.status_code) + " Expected: " + str(expected_status_code)
    print "Response: " + response.text
    return False


def load_data(data, expected_status_code=200):
    json_str = json.dumps(data)
    print "Loading Data: ", pretty_json(data)
    headers = {'Content-type': 'application/json'} 
    response = requests.post(base_url + "/store", headers=headers, data=json_str)
    print "Data Load:",
    return check_response(response, None, expected_status_code)

def check_counts(params, expected_count):
    print "Checking /get_counts=" + str(expected_count) + " for params " + str(params) + ": ",

    response = requests.get(base_url + '/get_count', params=params)
    check_response(response, {'count': expected_count})

test_data_1 =  [
    {"uid": "1",
     "name": "John Doe",
     "date": "2015-05-12T14:36:00.451765",
     "md5checksum": "e8c83e232b64ce94fdd0e4539ad0d44f"
    },
    {"uid": "1",
     "name": "John Doe",
     "date": "2015-05-12T15:36:00.451765",
     "md5checksum": "db72280ffe679e4435c60a5ed31bdef7"
    },
    {"uid": "2",
     "name": "Jane Doe",
     "date": "2015-05-14T14:36:00.451765",
     "md5checksum": "e9cda39188a534e584b0502b381c827f"
    },
    {"uid": "2",
     "name": "Jane Doe",
     "date": "2015-05-15T12:12:00.352465",
     "md5checksum": "da91acb9b0b94976b7fc7a4f60d2fd17"
    },
]
# Bad MD5
test_data_bad_md5 = [
    {'uid': '2',
     'name': 'Jane Doe',
     'date': '2015-05-13T14:36:00.451765',
     'md5checksum': 'b419795d50db2a35e94c8364978d898f'
    },
]

print "Clearing Database"
response = requests.get(base_url + '/clear_db')

print "Checking DB Empty:",
response = requests.get(base_url + '/output_db')
check_response(response, [])

print "Loading initial test data"
load_data(test_data_1)

check_counts({'uid': 1, 'date': '2015-05-12'}, 2)
check_counts({'uid': 1, 'date': '2015-05-13'}, 0)
check_counts({'uid': 1, 'date': '2015-05-14'}, 0)
check_counts({'uid': 1, 'date': '2015-05-15'}, 0)

check_counts({'uid': 2, 'date': '2015-05-12'}, 0)
check_counts({'uid': 2, 'date': '2015-05-13'}, 0)
check_counts({'uid': 2, 'date': '2015-05-14'}, 1)
check_counts({'uid': 2, 'date': '2015-05-15'}, 1)

print "Loading test data again to test duplicate detection"
load_data(test_data_1, expected_status_code=400)

check_counts({'uid': 1, 'date': '2015-05-12'}, 2)
check_counts({'uid': 1, 'date': '2015-05-13'}, 0)
check_counts({'uid': 1, 'date': '2015-05-14'}, 0)
check_counts({'uid': 1, 'date': '2015-05-15'}, 0)

check_counts({'uid': 2, 'date': '2015-05-12'}, 0)
check_counts({'uid': 2, 'date': '2015-05-13'}, 0)
check_counts({'uid': 2, 'date': '2015-05-14'}, 1)
check_counts({'uid': 2, 'date': '2015-05-15'}, 1)

print "Testing bad MD5 rejection"
result = load_data(test_data_bad_md5, expected_status_code=400)

print "Bad MD5 rejection:",
if result:
    pass_count += 1
    print "Pass"
else:
    fail_count += 1
    print "Fail"

print "Pass:", pass_count
print "Fail:", fail_count
