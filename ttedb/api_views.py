from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import TTEStudy, PICOComparison, LearningResource, DatabaseStatistic
from .serializers import (
    TTEStudySerializer, PICOComparisonSerializer, 
    LearningResourceSerializer, DatabaseStatisticSerializer
)


class TTEStudyViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for TTE studies"""
    queryset = TTEStudy.objects.all().order_by('-year', 'first_author')
    serializer_class = TTEStudySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['year', 'disease_category', 'data_type', 'institution_type', 'dag', 'qba']
    search_fields = ['first_author', 'disease', 'institution_names', 'target_trial_name']
    ordering_fields = ['year', 'first_author', 'created_at']
    lookup_field = 'slug'


class PICOComparisonViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for PICO comparisons"""
    queryset = PICOComparison.objects.all().select_related('tte_study')
    serializer_class = PICOComparisonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['effect_measure', 'outcome_type', 'target_trial_name', 'tte_study__disease_category']
    search_fields = ['outcome', 'population', 'intervention', 'comparison', 'target_trial_name']
    ordering_fields = ['tte_study__year', 'target_trial_name', 'outcome']


class LearningResourceViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for learning resources"""
    queryset = LearningResource.objects.all()
    serializer_class = LearningResourceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['resource_type', 'difficulty_level', 'is_featured', 'year']
    search_fields = ['title', 'description', 'tags', 'authors']
    ordering_fields = ['year', 'title', 'view_count']


class DatabaseStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for database statistics"""
    queryset = DatabaseStatistic.objects.all()
    serializer_class = DatabaseStatisticSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['statistic_type']


@api_view(['GET'])
def statistics_overview(request):
    """API endpoint for overview statistics"""
    stats = {
        'total_studies': TTEStudy.objects.count(),
        'total_comparisons': PICOComparison.objects.count(),
        'total_learning_resources': LearningResource.objects.count(),
        'studies_by_year': list(
            TTEStudy.objects.values('year').annotate(count=Count('id')).order_by('year')
        ),
        'studies_by_disease_category': list(
            TTEStudy.objects.values('disease_category').annotate(count=Count('id')).order_by('-count')[:10]
        ),
        'studies_by_data_type': list(
            TTEStudy.objects.values('data_type').annotate(count=Count('id')).order_by('-count')
        ),
    }
    return Response(stats)


@api_view(['GET'])
def search_api(request):
    """Global search API endpoint"""
    query = request.GET.get('q', '')
    
    if not query:
        return Response({'results': []})
    
    # Search across all models
    studies = TTEStudy.objects.filter(
        first_author__icontains=query
    )[:5]
    
    picos = PICOComparison.objects.filter(
        target_trial_name__icontains=query
    ).select_related('tte_study')[:5]
    
    resources = LearningResource.objects.filter(
        title__icontains=query
    )[:5]
    
    results = {
        'studies': TTEStudySerializer(studies, many=True).data,
        'picos': PICOComparisonSerializer(picos, many=True).data,
        'resources': LearningResourceSerializer(resources, many=True).data,
    }
    
    return Response({'results': results}) 