from pymongo import MongoClient

from app.core.config import MONGO_URI

client = MongoClient(MONGO_URI)

db = client["chatpdf"]

users_collection = db["users"]

pdf_collection = db["pdfs"]

chat_collection = db["chats"]