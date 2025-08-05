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
    
    # Bayesian Analysis API endpoints
    path('analysis/overview/', api_views.bayesian_analysis_overview, name='bayesian_analysis_overview'),
    path('analysis/export-summary/', api_views.export_summary, name='export_summary'),
    path('analysis/meta-analysis/', api_views.meta_analysis_results, name='meta_analysis_results'),
    path('analysis/descriptive/', api_views.descriptive_results, name='descriptive_results'),
    path('analysis/subgroup/', api_views.subgroup_analysis_results, name='subgroup_analysis_results'),
    path('analysis/forest-plot-data/', api_views.forest_plot_data, name='forest_plot_data'),
] 