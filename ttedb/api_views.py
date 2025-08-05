from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from django.http import JsonResponse
from django.conf import settings
import json
import os
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
    # Get database statistics
    db_stats = {
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
    
    # Add Bayesian analysis statistics if available
    export_data = load_analysis_json('export_summary.json')
    if export_data:
        db_stats['bayesian_analysis'] = {
            'last_updated': export_data.get('export_timestamp'),
            'total_studies_analyzed': export_data.get('total_studies'),
            'total_comparisons_analyzed': export_data.get('total_comparisons'),
            'effect_measures': export_data.get('effect_measures'),
            'analysis_type': export_data.get('export_type')
        }
    
    return Response(db_stats)


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


# =============================================================================
# BAYESIAN ANALYSIS API ENDPOINTS
# =============================================================================

def load_analysis_json(filename):
    """Helper function to load JSON files from ttedb/data directory"""
    file_path = os.path.join(settings.BASE_DIR, 'ttedb', 'data', filename)
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


@api_view(['GET'])
def export_summary(request):
    """API endpoint for export summary information"""
    data = load_analysis_json('export_summary.json')
    if data is None:
        return Response({'error': 'Export summary data not available'}, status=404)
    return Response(data)


@api_view(['GET'])
def meta_analysis_results(request):
    """API endpoint for Bayesian meta-analysis results"""
    data = load_analysis_json('meta_analysis_results.json')
    if data is None:
        return Response({'error': 'Meta-analysis results not available'}, status=404)
    return Response(data)


@api_view(['GET'])
def descriptive_results(request):
    """API endpoint for descriptive analysis results"""
    data = load_analysis_json('descriptive_results.json')
    if data is None:
        return Response({'error': 'Descriptive results not available'}, status=404)
    return Response(data)


@api_view(['GET'])
def subgroup_analysis_results(request):
    """API endpoint for subgroup analysis results"""
    data = load_analysis_json('subgroup_analysis_results.json')
    if data is None:
        return Response({'error': 'Subgroup analysis results not available'}, status=404)
    return Response(data)


@api_view(['GET'])
def forest_plot_data(request):
    """API endpoint for forest plot data"""
    data = load_analysis_json('forest_plot_data.json')
    if data is None:
        return Response({'error': 'Forest plot data not available'}, status=404)
    
    # Optional filtering by effect measure
    effect_measure = request.GET.get('effect_measure')
    if effect_measure and data:
        filtered_data = {k: v for k, v in data.items() if k.upper() == effect_measure.upper()}
        return Response(filtered_data)
    
    return Response(data)


@api_view(['GET'])
def bayesian_analysis_overview(request):
    """API endpoint for comprehensive Bayesian analysis overview"""
    # Load all analysis files
    export_data = load_analysis_json('export_summary.json')
    meta_data = load_analysis_json('meta_analysis_results.json')
    descriptive_data = load_analysis_json('descriptive_results.json')
    subgroup_data = load_analysis_json('subgroup_analysis_results.json')
    
    overview = {
        'analysis_available': any([export_data, meta_data, descriptive_data, subgroup_data]),
        'export_summary': export_data,
        'meta_analysis_summary': {
            'available_measures': list(meta_data.keys()) if meta_data else [],
            'total_measures': len(meta_data) if meta_data else 0
        },
        'descriptive_summary': {
            'overview': descriptive_data.get('overview') if descriptive_data else None
        },
        'subgroup_summary': {
            'available_groupings': list(subgroup_data.keys()) if subgroup_data else [],
            'total_subgroups': sum(len(v) for v in subgroup_data.values()) if subgroup_data else 0
        },
        'endpoints': {
            'export_summary': '/api/analysis/export-summary/',
            'meta_analysis': '/api/analysis/meta-analysis/',
            'descriptive': '/api/analysis/descriptive/',
            'subgroup': '/api/analysis/subgroup/',
            'forest_plot_data': '/api/analysis/forest-plot-data/',
        }
    }
    
    return Response(overview) 