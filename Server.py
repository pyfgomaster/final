from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

temp = 0
moist = 0
auto_state = False
aircon_state = False
dehumid_state = False
light_state = False

@app.route('/latest', methods=['GET', 'POST'])
def latest():
    if request.method == 'POST':
        post_data = request.get_json()
            
        if not post_data:
            return jsonify({"status": 1, "message": "Missing JSON body!"}), 400
            
        global temp, moist
        temp = post_data['temp']
        moist = post_data['moist']
        print(f"temp: {temp}, moist: {moist}")
        return jsonify({"status": 0, "message": "Success!"})

    elif request.method == 'GET':
        return jsonify({"temp": temp, "moist": moist})

@app.route('/ledAuto')
def ledAuto():
    global auto_state
    auto_state = not auto_state
    return jsonify({"status": 0, "message": "Success!"})

@app.route('/airconSwitch')
def airconSwitch():
    global aircon_state
    aircon_state = not aircon_state
    return jsonify({"status": 0, "message": "Success!"})
  
@app.route('/dehumidSwitch')
def dehumidSwitch():
    global dehumid_state
    dehumid_state = not dehumid_state
    return jsonify({"status": 0, "message": "Success!"})
  
@app.route('/lightSwitch')
def lightSwitch():
    global light_state
    light_state = not light_state
    return jsonify({"status": 0, "message": "Success!"})
  
@app.route('/isOn')
def isOn():
    return jsonify({"aircon": aircon_state, "dehumid": dehumid_state, "light": light_state})

@app.route('/isAuto')
def isAuto():
    return jsonify({"state": auto_state})

if __name__ == '__main__':
    app.run(port=30006)
