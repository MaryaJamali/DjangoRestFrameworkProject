from django.db import models
from django.contrib.auth import get_user_model

# Calling the user model and storing it in the variable
user = get_user_model()


# Create model for todo
class Todo(models.Model):
    title = models.CharField(max_length=300, verbose_name='title')
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='todos', verbose_name='user')
    content = models.TextField(verbose_name='text')
    priority = models.IntegerField(default=1, verbose_name='Display priority:')
    is_done = models.BooleanField(default=False, verbose_name='done/not done')

    def __str__(self) -> str:
        return f'{self.title} / Is Done: {self.is_done}'

    class Meta:
        # Set the desired table name
        db_table = 'todos'
