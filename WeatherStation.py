#!/usr/bin/env python
import time
import csv
import bme280
import RPi.GPIO as GPIO
import smbus2
from sklearn.neural_network import MLPClassifier
import joblib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import BlynkLib

# BME280 sensor address (default address)
address = 0x76

# Initialize I2C bus
bus = smbus2.SMBus(1)

# Load calibration parameters
calibration_params = bme280.load_calibration_params(bus, address)

# Set up GPIO for rain sensor
GPIO.setmode(GPIO.BOARD)
RAIN_SENSOR_PIN = 11
GPIO.setup(RAIN_SENSOR_PIN, GPIO.IN)

# Initialize Blynk
blynk = BlynkLib.Blynk('<auth string>', server='sgp1.blynk.cloud')

# Function to read rain sensor status
def read_rain_sensor():
    return int(not GPIO.input(RAIN_SENSOR_PIN))

# Function to read data from BME280 sensor
def read_bme280_data():
    data = bme280.sample(bus, address, calibration_params)
    temperature = data.temperature
    pressure = data.pressure
    humidity = data.humidity
    return humidity, pressure, temperature

# Send mail
def send_mail_to(receiver_email, subject, body):
    try:
     for i in range(len(receiver_email)):
        #create message
        message = MIMEMultipart()
        message["From"] = "quochuy0615@gmail.com"
        message["To"] = receiver_email[i]
        message["Subject"] = 'About: ' + subject
        message.attach(MIMEText(body, "plain"))
    
        #connect tot SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(message["From"], "<app pass>")
            server.sendmail(message["From"], message["To"], message.as_string())
    except:
     time.sleep(5)
     send_mail_to(receiver_email, subject, body)

# Main function to collect data and write to CSV
def main():
    fname = 'weather_data_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.csv'
    with open(fname, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Date", "MinTemp", "MaxTemp", "Humidity9am", "Humidity3pm", "Pressure9am", "Pressure3pm", "Temp9am", "Temp3pm", "RainToday", "RainTomorrow"])	#Header
        
        prev_day = time.localtime().tm_mday
        current_day = prev_day
        rain_today = 0
        rs_prev = 0
        max_temp = 0
        min_temp = 100
        am = 0
        pm = 0
        yesterday_data = []
        model = joblib.load('rain_predict_model.joblib')
        blynk.run()
        while True:
           try:
            # Update time
            current_time = time.localtime()
            current_day = current_time.tm_mday

            # Read data
            h, p, t = read_bme280_data()

            # Get data
            if current_time.tm_hour == 9 and am == 0:
                humidity9am, pressure9am, temp9am, am = h, p, t, 1
            if current_time.tm_hour == 15 and pm == 0:
                humidity3pm, pressure3pm, temp3pm, pm = h, p, t, 1
            if read_rain_sensor() == 1 and rs_prev==0:
                rain_today = 1
                send_mail_to(subscribers, "Raining", time.strftime("%H:%M %d/%m/%Y", current_time) + "\t-\tIt is raining here")
            rs_prev = read_rain_sensor()
            if t < min_temp:
                min_temp = t
            if t > max_temp:
                max_temp = t
            
            # Update Blynk
            try:
             blynk.virtual_write(0, t)
             blynk.virtual_write(1, p)
             blynk.virtual_write(2, h)
             blynk.virtual_write(3, rs_prev)
            except:
             pass
       
            # When change day
            if current_day != prev_day:
                # Collect data
                if len(yesterday_data) == 11:
                    yesterday_data.append(rain_today)
                    csvwriter.writerow(yesterday_data)
                if am==1 and pm==1:
                    yesterday_data = [time.strftime("%m/%d", current_time), min_temp, max_temp, humidity9am, humidity3pm, pressure9am, pressure3pm, temp9am, temp3pm, rain_today]
                
                # Predict
                if model.predict([[min_temp, max_temp, humidity9am, humidity3pm, pressure9am, pressure3pm, temp9am, temp3pm, rain_today]])[0] == 1:
                    send_mail_to(subscribers, "Today rain prediction", time.strftime("%d/%m/%Y", current_time) + "\t-\tToday will rain")
                else:
                    send_mail_to(subscribers, "Today rain prediction", time.strftime("%d/%m/%Y", current_time) + "\t-\tToday will NOT rain")
                
                prev_day = current_day
                rain_today = 0
                am = 0
                pm = 0
                max_temp = 0
                min_temp = 100
                rs_prev = 0

            # Wait for 1 s before collecting next data
            t = time.time()
            while True:
                try:
                 blynk.run()
                except:
                 try:
                  blynk.connect();
                 except:
                  pass
                if time.time() - t >= 1:
                    break
           except:
            with open('var.txt', 'w') as f:
             try:
              f.write('min_temp={}\n'.format(min_temp))
             except:
              pass
             try:
              f.write('max_temp={}\n'.format(max_temp))
             except:
              pass
             try:
              f.write('humidity9am={}\n'.format(humidity9am))
             except:
              pass
             try:
              f.write('humidity3pm={}\n'.format(humidity3pm))
             except:
              pass
             try:
              f.write('pressure9am={}\n'.format(pressure9am))
             except:
              pass
             try:
              f.write('pressure3pm={}\n'.format(pressure3pm))
             except:
              pass
             try:
              f.write('temp9am={}\n'.format(temp9am))
             except:
              pass
             try:
              f.write('temp3pm={}\n'.format(temp3pm))
             except:
              pass
             f.write('rain_today={}\n'.format(rain_today))

if __name__ == "__main__":
    if(len(sys.argv)<2):
        input('Usage: WeatherStation.py subscriber1 subscriber2 ...\n\nAre you sure to run without any subscribers? There will be no one know the result except \"Huy\".\n\nEnter any key to continue without any subscribers...')
    subscribers = sys.argv[1:]
    subscribers.append("quochuy0615@gmail.com")
    main()
