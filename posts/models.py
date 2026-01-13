from django.db import migrations, models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Kisne post kiya
    title = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateTimeField()
    purpose = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True) # Apne aap date lega

    def __str__(self):
        return self.title