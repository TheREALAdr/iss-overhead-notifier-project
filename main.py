# ---------------------- IMPORTS ---------------------- #

import smtplib
import requests
from datetime import datetime
import time

# ---------------------- CONSTANTS -------------------- #

# PERSONAL LOCATION CONSTANTS
MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude

# EMAIL CONSTANTS
sending_gmail_address = "obviouslyafakeemailbroski@gmail.com"
sending_gmail_app_password = "vqtlvqzpnjhufmto"
yahoo_testing_acc = "testing_468@yahoo.com"

# DATETIME CONSTANTS
time_now = datetime.now()
hour_now = time_now.hour

# ---------- REQUEST/CONSTANTS FOR ISS POSITION API ------------ #

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

# -------------- REQUEST/CONSTANTS FOR SUNRISE-SUNSET API --------------- #

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])


# ----------------------- CHECK ISS POSITION/TIME & SEND EMAIL ---------------------- #


def check_for_iss():
    latitude_distance_difference = abs(iss_latitude - MY_LAT)
    longitude_distance_difference = abs(iss_longitude - MY_LONG)
    while latitude_distance_difference <= 5 and longitude_distance_difference <= 5:
        if sunset < hour_now < sunrise:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=sending_gmail_address, password=sending_gmail_app_password)
                connection.sendmail(from_addr=sending_gmail_address,
                                    to_addrs=yahoo_testing_acc,
                                    msg=f"Subject:Look up!\n\nThe ISS is overhead in your location."
                                    )
                time.sleep(60)


# -------------------- SENDING THE EMAIL -------------------- #

# BONUS: run the code every 60 seconds.
check_for_iss()
# While loop or detection method to make the count stop once the ISS disappears?



