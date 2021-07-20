from future import unicode_literals
from .models import Profile,Projects

from django.test import TestCase

# Create your tests here.
class ProfileTestClass(TestCase):

    # Set up method
    def setUp(self):
        self.profile = Profile(id=1,user= 'fits',image='name',bio='Test bio')
        
    # Testing  instance
    def test_instance(self):
        self.assertTrue(isinstance( self.profile,Profile))


    def test_update_profile(self):
        self.profile.save_profle()
        self.profile.update_create_profile(self.profile.id, 'fits')
        changed_profile = Profile.objects.filter(name ='fits')
        self.assertTrue(len(changed_profile) > 0) 
    
    # Testing Save Method
    def test_save_method(self):
        self.profile.save_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile) > 0)

class ProjectTestClass(TestCase):

    # Set up method
    def setUp(self):
        self.project = Projects(id=1,author= 'self.profile',image='name',description='Test instance',created_date='19/07/2021',title='test_title',link='test_link',author_profile='self.profile')
        
    # Testing  instance
    def test_instance(self):
        self.assertTrue(isinstance( self.project,Projects))

        # Testing Save Method
    def test_save_method(self):
        self.project.save_project()
        project = Projects.objects.all()
        self.assertTrue(len(project) > 0)

    def test_delete_project(self):
        self.project.delete_project()
        project = Projects.objects.all()
        self.assertTrue(len(project)== 0)

    def tearDown(self):
        Profile.objects.all().delete()
        Projects.objects.all().delete()