"""
Script to create new network containers and networks in Infoblox Grid Manager (GM). 

Usage: python create_networks.py [state]

positional arguments:
state                 2-letter state code for the new network container. Example: "AR", "KS", "MI", "MO"

This script will create a new /23 network container under the parent container with EA-SNOWAutomation value of the provided state. 
It will then create /24, /25, and /27 networks under the new /23 container. 

"""

import requests
import json
import re
import argparse


requests.packages.urllib3.disable_warnings()


# Grid Variables
gm_url = "https://1.1.1.1/wapi/v2.7"
gm_user = 'fars'
gm_pwd = 'infoblox'


# List of state codes for the new network container
state_ea_values = ['AR', 'AZ', 'CA', 'CO', 'HI', 'ID', 'KS', 'MI', 'MO', 'MT', 'NM', 'NV', 'OH', 'OR', 'TX', 'UT', 'WA']


# Setting up a session with the Infoblox GM
s = requests.Session()
s.auth = (gm_user, gm_pwd)
s.verify = False
headers = {"content-type": "application/json"}


# initialize parser and set up Extensible attribute as argument for calling the script from CLI
parser = argparse.ArgumentParser(description="List of State Extensible Attribute values.")
parser.add_argument("ea", type=str, choices=state_ea_values, help="Please enter state value in short hand. Example: AR, KS, MI, MO")
args = parser.parse_args()
state = args.ea.upper()


def network_container_23():
    """Function to query available network under the container and create it as a new network container"""


    # Querying available network is based on the user provided state attribute value
    
    # STEP 1 Get the reference of the network container which has user provided EA-State Value
    
    container_23 = s.get(f'{gm_url}/networkcontainer?_return_fields=extattrs&*SNOW={state}', headers=headers)
    d = container_23.json()
    ref_container = d[0]['_ref']
    

    # STEP 2 Query next available network under the above network container
    payload = dict(cidr=23)
    url = f"{gm_url}/{ref_container}?_function=next_available_network"
    response = s.post(url, headers=headers, data=json.dumps(payload))
    d = response.json()
    new_container = d['networks'][0]
   

    # Create the above network as network container and capture reference
    payload = dict(network=new_container)
    url = f"{gm_url}/networkcontainer"
    response = s.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code != 201:
        raise Exception(f"Error creating network container. Response status code: {response.status_code}")
    
    ref_new_container = response.json().strip()
    ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', ref_new_container)
    print(f'Network container "{ip[0]}/23" is created')
    return ref_new_container


def create_networks(ref_new_container, x):
    """Function to create /24, /25 and /27 networks under new network container"""


    # Query available 3 networks under this newly created network container
    # Here we use "x" as a parameter to query /24, /25 and /27 networks


    cidr = dict(cidr=x)
    response = s.post(f'{gm_url}/{ref_new_container}?_function=next_available_network', headers=headers, data=json.dumps(cidr))
    d1 = response.json()
    new_network = d1['networks'][0]


    # create /24 , /25 and /27 networks
    payload = dict(network=new_network)
    response = s.post(f'{gm_url}/network', headers=headers, data=json.dumps(payload))
    r = response.json()
    ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', r)
    print(f'Network "{ip[0]}/{x}" is created')

    if 'Error' in r:
        raise Exception(f"An error occurred while creating network: {r}")

print(" ")
ref_new_container = network_container_23() # Create /23 new network container
print(" ")


# Create /24, /25 and 27  networks under above /23 container
create_networks(ref_new_container, 24)
create_networks(ref_new_container, 25)
create_networks(ref_new_container, 27)


