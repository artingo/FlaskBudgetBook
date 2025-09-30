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
        :param vorname: der Vorname
        :param nachname: der Nachname
        :return: die neu erstellte benutzer_id
        """
        result = self.collection.insert_one({
            "vorname": vorname,
            "nachname": nachname
        })
        return str(result.inserted_id)

    def read(self, benutzer_id: str):
        """
        Liest einen Benutzer anhand seiner benutzer_id
        :param benutzer_id: die ID des gesuchten Benutzers
        :return: den gefundenen Benutzer oder 'None', falls keiner gefunden wurde
        """
        benutzer = self.collection.find_one({"_id": ObjectId(benutzer_id)})

        if benutzer:
            return benutzer

        print(f"Benutzer mit id {benutzer_id} nicht gefunden!")
        return None

    def read_all(self) -> list:
        """
        Liest alle Benutzer aus der Sammlung
        :return: benutzerListe
        """
        return self.collection.find()

    def update(self, benutzer_id: str, vorname: str, nachname: str) -> bool:
        """
        Aktualisiert einen Benutzer anhand seiner benutzer_id
        :param benutzer_id: die ID des zu aktualisierenden Benutzers
        :param vorname: der neue Vorname
        :param nachname: der neue Nachname
        :return: True, wenn das Update geklappt hat - False, falls nicht
        """
        result = self.collection.update_one(
            { "_id": ObjectId(benutzer_id)},
            {
                "$set": {
                    "vorname": vorname,
                    "nachname": nachname
                }
            })
        return result.acknowledged

    def delete(self, benutzer_id: str) -> bool:
        """
        Löscht einen Benutzer anhand seiner benutzer_id
        :param benutzer_id: die ID des zu löschenden Benutzers
        :return: True, wenn das Löschen geklappt hat - False, falls nicht
        """
        result = self.collection.delete_one({"_id": ObjectId(benutzer_id)})
        return result.deleted_count > 0

