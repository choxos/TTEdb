from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'studies', api_views.TTEStudyViewSet)
router.register(r'pico-comparisons', api_views.PICOComparisonViewSet)
router.register(r'learning-resources', api_views.LearningResourceViewSet)
router.register(r'statistics', api_views.DatabaseStatisticViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Custom API endpoints
    path('statistics/overview/', api_views.statistics_overview, name='statistics_overview'),
    path('search/', api_views.search_api, name='search_api'),
] 