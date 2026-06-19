from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URL"))

db = client["student_management"]

users_collection = db["users"]
students_collection = db["students"]