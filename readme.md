# Infoblox Network Container and networks Creator

This is a Python script that creates new network container(/23) based on provided Extensible Attribute value and 3 networks(/24,/25 and /27) under this new network container


# Getting Started
# Prerequisites
- Python 3.x
- requests library

# Usage

python create_networks.py [state]

image.png

- The script takes a 2-letter state code as a positional argument. For example: "AR", "FL", "NY".

- This script will create a new /23 network container under the parent container with EA-State value of the provided state. 

- Then it would  create /24, /25, and /27 networks under the new /23 container.

# Configuration
Before running the script, you must set the following variables in the script:

- gm_url: URL of the Infoblox GM
- gm_user: Infoblox GM username
- gm_pwd: Infoblox GM password
  
# Example
To create new network containers and networks for the state of Arkansas:

image.png

# License
This project is licensed under the MIT License - see the LICENSE file for details.