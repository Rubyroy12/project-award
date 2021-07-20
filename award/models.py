from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from cloudinary.models import CloudinaryField 
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',null=True)
    photo = CloudinaryField('image')
    bio = models.CharField(max_length=300)
    name = models.CharField(blank=True, max_length=120)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    @classmethod
    def profile(cls):
        profiles = cls.objects.all()
        return profiles

    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url

    def save_profile(self):
        self.user

    def __str__(self):
        return self.name

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()

class Project(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE,related_name='projects')
    title = models.CharField(blank=True, max_length=120)
    landingpage = CloudinaryField('image')
    description = models.CharField(max_length=300)
    link= models.CharField(max_length=100)
    posted = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-pk"]
    def save_project(self):
        self.save()
    
    def delete_project(self):
        self.delete()
    
    @classmethod
    def search_project(cls, search_term):
        projects= cls.objects.filter(title__icontains=search_term)
        return projects
    
    def __str__(self):
        return self.title

class Rating(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rates', null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='rates', null=True)
    design= models.PositiveIntegerField( null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    usability = models.PositiveIntegerField( null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    content = models.PositiveIntegerField( null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])

    def save_rating(self):
        self.save()
    
    def get_ratings(self, queryset=None):
        rates = Rating.objects.filter(pk=self.kwargs['project.id']).first()
        return rates


class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey('Profile',on_delete=models.CASCADE,related_name='comment')
    project = models.ForeignKey('Project',on_delete=models.CASCADE,related_name='comment')

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return f'{self.user.name} Project'



class ProfileMerch(models.Model):
 
    photo = CloudinaryField('image')
    bio = models.CharField(max_length=300)
    name = models.CharField(blank=True, max_length=120)

class ProjectMerch(models.Model):
   
    title = models.CharField(blank=True, max_length=120)
    landingpage = CloudinaryField('image')
    description = models.CharField(max_length=300)
    link= models.CharField(max_length=100)
    posted = models.DateTimeField(auto_now_add=True)