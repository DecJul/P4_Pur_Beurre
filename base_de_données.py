import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="student",
    password="mot_de_passe",
    database="pur_beurre_P5")

MYCURSOR = mydb.cursor()

var = "sugar"

sql = "SELECT products.id, " \
              "products.product_name, " \
              "products._id, " \
              "products.nutriscore, " \
              "products.sugar, " \
              "products.salt, " \
              "products.fat, " \
              "products.energy " \
      "FROM substituts " \
      "INNER JOIN products " \
      "ON substituts.id_product = products._id " \
      "WHERE substituts."+var+" = 1 " \
      "ORDER BY substituts.searchscore"
MYCURSOR.execute(sql)
myresult = MYCURSOR.fetchone()
print(myresult[0])
