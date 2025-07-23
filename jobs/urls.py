from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jobs.views import JobCategoryViewset, JobViewset, ApplicationViewset
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

router = DefaultRouter()

router.register(r'job_categories', JobCategoryViewset, basename='job_categories')
router.register(r'jobs', JobViewset, basename='jobs')
router.register(r'applications', ApplicationViewset, basename='applications')

urlpatterns = [
    path('', include(router.urls))
]