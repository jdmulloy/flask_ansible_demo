import requests
import json

base_url = "http://localhost:8080"

def pretty_json(input):
    return json.dumps(input, indent=4, separators=(',', ': '))

def load_data(data):
    json_str = json.dumps(data)
    print "Loading Data: ", pretty_json(data)
    headers = {'Content-type': 'application/json'} 
    response = requests.post(base_url + "/store", headers=headers, data=json_str)

def check_counts(params, expected_count):
    print "Checking /get_counts=" + str(expected_count) + " for params " + str(params) + ": ",

    response = requests.get(base_url + '/get_count', params=params)
    if response.json() == {'count': expected_count}:
        print "Pass"
    else:
        print "Fail"

test_data_1 =  [
    {'uid': '1',
     'name': 'John Doe',
     'date': '2015-05-12T14:36:00.451765',
     'md5checksum': 'e8c83e232b64ce94fdd0e4539ad0d44f'
    },
    {'uid': '1',
     'name': 'John Doe',
     'date': '2015-05-12T15:36:00.451765',
     'md5checksum': 'e8c83e232b64ce94fdd0e4539ad0d44f'
    },
    {'uid': '2',
     'name': 'Jane Doe',
     'date': '2015-05-13T14:36:00.451765',
     'md5checksum': 'b419795d50db2a35e94c8364978d898f'
    },
    {'uid': '2',
     'name': 'Jane Doe',
     'date': '2015-05-14T14:36:00.451765',
     'md5checksum': 'b419795d50db2a35e94c8364978d898f'
    },
]
# Bad MD5
test_data_bad_md5 = [
    {'uid': '1',
     'name': 'John Doe',
     'date': '2015-05-14T14:36:00.451765',
     'md5checksum': 'e8c83e232b64ce94fdd0e4539ad0d44f'
    },
]

print "Clearing Database"
response = requests.get(base_url + '/clear_db')

print "Checking DB Empty:",
response = requests.get(base_url + '/output_db')
if response.json() == []:
    print "Pass"
else:
    print "Fail"

load_data(test_data_1)

check_counts({'uid': 1, 'date': '2015-05-12'}, 2)
check_counts({'uid': 1, 'date': '2015-05-13'}, 0)
check_counts({'uid': 1, 'date': '2015-05-14'}, 0)

check_counts({'uid': 2, 'date': '2015-05-12'}, 0)
check_counts({'uid': 2, 'date': '2015-05-13'}, 1)
check_counts({'uid': 2, 'date': '2015-05-14'}, 1)

print "Sending duplicate request to test duplicate detection"

load_data(test_data_1)

check_counts({'uid': 1, 'date': '2015-05-12'}, 2)
check_counts({'uid': 1, 'date': '2015-05-13'}, 0)
check_counts({'uid': 1, 'date': '2015-05-14'}, 0)

check_counts({'uid': 2, 'date': '2015-05-12'}, 0)
check_counts({'uid': 2, 'date': '2015-05-13'}, 1)
check_counts({'uid': 2, 'date': '2015-05-14'}, 1)
