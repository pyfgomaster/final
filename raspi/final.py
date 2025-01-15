import adafruit_dht
import requests, time, board
import RPi.GPIO as GPIO
import time
import tflite_runtime.interpreter as tflite
from tools import CustomVideoCapture, preprocess, parse_output
interpreter = tflite.Interpreter(model_path="model_unquant.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

with open("labels.txt", 'r') as f:
    labels = [line.strip().split()[1] for line in f.readlines()]
# Video Capture
LED_T = 18
LED = 15
LED_H = 14
BUZZ_PIN = 23
t_on = False
h_on = False
GPIO.setup(LED_T, GPIO.OUT)
GPIO.setup(LED_H, GPIO.OUT)
GPIO.setup(BUZZ_PIN, GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)
pwm = GPIO.PWM(LED, 100)
dht = adafruit_dht.DHT22(board.D17, use_pulseio=False)
buzz = GPIO.PWM(BUZZ_PIN, 262)
#vid = CustomVideoCapture()
#vid.set_title('Human Detection') 
pwm.start(0)
buzz.start(0)
#vid.start_stream()

while True:

    ledSwitch = requests.get("http://140.138.150.20/G6_api/isOn")
    ledSwitch = ledSwitch.json()
    # print(ledSwitch["aircon"])
    # print(ledSwitch["dehumid"])
    # print(ledSwitch["light"])
    ledAuto = requests.get("http://140.138.150.20/G6_api/isAuto")
    ledAuto = ledAuto.json()
    #print(ledAuto["state"])
    try:
        # Print the values to the serial port
        t = dht.temperature
        h = dht.humidity
    except RuntimeError as error:
        print(error.args[0])
    # t = 20
    # h = 80
    if ledAuto["state"] == False:
        if ledSwitch["aircon"]:
            t_on = True
            GPIO.output(LED_T, GPIO.HIGH)
        else:
            t_on = False
            GPIO.output(LED_T, GPIO.LOW)
        if ledSwitch["dehumid"]:
            h_on = True
            GPIO.output(LED_H, GPIO.HIGH)
        else:
            h_on = False
            GPIO.output(LED_H, GPIO.LOW)
        if ledSwitch["light"]:
            pwm.ChangeDutyCycle(50)
        else:
            pwm.ChangeDutyCycle(0)
    else:
        print("{}C, {}%".format(t, h))
        if t>20:
            GPIO.output(LED_T, GPIO.HIGH)
            t_on = True
        else:
            GPIO.output(LED_T, GPIO.LOW)
            t_on = False
        if h>80:
            GPIO.output(LED_H, GPIO.HIGH)
            h_on = True
        else:
            GPIO.output(LED_H, GPIO.LOW)
            h_on = False
        #if trg_class == "nobody":
            #pwm.ChangeDutyCycle(0)
        #elif trg_class == "person":
            #pwm.ChangeDutyCycle(50)
        #else:
            #pwm.ChangeDutyCycle(25)

    if t_on and h_on:
        buzz.ChangeDutyCycle(50)
    else:
        buzz.ChangeDutyCycle(0)

    #print(trg_class)
    #vid.info = '{}'.format(trg_class)
    post_data = {"temp": t, "moist": h}
    res = requests.post("http://140.138.150.20/G6_api/latest", json=post_data)
    time.sleep(0.2)

time.sleep(1)
print('-' * 30)
print(f'影像串流的線程是否已關閉 : {not vid.t.is_alive()}')
print('離開程式')

# not vid.isStop:
#     ret, frame = vid.get_current_frame()
#     if not ret:
#         continue
#     # Preprocess the image for the TensorFlow Lite model
#     data = preprocess(frame, resize=(224, 224), norm=True)
#     # Set the tensor
#     interpreter.set_tensor(input_details[0]['index'], data)
#     # Run inference
#     interpreter.invoke()
#     # Get the prediction result
#     prediction = interpreter.get_tensor(output_details[0]['index'])[0]
#     # Parse the recognition result
#     trg_id, trg_class, trg_prob = parse_output(prediction, labels)
