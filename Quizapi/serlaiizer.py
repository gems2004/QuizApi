from mongoengine import ListField
import random
from rest_framework_mongoengine.fields import ObjectIdField
from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Quiz


class QuestionSerializer(DocumentSerializer):
    _id = ObjectIdField(required=False)
    answers = ListField()

    class Meta:
        model = Quiz
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        randomized_answers = list(ret['answers'])
        random.shuffle(randomized_answers)
        ret['answers'] = randomized_answers
        return ret
