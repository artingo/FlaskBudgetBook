from bson import ObjectId


class DbBenutzer:
    """
       Diese Datei stellt CRUD-Operationen für die benutzer-Sammlung zur Verfügung

       Attribute
       ----------
        collection - die Benutzer-Sammlung in der DB

       Methoden
       -------
       create(vorname, nachname)
       read(id)
       update(id, vorname, nachname)
       delete(id)
    """

    def __init__(self, mongo):
        self.collection = mongo.db.benutzer
        print("Benutzer-Sammlung verbunden")

    def create(self, vorname: str, nachname: str) -> str:
        """
        Erzeugt einen neuen Benutzer
        :param vorname:
        :param nachname:
        :return:
        """
        result = self.collection.insert_one({
            "vorname": vorname,
            "nachname": nachname
        })
        return str(result.inserted_id)

    def read(self, benutzer_id: str):
        benutzer = self.collection.find_one({"_id": ObjectId(benutzer_id)})

        if benutzer:
            return benutzer

        print(f"Benutzer mit id {benutzer_id} nicht gefunden!")
        return None

    def update(self, benutzer_id: str, vorname: str, nachname: str) -> bool:
        result = self.collection.update_one(
            { "_id": ObjectId(benutzer_id)},
            {
                "$set": {
                    "vorname": vorname,
                    "nachname": nachname
                }
            })
        return result.acknowledged
