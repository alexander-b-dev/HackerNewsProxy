import unittest
from main import create_app
import config


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app = create_app()
        cls.client = app.test_client()
        cls.userName = "ZLMUIHN8RYQTBLN"
        cls.pwd = "1234567890"

    def test_Get(self):
        data = self.client.get("/")
        self.assertEqual(200, data.status_code)
        self.assertEqual(True, ("Hacker&#8482;" in data.text))

    def test_Post(self):
        data = self.client.post("/login", data={"acct": self.userName, "pw": self.pwd})
        self.assertEqual(200, data.status_code)
        cookie = self.client.get_cookie("user")
        self.assertIsNotNone(cookie)
        data = self.client.get("/")
        self.assertEqual(True, (self.userName in data.text))

    def test_NotAllowedMethod(self):
        data = self.client.put("/")
        self.assertEqual(405, data.status_code)

    def test_Timeout(self):
        config.reqTimeout = 0.01
        data = self.client.get("/")
        self.assertEqual(504, data.status_code)
        config.reqTimeout = 2

    def test_NonExisting(self):
        data = self.client.get("/ololo")
        self.assertEqual(404, data.status_code)
        self.assertEqual("Unknown.",  data.text)

    def test_WrongCredentials(self):
        data = self.client.post("/login", data={"acct": self.userName, "pw": "ololo"})
        self.assertEqual(200, data.status_code)


if __name__ == '__main__':
    unittest.main()
