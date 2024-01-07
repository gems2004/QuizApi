from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework  import status
from bson import ObjectId
from Quizapi.serlaiizer import QuestionSerializer
from utils import client
# Create your views here.
db = client['QuizDb']
collection = db['QuizCollection']


class QuizAPIView(APIView):
    def get(self, request):
        category = request.query_params.get('category')
        limit = request.query_params.get('limit')
        difficulty = request.query_params.get('difficulty')
        new_category_str = category.replace("-", " ")
        category_list = new_category_str.split()
        print(category_list)
        if new_category_str and difficulty and limit:
            pipeline = [ {'$match':{'difficulty': difficulty, 'category': {'$in': category_list}}},{'$sample': {'size': int(limit)}}]
            questions = list(collection.aggregate(pipeline))
            serializer = QuestionSerializer(data=questions, many=True)
            if serializer.is_valid():
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_404_NOT_FOUND)
        if difficulty and limit:
            pipeline = [ {'$match':{'difficulty': difficulty}},{'$sample': {'size': int(limit)}}]
            questions = list(collection.aggregate(pipeline))
            serializer = QuestionSerializer(data=questions, many=True)
            if serializer.is_valid():
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_404_NOT_FOUND)
        if new_category_str and limit:
            pipeline = [ {'$match':{'category': {'$in': category_list}}},{'$sample': {'size': int(limit)}}]
            questions = list(collection.aggregate(pipeline))
            serializer = QuestionSerializer(data=questions, many=True)
            if serializer.is_valid():
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_404_NOT_FOUND)
        if new_category_str and difficulty:
            questions = list(collection.find({'category': {'$in': category_list}, 'difficulty': difficulty}))
            serializer = QuestionSerializer(data=questions, many=True)
            if serializer.is_valid():
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_404_NOT_FOUND)
        if new_category_str:
            questions = list(collection.find({'category': {'$in': category_list}}))
            serializer = QuestionSerializer(data=questions, many=True)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

        if limit:
            pipeline = [{'$sample': {'size': int(limit)}}]
            random_documents = list(collection.aggregate(pipeline))
            serializer = QuestionSerializer(data=random_documents, many=True)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if difficulty:
            if difficulty == 'easy' or difficulty == 'medium' or difficulty == 'hard':
                questions = list(collection.find({'difficulty': str(difficulty)}))
                serializer = QuestionSerializer(data=questions, many=True)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message': 'bad request 400'}, status=status.HTTP_400_BAD_REQUEST)
        

        questions = list(collection.find())
        serializer = QuestionSerializer(data=questions, many=True)
        if serializer.is_valid():
            return Response({'quiz_list': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request):
        bulk_request = request.query_params.get('bulk_request')
        data = request.data
        if str(bulk_request) == 'true':
            bulk_quiz = []
            for quiz_data in data:
                
                quiz = {
                    'category': quiz_data['category'],
                    'difficulty': quiz_data['difficulty'],
                    'question': quiz_data['question'],
                    'correct_answer': quiz_data['correct_answer'],
                    'answers': quiz_data['answers']
                }
                bulk_quiz.append(quiz)
            serializer = QuestionSerializer(data=bulk_quiz, many=True)
            if serializer.is_valid():
                insert_bulk = collection.insert_many(bulk_quiz)
                return Response({'message': 'success', 'quiz_ids': [str(id) for id in insert_bulk.inserted_ids]}, status.HTTP_200_OK)
            else:
                return Response({'message': serializer.errors}, status.HTTP_400_BAD_REQUEST)
        quiz = {
            'category': data['category'],
            'difficulty': data['difficulty'],
            'question': data['question'],
            'correct_answer': data['correct_answer'],
            'answers': data['answers']
        }        
        serializer = QuestionSerializer(data=quiz, many=False)
        if serializer.is_valid():
            insert_col = collection.insert_one(quiz)
            return Response({'message': 'success', 'quiz id': str(insert_col.inserted_id)}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)