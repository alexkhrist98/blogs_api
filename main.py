import logging
import uvicorn
import dotenv
import dotenv
import os

dotenv.load("server.env")
HOST:str = os.getenv("HOST")
PORT = os.getenv("PORT")
PORT = int(PORT)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s: %(levelname)s - %(pathname)s:%(lineno)d - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

if __name__ == "__main__":
    uvicorn.run("app.app:app", host=HOST, port=PORT,
                reload=False)
