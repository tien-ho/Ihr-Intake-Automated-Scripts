import json
import csv
import requests
from os.path import join, dirname
from jsonschema import validate



def assert_valid_schema(data, schema_file):
    """ Checks whether the given data matches the schema """

    schema = _load_json_schema(schema_file)
    return (validate(data, schema))


def _load_json_schema(filename):
    """ Loads the given schema file """

    #relative_path = join('schemas', filename)
    #absolute_path = join(dirname(__file__), relative_path)
    #print ( absolute_path )
    with open(filename) as schema_file:
        return json.loads(schema_file.read())


def		load_file_replace_keywords( fileName, first, last, dob, searchID, policy, rallyID ):
	with open(fileName, 'r') as myfile:
		dataFile = myfile.read()
  
	dataFile=dataFile.replace( '<*First>', first )
	dataFile=dataFile.replace( '<*Last>', last )
	dataFile=dataFile.replace( '<*Dob>', dob )
	dataFile=dataFile.replace( '<*SearchID>', searchID )
	dataFile=dataFile.replace( '<*Policy>', policy )
	dataFile=dataFile.replace( '<*RallyID>', rallyID )
	return dataFile  



def check_batch_centrihealth_response( schema_file, request_file, big5_data_file ):
  results = ""
  schema = _load_json_schema(schema_file)
  
  
  payload ='client_id=l7xx442741ed031249bc95f8d3766b64c91a&client_secret=3de1acb0bea54f77818b45322b6b0337&grant_type=client_credentials' 
  r = requests.post('https://api-stg.optum.com:8444/auth/oauth/v2/token', data=payload)
  # print (r.text)
  y = r.json()
  # print ( y['access_token'] )
  headers = {'Authorization':'bearer '+y['access_token'], 'Content-Type':'application/json'}
  
  
  with open(big5_data_file, 'r') as my_file:
    reader = csv.reader(my_file)
    my_list = list(reader)
  
  
  for i in range(0, len(my_list)):

    #print("index 2 first name:" + my_list[i][1])
    #print("index 3 last name:" + my_list[i][2])
    #print("index 4 dob:" + my_list[i][3])
    #print("index 1 searchId:" + my_list[i][0])
    #print("index 5 policyNumber:" + my_list[i][4])
    #print("index 6 rallyId:" + my_list[i][5])
    #print("********************************************************************")

    data = load_file_replace_keywords( request_file, my_list[i][1].strip(), my_list[i][2].strip(), my_list[i][3].strip(), my_list[i][0].strip(),  my_list[i][4].strip(), my_list[i][5].strip() )
    #print (data)
    r2 = requests.post('https://api-stg.optum.com:8444/api/perf/ihr/v1.0/read', headers=headers, data=data)
    #print ( r2.text )
    
    results = results + str(my_list[i]) 
    if ( r2.status_code != 200 ):
      results = results + " -> " + str(r2.status_code) + "\n"
    else:
      json_data= json.loads( r2.text )
      try: 
        if (validate(json_data, schema)==None):
          results = results + " -> " + str(r2.status_code) + " Schema Validation Success\n"
        else:
  	      results = results + " -> " + str(r2.status_code) + " Schema Validation Failure\n"
      except:
  	    results = results + " -> Schema Error\n"
  
  results = results + "End"
  return results

Schema_file = 'CH_Response_Enum.json'
Request_file = 'General.json'
Big5_data_file = 'myList.csv'
  
xbuf = check_batch_centrihealth_response( Schema_file, Request_file, Big5_data_file )
print ( xbuf )