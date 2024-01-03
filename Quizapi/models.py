from mongoengine import Document, StringField, ListField, ObjectIdField
import random

class Quiz(Document):
    category = StringField()
    difficulty = StringField()
    question = StringField()
    correct_answer = StringField()
    answers = ListField(StringField())

