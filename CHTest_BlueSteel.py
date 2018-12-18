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

def getSearchId_1(alternateId, employerId, ssn):
  searchId = ""
  if (len(alternateId.strip()) > 0):
    searchId = alternateId
  elif (len(employerId.strip()) > 0):
    searchId = employerId
  else:
    searchId = ssn
  return searchId


def getSearchId_2(alternateId, employerId, ssn):
  searchId = ""
  if (len(alternateId.strip()) > 0):
    searchId = alternateId
  elif (len(ssn.strip()) > 0):
    searchId = ssn
  else:
    searchId = employerId
  return searchId


def check_batch_centrihealth_response( schema_file, request_file, big5_data_file ):
  results = ""
  schema = _load_json_schema(schema_file)
  results_validation_success = ""
  results_validation_failure = ""
  results_failure = ""
  results_validation_success_counter = 0
  results_validation_failure_counter = 0
  results_failure_counter = 0
  searchId = ""

  # BlueSteel Env 
  payload ='client_id=l7xxe1b9f59ceeb945baa38cf0d46848a1b2&client_secret=ad2748efd1364073a3311fce1e5ef499&grant_type=client_credentials' 
  r = requests.post('https://api-stg-perf.optum.com:8444/auth/oauth/v2/token', data=payload)
  # print (r.text)
  y = r.json()
  # print ( y['access_token'] )
  headers = {'Authorization':'bearer '+y['access_token'], 'Content-Type':'application/json'}
  
  
  with open(big5_data_file, 'r') as my_file:
    reader = csv.reader(my_file)
    my_list = list(reader)
  
  
  for i in range(0, len(my_list)):



    #print("********************************************************************")
    #print("index 0 last name:   " + my_list[i][0])
    #print("index 1 first name:  " + my_list[i][1])
    #print("index 2 dob:         " + my_list[i][2])
    #print("index 3 policyId:" + my_list[i][3])
    #print("index 4 Subscriber Id: " + my_list[i][4])
    #print("index 5 rallyId:     " + my_list[i][5])
    #print("********************************************************************")
  
    #searchId = getSearchId_2(my_list[i][0], my_list[i][6], my_list[i][7])
    
    searchId = my_list[i][4]
    #print("searchId : " + searchId)
 

    data = load_file_replace_keywords( request_file, my_list[i][1].strip(), my_list[i][0].strip(), my_list[i][2].strip(), searchId.strip(),  my_list[i][3].strip(), my_list[i][5].strip() )
    #print (data)

    # BlueSteel Env
    r2 = requests.post('https://api-stg-perf.optum.com:8444/api/perf/ihr/v1.0/read', headers=headers, data=data)

    #print("---------------------------------------------------------------------------------------------------------------------------------------------------------")
    #print (r2.text.encode('utf-8'))
    #print("---------------------------------------------------------------------------------------------------------------------------------------------------------")

    current_result = str(my_list[i]) 

    results = results + str(my_list[i]) 
    if ( r2.status_code != 200 ):
      results = results + " -> " + str(r2.status_code) + "\n"
      results_failure = results_failure + current_result + " -> " + str(r2.status_code) + "\n"
      results_failure_counter += 1
    else:
      json_data= json.loads( r2.text )
      results = results + " -> " + str(r2.status_code) + " Success\n"
      results_validation_success = results_validation_success + current_result + " -> " + str(r2.status_code) + " Success\n"
      results_validation_success_counter += 1

      #try: 
      #  if (validate(json_data, schema)==None):
      #    results = results + " -> " + str(r2.status_code) + " Schema Validation Success\n"
      #    results_validation_success = results_validation_success + current_result + " -> " + str(r2.status_code) + " Schema Validation Success\n"
      #    results_validation_success_counter += 1
      #  else:
      # 	  results = results + " -> " + str(r2.status_code) + " Schema Validation Failure\n"
      #    results_validation_failure = results_validation_failure + current_result + " -> " + str(r2.status_code) + " Schema Validation Failure\n"
      #    results_validation_failure_counter += 1
      #except:
      # 	    results = results + " -> Schema Error\n"
      #      results_validation_failure = results_validation_failure + current_result + " -> " + str(r2.status_code) + " Schema Validation Failure\n"
      #      results_validation_failure_counter += 1

  print("****************************************** Schema Validation Successful Requests *********************************************")
  print("*** Column Header: Last Name, First Name, Date of Birth, Policy Number, Subscriber ID, RallyId ***")
  print("")
  print(results_validation_success)
  print("Total Successful Requests: " + str(results_validation_success_counter))
  print("******************************************************************************************************************************")
  print("")
  print("")
  print("****************************************** Schema Validation Failure Requests *************************************************")
  print("*** Column Header: Last Name, First Name, Date of Birth, Policy Number, Subscriber ID, RallyId ***")
  print("")
  print(results_validation_failure)
  print("Total Failure Requests: " + str(results_validation_failure_counter))
  print("*******************************************************************************************************************************")
  print("")
  print("")
  print("****************************************** Other Error Requests ***************************************************************")
  print("*** Column Header: Last Name, First Name, Date of Birth, Policy Number, Subscriber ID, RallyId ***")
  print("")
  print(results_failure)
  print("Total Other Failure Requests: " + str(results_failure_counter))
  print("*******************************************************************************************************************************")
  print("")
  print("")
  print("Total Requests: " + str((results_validation_success_counter + results_validation_failure_counter + results_failure_counter)))
  results = results + "End"
  return results

Schema_file = 'CH_Response_Enum.json'
Request_file = 'General.json'
Big5_data_file = 'myList_BlueSteel.csv'
  
xbuf = check_batch_centrihealth_response( Schema_file, Request_file, Big5_data_file )
#print ( xbuf )
