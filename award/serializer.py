from rest_framework import serializers
from .models import ProfileMerch, ProjectMerch

class MerchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileMerch
        fields= ('photo','bio', 'name')

class MerchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMerch
        fields= ('title','lanidingpage','description', 'link')
        