from unittest import TestCase
from flask import Flask
from backend.db import init_db
from backend.dbbenutzer import DbBenutzer


class Test(TestCase):
    def setUp(self):
        app = Flask(__name__)
        self.mongo = init_db(app)
        self.db = DbBenutzer(self.mongo)

    def tearDown(self):
        self.mongo.cx.close()

    def test_create(self):
        benutzer_id = self.db.create('Annette', 'Ganz')
        assert benutzer_id is not None
        self._id = benutzer_id
        print(f"Benutzer mit ID {str(benutzer_id)} angelegt")

    def test_read(self):
        if not hasattr(self, "_id"):
            self.test_create()
        benutzer = self.db.read(self._id)
        assert benutzer is not None
        print(f"User mit ID {str(self._id)} gelesen")
        print("Benutzer: ", benutzer)

    def test_update(self):
        self.test_read()
        self.db.update(self._id, "Brigitte", "Ganz")
        print(f"Vorname geändert auf 'Brigitte'")

    def test_delete(self):
        self.test_read()
        self.db.update(self._id, "Brigitte", "Ganz")
        print(f"Vorname geändert auf 'Brigitte'")
