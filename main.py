import sqlite3
import requests
from Alerte import *


# Create a connection to the database
conn = sqlite3.connect("mydatabase.db")
# Create a cursor object to execute SQL commands
cursor = conn.cursor()


#cle pour ce connecter a l'API CoinAPI et recuperer les données (deux clé differentes au cas ou utilise tou sles tokesn possibles pour une suele clé)

API_KEY = "6D73B1B4-97EA-48D6-BF7C-98805B4DAB3A"
# API_KEY = 'C7BA6749-F83B-4BB0-80F6-2D3C596FE7DA'




#fonction pour creer des alertes
def creerAlerte():
    # endpoint url pour les assets
    url = 'https://rest.coinapi.io/v1/assets/BTC'

    #rajouter clé API
    headers = {'X-CoinAPI-Key': API_KEY}

    #commande egt pour recuperer les données
    response = requests.get(url, headers=headers)

    #verifier si on recoit une repsonse
    #print(response.status_code)


    #transfromer le json obtenu et le transforme en objet python
    data = response.json()
    ligne = data[0]
    name = ligne['name']
    value = ligne['price_usd']

    #verifier la structure de données de la data
    #print(type(response.json()))
    #print(data[0])


    #fonction pour verfifer si on a besoin de creer une alerte et la crée dans ce cas
    def checkPrice(price, name):
        alerte = None
        type = None
        if price > 7000:
            type = "Price over 7000"
            alerte = Alerte(name, price, type)


        if price < 5000:
            type = "Price under 5000"
            alerte = Alerte(name, price, type)
            # listAlertes.append(alerte)

        return alerte

    #parametres pour ajouter les données de l'alerte crée dans la base de donéées
    nameAlert = checkPrice(value, name).name
    priceAlert = str(checkPrice(value, name).price)
    typeAlert = checkPrice(value, name).type

    # Creaer la table dans la base de données qui contienne les alertes
    cursor.execute(f"CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price TEXT, type TEXT)")

    # Inserer les données recuérées
    cursor.execute(f"INSERT INTO test(name, price, type) VALUES ('{nameAlert}', '{priceAlert}','{typeAlert}')")


    # Commit les changemment dans la base de données
    conn.commit()




#fonction pour afficher les alertes
def afficherAlertes():
    # recuperer la table
    cursor.execute("SELECT * FROM test")
    rows = cursor.fetchall()

    # En tête de la table
    headers = ["ID", "Name", "Price","Message"]

    # longueur de chaque cellule
    max_widths = [max(len(header), max(len(str(row[i])) for row in rows)) for i, header in enumerate(headers)]

    # afficher en têtes
    table = " | ".join(header.ljust(max_widths[i]) for i, header in enumerate(headers))
    print(table)

    # afficher separation en tête
    separator = "-+-".join("-" * width for width in max_widths)
    print(separator)

    # afficher données de la table
    for row in rows:
        table_row = " | ".join(str(value).ljust(max_widths[i]) for i, value in enumerate(row))
        print(table_row)







#fonction pour supprimer une alerte
def supprimerAlerte(id):
    # Effacer une ligne de la table(alerte) a partir de son id
    id = 2
    cursor.execute("DELETE FROM test WHERE id = ?", (id,))

    # Commit the changes
    conn.commit()



creerAlerte()
afficherAlertes()
#supprimerAlerte(2)




# Close the database connection
conn.close()
