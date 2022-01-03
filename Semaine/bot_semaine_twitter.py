import mysql.connector
import matplotlib.pyplot as plt
import time
import tweepy
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

#initialise variable
total=2
i = 6
dict1 = {}
table = []
table_fin = []
y = 0
#connection mysql
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="DBLucas0806)",
  database="Météo"
)
#take valeur
mycursor = mydb.cursor()
mycursor.execute("SELECT degré FROM historique")
myresult = mycursor.fetchall()

for x in myresult:
    print(x)
    total=total+1

print(total)

while i>=0:
  mycursor = mydb.cursor()
  mycursor.execute("SELECT `degré` FROM `historique` WHERE id='{}'".format(total-i))
  a = mycursor.fetchall()
  table.append(a)
  i=i-1
print(table)
#convertir valeur
def convert(a):
  for y in range(7):
    av1 = a[y]
    av2 = av1[0]
    av3 = av2[0]
    av4 = int(av3)
    table_fin.append(av4)
    print("table fin dans la fonction : ",table_fin)

convert(table)
jour = ["lundi", "Mardi", "Mercredi", "Jeudi","Vendredi","Samedi","Dimanche"]
print("tableau_fin : ", table_fin)

#graphique
plt.figure()
plt.plot(jour,table_fin)
plt.title('Récap Semaine')
plt.xlabel("Jour")
plt.ylabel("Température")
plt.savefig("courbe.png")

#envois la photo sur twitter
imgPath = "courbe.png"
message = "Voici le récap de la semaine"
api.update_with_media(imgPath,message)