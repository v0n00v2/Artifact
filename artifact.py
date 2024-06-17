from fastapi import FastAPI, HTTPException, Response, status, Depends
import requests
import json
from requests.auth import HTTPBasicAuth
from fastapi.params import Body
from typing import Optional
import re

print()
print()
print("#####################################Test Connection for Artifact#######################################")
print("########################################################################################################")

artifact_old_url = input("Enter Artifact component url : ")

if '#configuration' in artifact_old_url:
    artifact_url = artifact_old_url.replace("#configuration", ".json")
else :
    print("not find")


local_old_url = input("Enter local variable url, if not available then press enter: ") or "https://oneops.prod.walmart.com/boppa/assemblies/SGAv2-REST/transition/environments/498128035#variables"

if '#variables' in local_old_url:
    local_var = local_old_url.replace("#variables", "/variables.json")
else :
    print("not find")



global_old_url = input("enter global variable  url if not available then press enter : ") or "https://oneops.prod.walmart.com/boppa/assemblies/SGAv2-REST/transition/environments/498128035#variables"

if '#variables' in global_old_url:
    global_var = global_old_url.replace("#variables", "/variables.json")
    
else :
    print("not find")

basic = HTTPBasicAuth('username', 'Password')
headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
platform = requests.get(artifact_url, auth=basic, headers=headers)
platform_var_data = platform.json()
# # # Store the JSON data in a file
# with open("oneops_platform_data.json", "w") as file:
#      json.dump(artifact_json, file, indent=4)

# print("Data stored successfully! PLATFORM ")

# with open("oneops_platform_data.json") as file:
#    platform_var_data =  json.load(file)


a = platform_var_data['ciAttributes']['url']
b = platform_var_data['ciAttributes']['repository']
c = platform_var_data['ciAttributes']['version']
d = platform_var_data['ciAttributes']['location']


local_var_platform = requests.get(local_var,  auth=basic, headers=headers)
local_var_data = local_var_platform.json()
# with open("oneops_local_var.json", "w") as file:
#     json.dump(local_var_json, file, indent=4)

# print("Data stored  successfully for local !")

# with open("oneops_local_data.json") as file:
#     local_var_data =  json.load(file)


global_url = requests.get(global_var,  auth=basic, headers=headers)
global_var_data = global_url.json()
# # Store the JSON data in a file
# with open("oneops_global_data.json", "w") as file:
#     json.dump(global_var_json, file, indent=4)

# print("Data stored successfully! for global")

# with open("oneops_global_data.json") as file:
#     global_var_data =  json.load(file)

self_initial_data= []
local_initial_data=[]
global_initial_data=[]
cloud_initial_data=[]
hard_local_global = []
group_id_data= []


hard_local_global.append(a)
hard_local_global.append(b)
d.split(':')
for element in d.split(':'):
    group_id_data.append(element)
    hard_local_global.append(element)
# print(group_id_data)

# here we replace ".",":" with "/" and seprate file_extension
#Function to extract the element between curly braces
#location_list = []  
def extract_element(value):
    match = re.search(r'\$\w+\{([^}]+)\}', value)
    if match:
        return match.group(1)
    else:
        return "No match found"

hard_local_global.append(c)
#hard_local_global.append(file_extension)


for i  in range (len(hard_local_global)):
    if '$OO_LOCAL' in hard_local_global[i]:
        local_initial_data.append(hard_local_global[i])
    elif '$OO_GLOBAL'  in hard_local_global[i]:
        global_initial_data.append(hard_local_global[i])
    elif '$OO_CLOUD'  in hard_local_global[i]:
        cloud_variable = input("enter cloud variable  : ")
        cloud_initial_data.append(cloud_variable)
    else : 
        self_initial_data.append(hard_local_global[i])

# print("$OO_LOCAL : ", local_initial_data)
# print("$OO_GLOBAL : ", global_initial_data) 
# print("$OO_CLOUD: " , cloud_initial_data) 
# print("HardCode: " , self_initial_data)  
# print()
# print("All value extracted form hard,local,global,cloud  :",  hard_local_global)

modified_list = []

modified_list.append(self_initial_data)
# print(modified_list)

for curly in range(len(local_initial_data)):
    modified_list.append(extract_element(local_initial_data[curly]))
# print(local_target_keys)
# print(modified_list)

# global_target_keys = []
for curly in range(len(global_initial_data)):
    modified_list.append(extract_element(global_initial_data[curly]))
# print(modified_list)

for curly in range(len(cloud_initial_data)):
    modified_list.append(extract_element(cloud_initial_data[curly]))
# print(modified_list)

target_keys=[]
for i in modified_list:
    if type(i) is list:
        target_keys.extend(i)
    else:
        target_keys.append(i)
# print(target_keys)
    

# Function to search for a value in the Local JSON data
def search_value(local_data, target_key):
        for item in local_data:
            if target_key in item["ciName"]:
                return item["ciAttributes"]["value"]
        raise KeyError(f'Element with key {target_key} not found in the LOCAL')

    # Load JSON data
    # json_file_path = 'nested_data.json'
    # local_data = load_json(json_file_path)

local_data = local_var_data

# List of target keys to search for
# Search for each target key in the JSON data
    
local_result = {}
for target_key in target_keys:
        #print(f'Searching for {local_target_key} in Local variable.')
        try:
            value = search_value(local_data, target_key)
        except KeyError as e:
            e
        else:
            #print(f' {local_target_key} :  {value}')
            local_result[target_key] = value
        
    
# print("Final for local_variable results:", local_result)
print()
print()

#searching in global variable

def search_value(global_data , target_key):
        for item in global_data:
            if target_key in item["ciName"]:
                return item["ciAttributes"]["value"]
        raise KeyError(f'Element with key {target_key} not found in GLOBAL')

    # Load JSON data
    # json_file_path = 'nested_data.json'
    # global_data, = load_json(json_file_path)

global_data = global_var_data
# List of target keys to search for
# Search for each target key in the JSON data
global_result = {}
for target_key in target_keys:
        #print(f'Searching for {target_key} in GLOBAL')
        try:
            value = search_value(global_data, target_key)
        except KeyError as e:
            e
        else:
            #print(f' {target_key} :  {value}')
            global_result[target_key] = value
       
# print("Final for Global_variable results:", global_result)

final_local =  [target_keys  for target_keys in local_result.values()]

final_global =  [target_keys  for target_keys in global_result.values()]

# print(final_global)
# print(final_local)


#########  url_id  ##############

if '$OO_LOCAL'  in a:
    url = extract_element(a)
    if url in local_result:
            url_id = local_result[url]
elif '$OO_GLOBAL' in a:
    url = extract_element(a)
    if url in global_result:
        url_id = global_result[url]
else:
    sub_str = "com"
    # slicing off after length computation
    url_id = a[:a.index(sub_str) + len(sub_str)]        
# print(url_id)

#########  repository_id  ##############



if '$OO_LOCAL' in b:
    repo = extract_element(b)
    if repo in local_result:
        repository_id = local_result[repo]
elif '$OO_GLOBAL' in b:
    repo = extract_element(b)
    if repo in global_result:
        repository_id = global_result[repo]
else:
    repository_id = b

# print(repository_id)



#########  group_id ##############


if "$OO_" not in d:
    replaced_str = d.replace('.', '/')
    parts = replaced_str.split(':')
    group_id = '/'.join(parts[:-1])
    # print(group_id)
elif '$OO_LOCAL' in d:
    group_new_id = extract_element(group_id_data[0])
    modified_string = local_result[group_new_id]
    group_id = modified_string.replace('.', '/')
    # print(group_id)
elif '$OO_GLOBAL' in d:
    group_new_id = extract_element(group_id_data[0])
    modified_string = global_result[group_new_id]
    group_id = modified_string.replace('.', '/')
    # print(group_id)



#########  Artifact_id ##############

if "$OO_" not in d:
    replaced_str = d.replace('.', '/')
    parts = replaced_str.split(':')
    artifact_id = '/'.join(parts[:-1])
    # print(artifact_id)
    artifact_id = parts[1]
    # print(artifact_id)
elif '$OO_LOCAL' in d:
    group_new_id = extract_element(group_id_data[1])
    modified_string = local_result[group_new_id]
    artifact_id = modified_string.replace('.', '/')
    # print(artifact_id)
elif '$OO_GLOBAL' in d:
    group_new_id = extract_element(group_id_data[1])
    modified_string = global_result[group_new_id]
    artifact_id = modified_string.replace('.', '/')
    # print(artifact_id)
# #########  appversion_id ##############

if '$OO_LOCAL' in c:
    appversion = extract_element(c)
    appVersion_id = local_result[appversion]
    # print(appVersion_id)
elif '$OO_GLOBAL' in c:
    appversion = extract_element(c)
    appVersion_id = global_result[appversion]
    # print(appVersion_id)
else:
    appVersion_id = c
    # print(appVersion_id)

#########  extension_id ##############

if "$OO_" not in d:
    replaced_str = d.replace('.', '/')
    parts = replaced_str.split(':')
    group_id = '/'.join(parts[:-1])
    extension_id = parts[-1]
    # print(extension_id)
elif '$OO_LOCAL' in d:
    extension = extract_element(group_id_data[-1])
    extension_id = local_result[extension]
    # print(extension_id)
elif '$OO_GLOBAL' in group_id_data[-1]:
    extension = extract_element(group_id_data[-1])
    extension_id = global_result[extension]
    # print(extension_id)

print()
print('###################  Variable define at Artifact-Component and Value  #################################')
print()
if "$OO_" not in a:
    print ("Url :", a  )
else:
    print ("Url :", a , "====>>>>", url_id  )

print('---')


if "$OO_" not in b:
    print ("Repository :", b )
else:
    print ("Repository :", b , "====>>>>", repository_id  )

print('-----------')

if "$OO_" not in d:
    print("Location :", d  )

else:
    
    print ("Group_ID :", d , "====>>>>", group_id   )
    print('---------')
    print ("Artifact_ID :", d , "====>>>>", artifact_id   )
    print('---------')
    print ("Extension : ====>>>>", extension_id   )

print('----------')



if "$OO_" not in c:
    print("Version :", c )
else:
    print ("Version :", c , "====>>>>", appVersion_id  )

print('-------')


print('######################################################')
print('********************************************************************************************')
print()

if  'mvn' in url_id:
        if "$OO_" not in d:
            web_address = [f"{url_id}/artifactory/{repository_id}/{group_id}/{appVersion_id}/{artifact_id}-{appVersion_id}.{extension_id}"]
        else:           
            web_address = [f"{url_id}/artifactory/{repository_id}/{group_id}/{artifact_id}/{appVersion_id}/{artifact_id}-{appVersion_id}.{extension_id}"]
else :
    if "$OO_" not in d:
        web_address = [f"{url_id}/content/repositories/{repository_id}/{group_id}/{appVersion_id}/{artifact_id}-{appVersion_id}.{extension_id}"]
    else:
        web_address = [f"{url_id}/content/repositories/{repository_id}/{group_id}/{artifact_id}/{appVersion_id}/{artifact_id}-{appVersion_id}.{extension_id}"]
statuses = {
    200: "Artifact Available",
    301: "Permanent Redirect",
    302: "Temporary Redirect",
    404: "Not Found",
    500: "Internal Server Error",
    503: "Service Unavailable"
    }
    
for url in web_address:
    try:
        web_response = requests.get(url)
        print(url, "===>>>>", statuses[web_response.status_code])
    
    except:
        print(url, "===>>>", statuses[web_response.status_code])         


