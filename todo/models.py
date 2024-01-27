from django.db import models


# Create model for todo
class Todo(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان')
    content = models.TextField(verbose_name='متن')
    priority = models.IntegerField(default=1, verbose_name='اولویت نمایش')
    is_done = models.BooleanField(default=False, verbose_name='انجام شده/نشده')

    def __str__(self) -> str:
        return f'{self.title} / Is Done: {self.is_done}'

    class Meta:
        # Set the desired table name
        db_table = 'todos'
