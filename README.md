# pythonCodebase
PythonCodebase
Download Inventory_Module.zip so you have appropriate template setup
#Dependencies
This app is built using python flask frame work 
Below are the modules imported, please install any modules missing in your environment
 flask
 ipaddress
 csv
 json
 logging
 request
 jsonify
 render_template
#API 
This is a get api deployed using PythonAnywhere for validation and testing, attached
Swagger screenshots for testing
http://lakshmanpythonapps.pythonanywhere.com/addresses
Parameters to be passed:
addr - a valid ip address
mask - a valid mask in ip notation or cidr format
Output : Json/Json array
#UI
web application is deployed here
http://lakshmanpythonapps.pythonanywhere.com
accepts user inputs 
addr - a valid ip address
mask - a valid mask in ip notation or cidr format
output a simple html table

Possible enhancements:
Implement authentication with local/basic or LDAP based authentication
Implement ssl certificates for encryption
Add css styling for a better user experience on webui
Implement security framework to filter out malicious inputs
