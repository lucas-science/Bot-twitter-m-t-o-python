import tweepy
import requests
import json
import emojis
import mysql.connector
import json

# get TOKENS
f = open('config.json')
data = json.load(f)
f.close()

consumer_key = data["consumer_key"]
consumer_secret = data['consumer_secret']
access_token = data['access_token']
access_token_secret = data['access_token_secret']

#connexion API twitter 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Connexion mysql
"""
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="DBLucas0806)",
  database="Météo"
)
"""
#get l'API openweathermap
response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Fouchy&appid=22c5f232d2cfedf6d2f67e8f5d1b3c2b&lang=fr")
print(response.status_code)

#stock les emoji de l'API
emoji = {
    "01d":emojis.encode(":sunny:"),
    "02d":emojis.encode(":partly_sunny:"),
    "03d":emojis.encode(":cloud:"),
    "04d":emojis.encode(":cloud:"),
    "09d":emojis.encode(":cloud_rain:"),
    "10d":emojis.encode(":white_sun_rain_cloud:"),
    "11d":emojis.encode(":cloud_lightning:"),
    "13d":emojis.encode(":snowflake:"),
    "50d":emojis.encode(":fog:"),
    "01n":emojis.encode(":crescent_moon:"),
    "02n":emojis.encode(":white_sun_cloud:"),
    "03n":emojis.encode(":cloud:"),
    "04n":emojis.encode(":cloud:"),
    "09n":emojis.encode(":umbrella:"),
    "10n":emojis.encode(":white_sun_rain_cloud:"),
    "11n":emojis.encode(":zap:"),
    "13n":emojis.encode(":snowflake:"),
    "50n":emojis.encode(":fog:")
}

#montrer le Json
"""def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(response.json())"""

#initialiser les variable de température
temp_K = response.json()["main"]["temp"]
temp_C = round(temp_K-273.15)

#cherhcer info dans l'api (json)
response.json()["weather"][0]["icon"][0]
emoji_resp = response.json()["weather"][0]["icon"]
description = response.json()["weather"][0]["description"]

#choisir emoji pour la situation
if temp_C < 5:
    icon_temp = emojis.encode(":snowman:")
elif temp_C > 28:
    icon_temp = emojis.encode(":fire:")
else:
    icon_temp = emojis.encode(":smile:")
#expoter to mysql

mycursor = mydb.cursor()

sql = "INSERT INTO historique (degré) VALUES ({})".format(temp_C) 
mycursor.execute(sql)
mydb.commit()

print(mycursor.rowcount, "record inserted.")

#stoquer le texte
text = emojis.encode("La température actuel est de {}°C {} ".format(temp_C, icon_temp)+"\n"+ "Et le temps est {} {}".format(description, emoji[emoji_resp])+"\n"+"\n"+"Bonne journée")

#montrer le résultat
print(text)

#upload sur twitter
api.update_status(text)
