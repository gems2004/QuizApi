[33mcommit f05e2cf1a5c587e02bb55a52d621a72cefd5d615[m[33m ([m[1;36mHEAD -> [m[1;32mmaster[m[33m, [m[1;31morigin/master[m[33m, [m[1;31morigin/HEAD[m[33m)[m
Author: Georgesa98 <georgesalebe0@gmail.com>
Date:   Thu Jan 4 02:38:13 2024 +0200

    FIRST_COMMIT

[1mdiff --git a/Quizapi/views/quizsList.py b/Quizapi/views/quizsList.py[m
[1mindex e273114..61b1b0b 100644[m
[1m--- a/Quizapi/views/quizsList.py[m
[1m+++ b/Quizapi/views/quizsList.py[m
[36m@@ -42,14 +42,12 @@[m [mclass QuizAPIView(APIView):[m
             else:[m
                 return Response({'message': 'bad request 400'}, status=status.HTTP_400_BAD_REQUEST)[m
 [m
[31m-        if category is None and limit is None:[m
[31m-            questions = list(collection.find())[m
[31m-            serializer = QuestionSerializer(data=questions, many=True)[m
[31m-            if serializer.is_valid():[m
[31m-                return Response({'quiz_list': serializer.data}, status=status.HTTP_200_OK )[m
[31m-            else:[m
[31m-                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)[m
[31m-[m
[32m+[m[32m        questions = list(collection.find())[m
[32m+[m[32m        serializer = QuestionSerializer(data=questions, many=True)[m
[32m+[m[32m        if serializer.is_valid():[m
[32m+[m[32m            return Response({'quiz_list': serializer.data}, status=status.HTTP_200_OK)[m
[32m+[m[32m        else:[m
[32m+[m[32m            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)[m
     def post(self, request):[m
         data = request.data[m
         quiz = {[m
