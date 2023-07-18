import os
import requests
import dotenv

dotenv.load("C:/users/alex-/PycharmProjects/blogs_api/server.env")

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

ADDRESS = "http://" + str(HOST) + ":" + str(PORT) + "/"

def test_hello():
    response = requests.get(ADDRESS)
    assert response.status_code == 200