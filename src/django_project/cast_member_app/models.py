from uuid import uuid4
from django.db import models

# Create your models here.
class CastMember(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid4)
    name = models.CharField(max_length=255)
    type = models.TextField()

    class Meta:
        db_table = 'cast_member'
    
    def __str__(self):
        return self.name