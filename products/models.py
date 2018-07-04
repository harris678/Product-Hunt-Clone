from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Product(models.Model):
    title = models.CharField(max_length=255, unique=True)
    pub_date = models.DateTimeField()
    upvoters = models.ManyToManyField(User, related_name = 'upvoted_by', blank=True)
    body = models.TextField()
    url = models.TextField(unique=True)
    image = models.ImageField(upload_to='images/')
    icon = models.ImageField(upload_to='images/')
    votes_total = models.IntegerField(default = 1)
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]+'...'

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def user(self):
        return self.hunter

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
