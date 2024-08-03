from django.db import models


class BaseModel(models.Model):
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted = True
        self.save()


class BaseModelManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class Task(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BaseModelManager()

    def __str__(self):
        return self.title
