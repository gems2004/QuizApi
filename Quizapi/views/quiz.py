from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework  import status
from bson import ObjectId
from Quizapi.serlaiizer import QuestionSerializer
from utils import client
# Create your views here.
db = client['QuizDb']
collection = db['QuizCollection']


class QuestionDetailView(APIView):
    def get(self, request, quiz_id):
        question = collection.find_one({'_id': ObjectId(quiz_id)})
        serializer = QuestionSerializer(data=question, many=False)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif serializer.errors:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, quiz_id):
        data = request.data
        quiz = {
            'category': data['category'],
            'difficulty': data['difficulty'],
            'question': data['question'],
            'correct_answer': data['correct_answer'],
            'answers': data['answers']
        }
        modified = collection.find_one_and_update({'_id': ObjectId(quiz_id)}, {'$set': quiz})
        serializer = QuestionSerializer(data=modified, many=False)
        if serializer.is_valid():
            return Response({'message': 'modified successfully'}, status=status.HTTP_200_OK)
        elif serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, quiz_id):
       quiz = collection.find_one_and_delete({'_id': ObjectId(quiz_id)})
       serializer = QuestionSerializer(data=quiz, many=False)
       print(quiz)
       if serializer.is_valid():
           return Response({'message': 'deleted successfully'}, status=status.HTTP_200_OK)
       elif serializer.errors:
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

