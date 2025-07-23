from rest_framework import serializers
from rest_framework.validators import ValidationError
from jobs import models


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobCategory
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Job
        fields = '__all__'
        read_only_fields = ['employer']

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Application
        fields = '__all__'
        read_only_fields = ['applicant']
    