from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from jobs import models, serializers
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .permissions import HasRolePermission
# Create your views here.

class JobCategoryViewset(viewsets.ModelViewSet):
    queryset = models.JobCategory.objects.all()
    serializer_class = serializers.JobCategorySerializer
    permission_classes = [HasRolePermission]

class JobViewset(viewsets.ModelViewSet):
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer
    permission_classes = [HasRolePermission]

    #filtering jobs
    DjangoFilterBackend = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_backends = ['title', 'location', 'category', 'is_active', 'deadline', 'salary']
    search_fields = ['applicant__name', 'title']
    ordering_fields = ['is_shortlisted', 'applied_at']

    #auto-assigning employer the FK of the user who is requesting
    def perform_create(self, serializer):
        return serializer.save(employer=self.request.user)
    
    #getting the soft-deleted application objects
    @action(detail=False, methods=['get'], url_path='deleted_jobs')
    def deleted_apps(self, request):
        apps = models.Job.objects.deleted_objs()
        serializer = self.get_serializer(apps, many=True)
        return Response({'Deleted Jobs': serializer.data})
    

class ApplicationViewset(viewsets.ModelViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializers.ApplicationSerializer
    permission_classes = [HasRolePermission]


    #filtering applications
    DjangoFilterBackend = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_backends = ['is_shortlisted']
    search_fields = ['applicant__name', 'title']
    ordering_fields = ['is_shortlisted', 'applied_at']

    #auto-assigning applicant the FK of the user who is requesting
    def perform_create(self, serializer):
        return serializer.save(applicant=self.request.user)
    
    #getting the soft-deleted application objects
    @action(detail=False, methods=['get'], url_path='deleted_applications')
    def deleted_apps(self, request):
        apps = models.Application.objects.deleted_objs()
        serializer = self.get_serializer(apps, many=True)
        return Response({'Deleted Applications': serializer.data})