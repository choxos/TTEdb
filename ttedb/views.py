from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import TTEStudy, PICOComparison, LearningResource, DatabaseStatistic


def home(request):
    """Main landing page with database overview"""
    context = {
        'total_studies': TTEStudy.objects.count(),
        'total_comparisons': PICOComparison.objects.count(),
        'recent_studies': TTEStudy.objects.select_related().order_by('-created_at')[:5],
        'disease_categories': TTEStudy.objects.values('disease_category').annotate(
            count=Count('id')
        ).order_by('-count')[:10],
    }
    return render(request, 'ttedb/home.html', context)


def tte_list(request):
    """List all TTE studies with search and filtering"""
    studies = TTEStudy.objects.all().order_by('-year', 'first_author')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        studies = studies.filter(
            Q(first_author__icontains=query) |
            Q(disease__icontains=query) |
            Q(disease_category__icontains=query) |
            Q(institution_names__icontains=query) |
            Q(target_trial_name__icontains=query)
        )
    
    # Filtering
    disease_category = request.GET.get('disease_category')
    if disease_category:
        studies = studies.filter(disease_category=disease_category)
    
    data_type = request.GET.get('data_type')
    if data_type:
        studies = studies.filter(data_type=data_type)
    
    year = request.GET.get('year')
    if year:
        studies = studies.filter(year=year)
    
    # Transparency filtering
    transparency = request.GET.get('transparency')
    if transparency == 'high':
        studies = studies.filter(
            Q(protocol__isnull=False) | Q(data_url__isnull=False) | Q(code_url__isnull=False)
        )
    elif transparency == 'low':
        studies = studies.filter(
            protocol__isnull=True, data_url__isnull=True, code_url__isnull=True
        )
    
    # Methodology filtering
    methodology = request.GET.get('methodology')
    if methodology == 'dag':
        studies = studies.filter(dag=True)
    elif methodology == 'qba':
        studies = studies.filter(qba=True)
    elif methodology == 'both':
        studies = studies.filter(dag=True, qba=True)
    
    # Pagination
    paginator = Paginator(studies, 25)
    page = request.GET.get('page')
    studies = paginator.get_page(page)
    
    context = {
        'studies': studies,
        'query': query,
        'disease_categories': TTEStudy.objects.values_list('disease_category', flat=True).distinct().order_by('disease_category'),
        'data_types': TTEStudy.objects.values_list('data_type', flat=True).distinct().order_by('data_type'),
        'years': TTEStudy.objects.values_list('year', flat=True).distinct().order_by('-year'),
    }
    return render(request, 'ttedb/tte_list.html', context)


def tte_vs_rct(request):
    """List studies that compared TTE with RCT results"""
    studies_with_comparisons = TTEStudy.objects.filter(
        pico_comparisons__isnull=False
    ).distinct().order_by('-year', 'first_author')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        studies_with_comparisons = studies_with_comparisons.filter(
            Q(first_author__icontains=query) |
            Q(target_trial_name__icontains=query) |
            Q(pico_comparisons__target_trial_name__icontains=query)
        )
    
    # Filtering
    target_trial = request.GET.get('target_trial')
    if target_trial:
        studies_with_comparisons = studies_with_comparisons.filter(
            pico_comparisons__target_trial_name__icontains=target_trial
        )
    
    effect_measure = request.GET.get('effect_measure')
    if effect_measure:
        studies_with_comparisons = studies_with_comparisons.filter(
            pico_comparisons__effect_measure=effect_measure
        )
    
    disease_category = request.GET.get('disease_category')
    if disease_category:
        studies_with_comparisons = studies_with_comparisons.filter(disease_category=disease_category)
    
    # Pagination
    paginator = Paginator(studies_with_comparisons, 25)
    page = request.GET.get('page')
    studies_with_comparisons = paginator.get_page(page)
    
    context = {
        'studies': studies_with_comparisons,
        'query': query,
        'target_trials': PICOComparison.objects.values_list('target_trial_name', flat=True).distinct().order_by('target_trial_name'),
        'effect_measures': PICOComparison.objects.values_list('effect_measure', flat=True).distinct().order_by('effect_measure'),
        'disease_categories': TTEStudy.objects.filter(pico_comparisons__isnull=False).values_list('disease_category', flat=True).distinct().order_by('disease_category'),
    }
    return render(request, 'ttedb/tte_vs_rct.html', context)


def tte_detail(request, slug):
    """Detail view for a single TTE study"""
    study = get_object_or_404(TTEStudy, slug=slug)
    pico_comparisons = study.pico_comparisons.all().order_by('outcome')
    
    context = {
        'study': study,
        'pico_comparisons': pico_comparisons,
    }
    return render(request, 'ttedb/tte_detail.html', context)


def learning_hub(request):
    """Learning hub with educational resources"""
    resources = LearningResource.objects.all().order_by('-is_featured', '-year', 'title')
    
    # Filtering by resource type
    resource_type = request.GET.get('type')
    if resource_type:
        resources = resources.filter(resource_type=resource_type)
    
    # Filtering by difficulty level
    difficulty = request.GET.get('difficulty')
    if difficulty:
        resources = resources.filter(difficulty_level=difficulty)
    
    # Search
    query = request.GET.get('q')
    if query:
        resources = resources.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(resources, 20)
    page = request.GET.get('page')
    resources = paginator.get_page(page)
    
    context = {
        'resources': resources,
        'resource_types': LearningResource.RESOURCE_TYPES,
        'difficulty_levels': [('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')],
        'query': query,
    }
    return render(request, 'ttedb/learning_hub.html', context)


def learning_resource_detail(request, resource_id):
    """Detail view for a learning resource"""
    resource = get_object_or_404(LearningResource, id=resource_id)
    
    # Increment view count
    resource.view_count += 1
    resource.save(update_fields=['view_count'])
    
    context = {
        'resource': resource,
    }
    return render(request, 'ttedb/learning_resource_detail.html', context)


def statistics(request):
    """Statistics page with database analytics"""
    # Get pre-calculated statistics
    overview_stats = DatabaseStatistic.objects.filter(statistic_type='overview')
    tte_vs_rct_stats = DatabaseStatistic.objects.filter(statistic_type='tte_vs_rct')
    tte_general_stats = DatabaseStatistic.objects.filter(statistic_type='tte_general')
    
    # Calculate some real-time statistics
    total_studies = TTEStudy.objects.count()
    total_comparisons = PICOComparison.objects.count()
    
    # Disease distribution
    disease_distribution = TTEStudy.objects.values('disease_category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Transparency metrics
    studies_with_protocol = TTEStudy.objects.filter(protocol__isnull=False).count()
    studies_with_data = TTEStudy.objects.filter(data_url__isnull=False).count()
    studies_with_code = TTEStudy.objects.filter(code_url__isnull=False).count()
    
    # Methodology usage
    studies_with_dag = TTEStudy.objects.filter(dag=True).count()
    studies_with_qba = TTEStudy.objects.filter(qba=True).count()
    
    # Concordance metrics for TTE vs RCT
    pico_overlapping = PICOComparison.objects.filter(
        rct_estimate__isnull=False, tte_estimate__isnull=False
    ).count()
    
    context = {
        'overview_stats': overview_stats,
        'tte_vs_rct_stats': tte_vs_rct_stats,
        'tte_general_stats': tte_general_stats,
        'total_studies': total_studies,
        'total_comparisons': total_comparisons,
        'disease_distribution': disease_distribution,
        'transparency_metrics': {
            'protocol_percentage': (studies_with_protocol / total_studies * 100) if total_studies > 0 else 0,
            'data_percentage': (studies_with_data / total_studies * 100) if total_studies > 0 else 0,
            'code_percentage': (studies_with_code / total_studies * 100) if total_studies > 0 else 0,
        },
        'methodology_metrics': {
            'dag_percentage': (studies_with_dag / total_studies * 100) if total_studies > 0 else 0,
            'qba_percentage': (studies_with_qba / total_studies * 100) if total_studies > 0 else 0,
        },
        'concordance_metrics': {
            'total_comparisons': pico_overlapping,
        }
    }
    return render(request, 'ttedb/statistics.html', context)


def about(request):
    """About page with team and project information"""
    context = {
        'team_members': [
            {
                'name': 'Ahmad Sofi-Mahmudi',
                'role': 'Principal Investigator',
                'affiliation': 'McMaster University',
                'orcid': '0000-0001-6829-0823',
                'email': 'a.sofimahmudi@gmail.com',
            },
            {
                'name': 'Kristian Thorlund',
                'role': 'Co-Investigator',
                'affiliation': 'McMaster University',
                'orcid': '0000-0002-4645-6924',
                'email': 'thorlunk@mcmaster.ca',
            },
            {
                'name': 'Louis Dron',
                'role': 'Co-Investigator', 
                'affiliation': 'McMaster University',
                'orcid': '0000-0002-8469-1830',
                'email': 'dronl@mcmaster.ca',
            },
            {
                'name': 'Priya Arora',
                'role': 'Co-Investigator',
                'affiliation': 'McMaster University',
                'orcid': '0000-0002-0842-5787',
                'email': 'arorap6@mcmaster.ca',
            },
        ],
    }
    return render(request, 'ttedb/about.html', context)


def search(request):
    """Advanced search with PICO elements and filters"""
    # Get search parameters
    query = request.GET.get('q', '')
    population = request.GET.get('population', '')
    intervention = request.GET.get('intervention', '')
    comparison = request.GET.get('comparison', '')
    outcome = request.GET.get('outcome', '')
    disease_category = request.GET.get('disease_category', '')
    data_type = request.GET.get('data_type', '')
    year_from = request.GET.get('year_from', '')
    year_to = request.GET.get('year_to', '')
    
    # Start with all studies and PICO comparisons
    studies = TTEStudy.objects.all()
    picos = PICOComparison.objects.select_related('tte_study')
    
    # Apply general search query
    if query:
        studies = studies.filter(
            Q(first_author__icontains=query) |
            Q(disease__icontains=query) |
            Q(disease_category__icontains=query) |
            Q(institution__icontains=query) |
            Q(journal__icontains=query) |
            Q(title__icontains=query)
        )
        
        picos = picos.filter(
            Q(target_trial_name__icontains=query) |
            Q(population__icontains=query) |
            Q(intervention__icontains=query) |
            Q(comparison__icontains=query) |
            Q(outcome__icontains=query) |
            Q(tte_study__first_author__icontains=query) |
            Q(tte_study__disease__icontains=query)
        )
    
    # Apply PICO-specific filters
    if population:
        picos = picos.filter(population__icontains=population)
        studies = studies.filter(picocomparison__population__icontains=population).distinct()
    
    if intervention:
        picos = picos.filter(intervention__icontains=intervention)
        studies = studies.filter(picocomparison__intervention__icontains=intervention).distinct()
    
    if comparison:
        picos = picos.filter(comparison__icontains=comparison)
        studies = studies.filter(picocomparison__comparison__icontains=comparison).distinct()
    
    if outcome:
        picos = picos.filter(outcome__icontains=outcome)
        studies = studies.filter(picocomparison__outcome__icontains=outcome).distinct()
    
    # Apply additional filters
    if disease_category:
        studies = studies.filter(disease_category__icontains=disease_category)
        picos = picos.filter(tte_study__disease_category__icontains=disease_category)
    
    if data_type:
        studies = studies.filter(data_type__icontains=data_type)
        picos = picos.filter(tte_study__data_type__icontains=data_type)
    
    if year_from:
        try:
            year_from_int = int(year_from)
            studies = studies.filter(year__gte=year_from_int)
            picos = picos.filter(tte_study__year__gte=year_from_int)
        except ValueError:
            pass
    
    if year_to:
        try:
            year_to_int = int(year_to)
            studies = studies.filter(year__lte=year_to_int)
            picos = picos.filter(tte_study__year__lte=year_to_int)
        except ValueError:
            pass
    
    # Get filter options for the form
    disease_categories = TTEStudy.objects.values_list('disease_category', flat=True).distinct().order_by('disease_category')
    data_types = TTEStudy.objects.values_list('data_type', flat=True).distinct().order_by('data_type')
    
    # Search learning resources if general query provided
    resources = []
    if query:
        resources = LearningResource.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )[:10]
    
    # Pagination
    from django.core.paginator import Paginator
    
    studies_paginator = Paginator(studies, 20)
    picos_paginator = Paginator(picos, 20)
    
    studies_page = request.GET.get('studies_page')
    picos_page = request.GET.get('picos_page')
    
    studies = studies_paginator.get_page(studies_page)
    picos = picos_paginator.get_page(picos_page)
    
    context = {
        'query': query,
        'population': population,
        'intervention': intervention,
        'comparison': comparison,
        'outcome': outcome,
        'disease_category': disease_category,
        'data_type': data_type,
        'year_from': year_from,
        'year_to': year_to,
        'studies': studies,
        'picos': picos,
        'resources': resources,
        'disease_categories': disease_categories,
        'data_types': data_types,
        'total_studies': studies.paginator.count if studies else 0,
        'total_picos': picos.paginator.count if picos else 0,
        'total_resources': len(resources),
    }
    return render(request, 'ttedb/search.html', context)
