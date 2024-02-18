from rest_framework import serializers
from .models import Todo
from django.contrib.auth import get_user_model


User = get_user_model()


class TodoSerializer(serializers.ModelSerializer):

    # Setting up the validation system personal
    # def validate_..... --> The name of the field we want to validate
    def validate_priority(self, priority):
        if priority < 10 or priority > 20:
            raise serializers.ValidationError('priority is not ok')
        return priority

    class Meta:
        model = Todo
        # fields = ['id', 'title', 'content']
        fields = '__all__'


# fetch the user list and in addition to serializing the user information,
# it displays the serializing todos list of each user.
class UserSerialzier(serializers.ModelSerializer):
    # The name of the 'todos' is taken from the 'user' field model of 'related_name' part
    todos = TodoSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = '__all__'
