from rest_framework import generics, status
from attr import attr
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from django.shortcuts import render

from .models import Teacher

from apps.students.models import Assignment, Student

from .serializers import TeacherAssignmentSerializer



class AssignmentsView(generics.ListCreateAPIView):
    serializer_class = TeacherAssignmentSerializer


    def get(self, request, *args, **kwargs):
        assignments = Assignment.objects.filter(teacher__user=request.user)

        return Response(
            data=self.serializer_class(assignments, many=True).data,
            status=status.HTTP_200_OK
        )


    def post(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(user=request.user)
        request.data['teacher'] = teacher.id

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(user=request.user)
        request.data['teacher'] = teacher.id

        

                
        try:
            assignment = Assignment.objects.get(pk=request.data['id'], teacher__user=request.user)
            
            request.data['state'] = assignment.state
            
        except Assignment.DoesNotExist:

            if 'student' in request.data:
                return Response(
                data={'non_field_errors': ['Teacher cannot change the student who submitted the assignment']}, status=status.HTTP_400_BAD_REQUEST
            )

            if 'grade' in request.data:
                return Response(
                data={'non_field_errors': ['Teacher cannot grade for other teacher''s assignment']}, status=status.HTTP_400_BAD_REQUEST
            )

            return Response(
                data={'error': 'Assignment does not exist/permission denied'}, status=status.HTTP_400_BAD_REQUEST
            )

        

        serializer = self.serializer_class(assignment, data=request.data, partial=True)

        

        if serializer.is_valid():
            if 'grade' in request.data and request.data['state'] == 'SUBMITTED':
                serializer.validated_data['state'] = 'GRADED'

            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_200_OK
            )

        
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )



    