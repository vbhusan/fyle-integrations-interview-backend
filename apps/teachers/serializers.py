from attr import attr
from rest_framework import serializers
from apps.students.models import Assignment


class TeacherAssignmentSerializer(serializers.ModelSerializer):
    """
    Teacher Assignment serializer
    """
    class Meta:
        model = Assignment
        fields = '__all__'

    def validate(self, attrs):

        if 'content' in attrs and attrs['content']:
            raise serializers.ValidationError('Teacher cannot change the content of the assignment')

        


        if 'state' in attrs:
            if attrs['state'] == 'GRADED' and ('grade' in attrs and attrs['grade']) :
                raise serializers.ValidationError('GRADED assignments cannot be graded again')

            if attrs['state'] == 'DRAFT' and ('grade' in attrs and attrs['grade']) :
                raise serializers.ValidationError('SUBMITTED assignments can only be graded')
                

        if self.partial:
            return attrs

        return super().validate(attrs)
