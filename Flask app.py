from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello_world():
	return "Hello Friend!"

@app.route('/bye')
def bye_world():
	return "Good Bye Friend!"	

# by default functions have GET, but if we write POST default is overrided
@app.route('/add', methods=["POST", "GET"])
def add_numbers():
	dataDict = request.get_json()

	if "y" not in dataDict:
		return "ERROR", 400
	
	x = dataDict["x"]
	y = dataDict["y"]
	z = x + y

	retJSON = {
		"z" : z
	}

	return retJSON, 200

if __name__ == "__main__":
	app.run(debug=True)
