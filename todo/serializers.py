from rest_framework import serializers
from .models import Todo


# Converting data in the database to a format such as JSON for use in other applications such as mobile phones
# is called serializer and vice versa is called de-serializer.
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'content']
