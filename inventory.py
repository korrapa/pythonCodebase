import flask, ipaddress, csv, json, logging
from flask import request, jsonify, render_template

app = flask.Flask(__name__)
app.config["DEBUG"] = True
#logging for local execution
FORMAT = "[%(levelname)s:%(filename)s:%(lineno)s:%(asctime)s:%(funcName)s()] %(message)s"
logging.basicConfig(filename='inventory.log', format=FORMAT, level=logging.DEBUG)
def buildResponse(addr, mask):
    error = {}
    apiResponse = []
    inputvar = addr + "/" + mask
    # Create an empty list for our results
    ipResults = []
    #get matching ipaddresses
    try:
     ipResults = [str(ip) for ip in ipaddress.IPv4Network(inputvar)]
    except:
     error['Error'] = "Invalid Input Parameters"
     logging.error('Invalid Input Parameters')
     return error
    #read source file
    try:
     csv_file = csv.reader(open('inventory.csv', "r"), delimiter=",")
    except:
     error['Error'] = "Cannot access csv file inventory.csv"
     logging.error('Cannot access csv file inventory.csv')
     return error
    #ignore header records
    next(csv_file)
    #loop through to prepare matching response
    for ipRecords in csv_file:
        for ipadd in ipResults:
            if ipadd == ipRecords[2]:
                  matchList = {}
                  matchList['id'] = ipRecords[0]
                  matchList['object_name'] = ipRecords[1]
                  matchList['address'] = ipRecords[2]
                  matchList['owner'] = ipRecords[5]
                  apiResponse.append(matchList)
    if len(apiResponse) == 0:
       apiResponse = {}
       apiResponse['Empty'] = "no match"
    #convert response to json
    apiResponse = json.dumps(apiResponse, sort_keys=True, indent=4)
    apiResponse = json.loads(apiResponse)
    return apiResponse
#adding this additional route to redirect
@app.route('/',methods = ['GET','POST'])
@app.route('/report',methods = ['GET','POST'])
def inputParameters():
    error = {}
    #to get input parameters
    if request.method == 'GET':
       try:
         return render_template("request.html")
       except:
         error['Error'] = "render_template failed: request.html"
         logging.error('render_template failed: request.html')
         return error
    #now process to report
    if request.method == 'POST':
       addr = request.form.get('addr')
       mask = request.form.get('mask')
       if addr == '' or mask == '':
         error['Error'] = "Input parameters cannot be empty"
         logging.error('Input parameters cannot be empty')
         try:
           return render_template("error.html",result = error)
         except:
           error['Error'] = "render_template failed: error.html"
           logging.error('render_template failed: error.html')
           return error
       try:
         apiResponse = buildResponse(addr, mask)
       except:
         error['Error'] = "Error in calling function: buildResponse "
         logging.error('Error in calling function: buildResponse')
         return error
       if 'Error' in apiResponse or 'Empty' in apiResponse:
          try:
            return render_template("error.html",result = apiResponse)
          except:
            error['Error'] = "render_template failed: error.html"
            logging.error('render_template failed: error.html')
            return error
       else:
          try:
            return render_template("result.html",result = apiResponse)
          except:
            error['Error'] = "render_template failed: result.html"
            logging.error('render_template failed: result.html')
            return error
@app.route('/addresses', methods=['GET'])
def api_ip():
    error = {}
    #input attributes should not be empty!
    if 'addr' in request.args:
        addr = str(request.args['addr'])
    else:
        error['Error'] = "No addr attribute provided. Please specify an addr."
        logging.error('No addr attribute provided. Please specify an addr.')
        return error
    if 'mask' in request.args:
        mask = str(request.args['mask'])
    else:
        error['Error'] = "No mask attribute provided. Please specify a mask"
        logging.error('No mask attribute provided. Please specify a mask')
        return error
    try:
     apiResponse = buildResponse(addr, mask)
    except:
     error['Error'] = "Error in calling function: buildResponse "
     logging.error('Error in calling function: buildResponse')
     return error
    return jsonify(apiResponse)
app.run()