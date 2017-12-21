from django.contrib.auth.models import User
from django.db import models


# from faker import Factory
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    comments = models.IntegerField(default=0)
    label = models.CharField(max_length=50, blank=True)

    # d
    # def created_date(cls):
    #   return  cls.created_at.strftime('%Y-%m')

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User)
    avatar_path = models.CharField(max_length=200, default='blog/images/defaultavata.png')
    content = models.CharField(blank=True, max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content


class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_image', blank=True, null=True)

    def __str__(self):
        return self.belong_to.username

        # fake = Factory.create()
        # for counts in range(99):
        #     a = Article(
        #         title=fake.text(max_nb_chars=30),
        #         content=fake.text(max_nb_chars=3000),
        #         label = fake.text(max_nb_chars = 10)
        #         )
        #     a.save()
