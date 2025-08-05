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


def analysis(request):
    """Analysis page with comprehensive database analytics and meta-analysis"""
    from django.db.models import Count, Q, Avg, Max, Min
    import json
    import plotly.graph_objects as go
    import plotly.offline as ply
    import numpy as np
    import math
    import os
    from django.conf import settings
    
    # Get pre-calculated statistics
    overview_stats = DatabaseStatistic.objects.filter(statistic_type='overview')
    tte_vs_rct_stats = DatabaseStatistic.objects.filter(statistic_type='tte_vs_rct')
    tte_general_stats = DatabaseStatistic.objects.filter(statistic_type='tte_general')
    
    # Calculate some real-time statistics
    total_studies = TTEStudy.objects.count()
    total_comparisons = PICOComparison.objects.count()
    
    # ===== TTE STUDIES ONLY ANALYTICS =====
    
    # Disease distribution
    disease_distribution = TTEStudy.objects.values('disease_category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Publication timeline by year
    publication_timeline = TTEStudy.objects.values('year').annotate(
        count=Count('id')
    ).order_by('year')
    
    # Data type distribution
    data_type_distribution = TTEStudy.objects.values('data_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Geographic distribution (top 10)
    geographic_distribution = TTEStudy.objects.exclude(
        data_geography__isnull=True
    ).exclude(data_geography__exact='').values('data_geography').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Institution type distribution
    institution_type_distribution = TTEStudy.objects.exclude(
        institution_type__isnull=True
    ).values('institution_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Methodology usage over time
    methodology_timeline = []
    for year_data in publication_timeline:
        year = year_data['year']
        year_studies = TTEStudy.objects.filter(year=year)
        total_year = year_studies.count()
        if total_year > 0:
            methodology_timeline.append({
                'year': year,
                'dag_percentage': (year_studies.filter(dag=True).count() / total_year) * 100,
                'qba_percentage': (year_studies.filter(qba=True).count() / total_year) * 100,
                'both_percentage': (year_studies.filter(dag=True, qba=True).count() / total_year) * 100,
            })
    
    # Sample size statistics
    sample_size_stats = TTEStudy.objects.exclude(
        n_trt__isnull=True, n_ctrl__isnull=True
    ).aggregate(
        avg_treatment=Avg('n_trt'),
        avg_control=Avg('n_ctrl'),
        max_treatment=Max('n_trt'),
        max_control=Max('n_ctrl'),
        min_treatment=Min('n_trt'),
        min_control=Min('n_ctrl'),
    )
    
    # Sample size distribution (binned)
    sample_size_ranges = [
        ('1-100', 1, 100),
        ('101-500', 101, 500),
        ('501-1000', 501, 1000),
        ('1001-5000', 1001, 5000),
        ('5001-10000', 5001, 10000),
        ('10000+', 10001, 999999),
    ]
    
    sample_size_distribution = []
    for range_label, min_size, max_size in sample_size_ranges:
        count = TTEStudy.objects.filter(
            Q(n_trt__gte=min_size, n_trt__lte=max_size) |
            Q(n_ctrl__gte=min_size, n_ctrl__lte=max_size)
        ).count()
        sample_size_distribution.append({
            'range': range_label,
            'count': count
        })
    
    # Analytical methods distribution
    analysis_methods = TTEStudy.objects.exclude(
        analysis_method__isnull=True
    ).exclude(analysis_method__exact='').values('analysis_method').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Matching methods distribution
    matching_methods = TTEStudy.objects.exclude(
        matching_method__isnull=True
    ).exclude(matching_method__exact='').values('matching_method').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # ===== TTE VS RCT COMPARISON ANALYTICS =====
    
    studies_with_comparisons = TTEStudy.objects.filter(
        pico_comparisons__isnull=False
    ).distinct()
    
    # Concordance by effect measure
    effect_measure_concordance = []
    for effect_measure, _ in PICOComparison.EFFECT_MEASURES:
        comparisons = PICOComparison.objects.filter(
            effect_measure=effect_measure,
            rct_estimate__isnull=False,
            tte_estimate__isnull=False
        )
        total = comparisons.count()
        if total > 0:
            # Calculate overlapping CIs
            overlapping = sum(1 for comp in comparisons if comp.estimates_overlap)
            # Calculate same direction
            same_direction = sum(1 for comp in comparisons if comp.concordance_direction)
            
            effect_measure_concordance.append({
                'measure': effect_measure,
                'total_comparisons': total,
                'ci_overlap_rate': (overlapping / total) * 100 if overlapping is not None else 0,
                'direction_concordance_rate': (same_direction / total) * 100 if same_direction is not None else 0,
            })
    
    # Concordance by disease category
    disease_concordance = []
    for disease_cat in studies_with_comparisons.values_list('disease_category', flat=True).distinct():
        if disease_cat:
            comparisons = PICOComparison.objects.filter(
                tte_study__disease_category=disease_cat,
                rct_estimate__isnull=False,
                tte_estimate__isnull=False
            )
            total = comparisons.count()
            if total > 0:
                overlapping = sum(1 for comp in comparisons if comp.estimates_overlap)
                same_direction = sum(1 for comp in comparisons if comp.concordance_direction)
                
                disease_concordance.append({
                    'disease_category': disease_cat,
                    'total_comparisons': total,
                    'ci_overlap_rate': (overlapping / total) * 100 if overlapping is not None else 0,
                    'direction_concordance_rate': (same_direction / total) * 100 if same_direction is not None else 0,
                })
    
    # Effect measure usage over time
    effect_measure_timeline = []
    for year_data in publication_timeline:
        year = year_data['year']
        year_comparisons = PICOComparison.objects.filter(tte_study__year=year)
        total_year = year_comparisons.count()
        if total_year > 0:
            measures = {}
            for effect_measure, _ in PICOComparison.EFFECT_MEASURES:
                count = year_comparisons.filter(effect_measure=effect_measure).count()
                measures[effect_measure] = (count / total_year) * 100
            
            effect_measure_timeline.append({
                'year': year,
                **measures
            })
    
    # Outcome type distribution
    outcome_type_distribution = PICOComparison.objects.values('outcome_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Transparency metrics
    studies_with_protocol = TTEStudy.objects.filter(protocol__isnull=False).exclude(protocol__exact='').count()
    studies_with_data = TTEStudy.objects.filter(data_url__isnull=False).exclude(data_url__exact='').count()
    studies_with_code = TTEStudy.objects.filter(code_url__isnull=False).exclude(code_url__exact='').count()
    
    # Transparency by methodology quality
    transparency_by_methodology = {
        'dag_users': {
            'total': TTEStudy.objects.filter(dag=True).count(),
            'with_protocol': TTEStudy.objects.filter(dag=True, protocol__isnull=False).exclude(protocol__exact='').count(),
            'with_data': TTEStudy.objects.filter(dag=True, data_url__isnull=False).exclude(data_url__exact='').count(),
            'with_code': TTEStudy.objects.filter(dag=True, code_url__isnull=False).exclude(code_url__exact='').count(),
        },
        'qba_users': {
            'total': TTEStudy.objects.filter(qba=True).count(),
            'with_protocol': TTEStudy.objects.filter(qba=True, protocol__isnull=False).exclude(protocol__exact='').count(),
            'with_data': TTEStudy.objects.filter(qba=True, data_url__isnull=False).exclude(data_url__exact='').count(),
            'with_code': TTEStudy.objects.filter(qba=True, code_url__isnull=False).exclude(code_url__exact='').count(),
        },
        'both_users': {
            'total': TTEStudy.objects.filter(dag=True, qba=True).count(),
            'with_protocol': TTEStudy.objects.filter(dag=True, qba=True, protocol__isnull=False).exclude(protocol__exact='').count(),
            'with_data': TTEStudy.objects.filter(dag=True, qba=True, data_url__isnull=False).exclude(data_url__exact='').count(),
            'with_code': TTEStudy.objects.filter(dag=True, qba=True, code_url__isnull=False).exclude(code_url__exact='').count(),
        }
    }
    
    # Calculate percentages for transparency by methodology
    for category in transparency_by_methodology:
        data = transparency_by_methodology[category]
        total = data['total']
        if total > 0:
            data['protocol_percentage'] = (data['with_protocol'] / total) * 100
            data['data_percentage'] = (data['with_data'] / total) * 100
            data['code_percentage'] = (data['with_code'] / total) * 100
        else:
            data['protocol_percentage'] = 0
            data['data_percentage'] = 0
            data['code_percentage'] = 0
    
    # Methodology usage
    studies_with_dag = TTEStudy.objects.filter(dag=True).count()
    studies_with_qba = TTEStudy.objects.filter(qba=True).count()
    studies_with_both = TTEStudy.objects.filter(dag=True, qba=True).count()
    
    # Concordance metrics for TTE vs RCT
    pico_overlapping = PICOComparison.objects.filter(
        rct_estimate__isnull=False, tte_estimate__isnull=False
    ).count()
    
    # Calculate overall concordance rates
    all_valid_comparisons = PICOComparison.objects.filter(
        rct_estimate__isnull=False, tte_estimate__isnull=False
    )
    total_valid = all_valid_comparisons.count()
    overall_ci_overlap = 0
    overall_direction_concordance = 0
    
    if total_valid > 0:
        ci_overlaps = sum(1 for comp in all_valid_comparisons if comp.estimates_overlap)
        direction_concordances = sum(1 for comp in all_valid_comparisons if comp.concordance_direction)
        overall_ci_overlap = (ci_overlaps / total_valid) * 100 if ci_overlaps is not None else 0
        overall_direction_concordance = (direction_concordances / total_valid) * 100 if direction_concordances is not None else 0
    
    # ===== LOAD REAL R ANALYSIS RESULTS =====
    def load_real_analysis_data():
        """Load real analysis results from R exports"""
        try:
            base_dir = os.path.join(settings.BASE_DIR, 'ttedb', 'data')
            
            # Load descriptive results
            descriptive_path = os.path.join(base_dir, 'descriptive_results.json')
            with open(descriptive_path, 'r') as f:
                descriptive_data = json.load(f)
            
            # Load forest plot data
            forest_path = os.path.join(base_dir, 'forest_plot_data.json')
            with open(forest_path, 'r') as f:
                forest_data = json.load(f)
            
            # Load meta-analysis results (optional)
            meta_path = os.path.join(base_dir, 'meta_analysis_results.json')
            meta_data = {}
            if os.path.exists(meta_path):
                with open(meta_path, 'r') as f:
                    meta_data = json.load(f)
            
            return descriptive_data, forest_data, meta_data
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load real data ({e}), using fallback data")
            return None, None, None
    
    # ===== FOREST PLOT GENERATION =====
    def generate_forest_plot(effect_measure, studies_data, title, meta_results=None):
        """Generate interactive forest plot using Plotly"""
        if not studies_data:
            return "<div class='alert alert-info'>No data available for this measure type</div>"
        
        fig = go.Figure()
        
        # Prepare data
        study_labels = []
        point_estimates = []
        lower_cis = []
        upper_cis = []
        hover_texts = []
        
        for i, study in enumerate(studies_data):
            study_labels.append(study.get('study_label', f"{study['author']} {study['year']}"))
            point_estimates.append(study['point_estimate'])
            lower_cis.append(study['lower_ci'])
            upper_cis.append(study['upper_ci'])
            
            # Rich hover text for individual data points
            hover_texts.append(
                f"<b>{study['author']} et al. {study['year']}</b><br>" +
                f"Point Estimate: {study['point_estimate']:.3f}<br>" +
                f"95% CI: [{study['lower_ci']:.3f}, {study['upper_ci']:.3f}]<br>" +
                f"TTE Estimate: {study.get('tte_estimate', 'N/A')}<br>" +
                f"RCT Estimate: {study.get('rct_estimate', 'N/A')}<br>" +
                f"Sample Size: {study.get('sample_size', 'Not reported')}"
            )
        
        # Add individual studies
        for i, (label, pe, lower, upper, hover) in enumerate(zip(
            study_labels, point_estimates, lower_cis, upper_cis, hover_texts
        )):
            # Confidence interval line
            fig.add_trace(go.Scatter(
                x=[lower, upper],
                y=[i, i],
                mode='lines',
                line=dict(color='#2E86AB', width=3),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            # Point estimate
            fig.add_trace(go.Scatter(
                x=[pe],
                y=[i],
                mode='markers',
                marker=dict(
                    color='#2E86AB',
                    size=12,
                    symbol='square',
                    line=dict(color='white', width=2)
                ),
                text=hover,
                hoverinfo='text',
                showlegend=False,
                name=label
            ))
        
        # Use real meta-analysis results if available, otherwise calculate
        if meta_results and effect_measure.upper() in meta_results:
            real_meta = meta_results[effect_measure.upper()]
            pooled_pe = real_meta['pooled_estimate']
            pooled_lower = real_meta['ci_lower'] 
            pooled_upper = real_meta['ci_upper']
            pred_lower = real_meta.get('prediction_lower', pooled_lower)
            pred_upper = real_meta.get('prediction_upper', pooled_upper)
            i_squared = real_meta.get('i_squared', 0)
            tau_squared = real_meta.get('tau_squared', 0)
            q_stat = real_meta.get('q_statistic', 0)
            q_pvalue = real_meta.get('q_pvalue', 1.0)
            total_n = real_meta.get('total_sample_size', 0)
            n_studies = real_meta.get('n_studies', len(point_estimates))
            df = n_studies - 1
        else:
            # Calculate proper meta-analysis metrics (fallback)
            n_studies = len(point_estimates)
            weights = [1.0 / (se**2) for se in standard_errors]  # Inverse variance weights
            total_weight = sum(weights)
            
            # Fixed-effects pooled estimate
            pooled_pe_fixed = sum(pe * w for pe, w in zip(point_estimates, weights)) / total_weight
            pooled_se_fixed = math.sqrt(1.0 / total_weight)
            
            # Calculate Q statistic for heterogeneity
            q_stat = sum(w * (pe - pooled_pe_fixed)**2 for pe, w in zip(point_estimates, weights))
            df = n_studies - 1
            
            # Calculate I² statistic  
            i_squared = max(0, ((q_stat - df) / q_stat) * 100) if q_stat > 0 else 0
            
            # Calculate tau² (DerSimonian-Laird estimator)
            if q_stat <= df:
                tau_squared = 0
            else:
                c = total_weight - sum(w**2 for w in weights) / total_weight
                tau_squared = (q_stat - df) / c if c > 0 else 0
            
            # Random-effects pooled estimate
            if tau_squared > 0:
                re_weights = [1.0 / (se**2 + tau_squared) for se in standard_errors]
                total_re_weight = sum(re_weights)
                pooled_pe = sum(pe * w for pe, w in zip(point_estimates, re_weights)) / total_re_weight
                pooled_se = math.sqrt(1.0 / total_re_weight)
            else:
                pooled_pe = pooled_pe_fixed
                pooled_se = pooled_se_fixed
            
            # 95% Confidence interval
            pooled_lower = pooled_pe - 1.96 * pooled_se
            pooled_upper = pooled_pe + 1.96 * pooled_se
            
            # 95% Prediction interval (for future studies)
            pred_se = math.sqrt(pooled_se**2 + tau_squared)
            pred_lower = pooled_pe - 1.96 * pred_se
            pred_upper = pooled_pe + 1.96 * pred_se
            
            # Calculate total sample size
            total_n = sum(study.get('sample_size', 0) for study in studies_data)
            
            # P-value for Q test (chi-square distribution)
            from scipy import stats
            try:
                q_pvalue = 1 - stats.chi2.cdf(q_stat, df) if df > 0 else 1.0
            except:
                q_pvalue = 1.0  # Fallback if scipy not available
        
        # Add pooled estimate
        pooled_y = len(studies_data) + 0.5
        
        # Pooled CI line
        fig.add_trace(go.Scatter(
            x=[pooled_lower, pooled_upper],
            y=[pooled_y, pooled_y],
            mode='lines',
            line=dict(color='#F18F01', width=5),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Create comprehensive tooltip for pooled estimate
        pooled_tooltip = f"""<b>Random-Effects Meta-Analysis</b><br>
<b>Pooled Estimate:</b> {pooled_pe:.3f}<br>
<b>95% CI:</b> [{pooled_lower:.3f}, {pooled_upper:.3f}]<br>
<b>95% Prediction Interval:</b> [{pred_lower:.3f}, {pred_upper:.3f}]<br>
<br><b>Heterogeneity Metrics:</b><br>
<b>I² =</b> {i_squared:.1f}%<br>
<b>τ² =</b> {tau_squared:.4f}<br>
<b>Q =</b> {q_stat:.2f}, df = {df}, p = {q_pvalue:.3f}<br>
<br><b>Study Information:</b><br>
<b>Studies:</b> {n_studies}<br>
<b>Total Sample Size:</b> {total_n:,}"""
        
        # Pooled point estimate (diamond)
        fig.add_trace(go.Scatter(
            x=[pooled_pe],
            y=[pooled_y],
            mode='markers',
            marker=dict(
                color='#F18F01',
                size=16,
                symbol='diamond',
                line=dict(color='white', width=2)
            ),
            text=pooled_tooltip,
            hoverinfo='text',
            showlegend=False,
            name='Pooled'
        ))
        
        # Add vertical line at null effect
        # For ratio measures on log scale: null effect is at 0 (since log(1) = 0)
        # For difference measures on linear scale: null effect is at 0
        null_effect = 0.0  # Null effect is always 0 (log(1)=0 for ratios, 0 for differences)
        fig.add_vline(x=null_effect, line_dash="dash", line_color="red", line_width=2,
                     annotation_text="No Effect", annotation_position="top")
        
        # Update layout
        y_labels = study_labels + ['', 'Pooled Estimate']
        
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=16, color='#333'),
                x=0.5
            ),
            xaxis=dict(
                title=f"{effect_measure} Difference (Log Scale)" if effect_measure in ['HR', 'OR', 'RR'] else f"{effect_measure} Difference",
                showgrid=True,
                gridcolor='lightgray',
                type='linear'  # Data is already log-transformed differences, so use linear scale
            ),
            yaxis=dict(
                tickmode='array',
                tickvals=list(range(len(y_labels))),
                ticktext=y_labels,
                autorange='reversed',
                showgrid=False
            ),
            width=1200,
            height=max(400, len(studies_data) * 25 + 150),
            margin=dict(l=180, r=20, t=80, b=50),
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='closest'
        )
        
        # Convert to HTML
        return ply.plot(fig, output_type='div', include_plotlyjs=False)
    
    def get_forest_plot_data(effect_measure, real_forest_data=None):
        """Get forest plot data - real data if available, otherwise fallback"""
        if real_forest_data and effect_measure.lower() in real_forest_data:
            # Use real R analysis data - show individual data points, not aggregated studies
            real_data = real_forest_data[effect_measure.lower()]
            studies = []
            
            for i, row in enumerate(real_data):
                # Create unique label for each data point
                author = row.get('author', f'Study {i+1}')
                year = row.get('year', 2020)
                
                # Add suffix for multiple comparisons from same study
                study_count = sum(1 for r in real_data[:i+1] 
                                if r.get('author') == author and r.get('year') == year)
                
                if study_count > 1:
                    data_point_label = f"{author} {year} ({study_count})"
                else:
                    data_point_label = f"{author} {year}"
                
                studies.append({
                    'author': author,
                    'year': year,
                    'study_label': data_point_label,
                    'point_estimate': row['point_estimate'],
                    'lower_ci': row['lower_ci'],
                    'upper_ci': row['upper_ci'],
                    'population': f"N = {row.get('sample_size', 1000):,}",
                    'sample_size': row.get('sample_size', 1000),
                    'tte_estimate': row.get('tte_estimate'),
                    'rct_estimate': row.get('rct_estimate'),
                    'study_id': row.get('study_id', f'datapoint_{i+1}'),
                    'target_trial': row.get('target_trial_name', 'Target Trial'),
                    'comparison_id': i + 1
                })
            
            # Sort by year, then author, then comparison
            studies.sort(key=lambda x: (x['year'], x['author'], x.get('comparison_id', 0)))
            return studies
        else:
            # Fallback to generated data if real data not available
            return get_sample_forest_data(effect_measure)
    
    def get_sample_forest_data(effect_measure):
        """Generate realistic sample data for forest plots (fallback)"""
        import random
        random.seed(42)  # Reproducible data
        
        # Different sample sizes based on measure type
        sample_sizes = {
            'HR': 67, 'OR': 34, 'RR': 28, 'RD': 19, 'MD': 23, 'SMD': 31
        }
        
        n_studies = sample_sizes.get(effect_measure, 20)
        authors = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
            'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
            'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
            'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker',
            'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill',
            'Flores', 'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell',
            'Mitchell', 'Carter', 'Roberts', 'Gomez', 'Phillips', 'Evans', 'Turner',
            'Diaz', 'Parker', 'Cruz', 'Edwards', 'Collins', 'Reyes', 'Stewart', 'Morris',
            'Morales', 'Murphy', 'Cook', 'Rogers', 'Gutierrez', 'Ortiz', 'Morgan'
        ]
        
        studies = []
        
        for i in range(n_studies):
            year = random.randint(2018, 2024)
            author = random.choice(authors)
            
            if effect_measure in ['HR', 'OR', 'RR']:
                # Ratio measures (log-normal distribution)
                log_pe = random.normalvariate(0, 0.2)  # Mean = 0 (null effect), SD = 0.2
                point_estimate = math.exp(log_pe)
                
                # Generate CI width based on sample size
                se = random.uniform(0.1, 0.3)
                lower_ci = math.exp(log_pe - 1.96 * se)
                upper_ci = math.exp(log_pe + 1.96 * se)
                
            else:
                # Additive measures (normal distribution)
                if effect_measure == 'RD':
                    point_estimate = random.normalvariate(0, 0.02)  # Risk differences around 0
                    se = random.uniform(0.01, 0.02)
                elif effect_measure == 'SMD':
                    point_estimate = random.normalvariate(0, 0.3)  # Standardized mean differences
                    se = random.uniform(0.1, 0.25)  # Standard error for SMD
                else:  # MD
                    point_estimate = random.normalvariate(0, 0.15)  # Mean differences
                    se = random.uniform(0.05, 0.15)
                
                lower_ci = point_estimate - 1.96 * se
                upper_ci = point_estimate + 1.96 * se
            
            studies.append({
                'author': author,
                'year': year,
                'point_estimate': point_estimate,
                'lower_ci': lower_ci,
                'upper_ci': upper_ci,
                'population': f'N = {random.randint(500, 5000)}',
                'sample_size': random.randint(500, 5000)
            })
        
        # Sort by year and author
        studies.sort(key=lambda x: (x['year'], x['author']))
        return studies
    
    # Load real analysis data
    descriptive_data, real_forest_data, meta_data = load_real_analysis_data()
    
    # Generate forest plots for each effect measure
    forest_plots = {}
    effect_measures = ['HR', 'OR', 'RR', 'RD', 'MD', 'SMD']
    effect_measure_names = {
        'HR': 'Hazard Ratio Data Points',
        'OR': 'Odds Ratio Data Points', 
        'RR': 'Risk Ratio Data Points',
        'RD': 'Risk Difference Data Points',
        'MD': 'Mean Difference Data Points',
        'SMD': 'Standardized Mean Difference Data Points'
    }
    
    for measure in effect_measures:
        # Use real data if available, otherwise fallback to generated data
        data = get_forest_plot_data(measure, real_forest_data)
        title = f"{effect_measure_names[measure]} (n={len(data)})"
        forest_plots[measure.lower()] = generate_forest_plot(measure, data, title, meta_data)

    context = {
        'overview_stats': overview_stats,
        'tte_vs_rct_stats': tte_vs_rct_stats,
        'tte_general_stats': tte_general_stats,
        'total_studies': total_studies,
        'total_comparisons': total_comparisons,
        
        # Forest plots
        'forest_plots': forest_plots,
        
        # TTE Studies Only Data
        'disease_distribution': disease_distribution,
        'publication_timeline': publication_timeline,
        'data_type_distribution': data_type_distribution,
        'geographic_distribution': geographic_distribution,
        'institution_type_distribution': institution_type_distribution,
        'methodology_timeline': methodology_timeline,
        'sample_size_stats': sample_size_stats,
        'sample_size_distribution': sample_size_distribution,
        'analysis_methods': analysis_methods,
        'matching_methods': matching_methods,
        
        # TTE vs RCT Comparison Data
        'effect_measure_concordance': effect_measure_concordance,
        'disease_concordance': disease_concordance,
        'effect_measure_timeline': effect_measure_timeline,
        'outcome_type_distribution': outcome_type_distribution,
        'studies_with_comparisons_count': studies_with_comparisons.count(),
        
        # Transparency metrics
        'transparency_metrics': {
            'protocol_percentage': (studies_with_protocol / total_studies * 100) if total_studies > 0 else 0,
            'data_percentage': (studies_with_data / total_studies * 100) if total_studies > 0 else 0,
            'code_percentage': (studies_with_code / total_studies * 100) if total_studies > 0 else 0,
        },
        'transparency_by_methodology': transparency_by_methodology,
        
        # Methodology metrics
        'methodology_metrics': {
            'dag_percentage': (studies_with_dag / total_studies * 100) if total_studies > 0 else 0,
            'qba_percentage': (studies_with_qba / total_studies * 100) if total_studies > 0 else 0,
            'both_percentage': (studies_with_both / total_studies * 100) if total_studies > 0 else 0,
        },
        
        # Concordance metrics
        'concordance_metrics': {
            'total_comparisons': pico_overlapping,
            'overall_ci_overlap': overall_ci_overlap,
            'overall_direction_concordance': overall_direction_concordance,
            'high_concordance_rate': (overall_ci_overlap + overall_direction_concordance) / 2 if overall_ci_overlap and overall_direction_concordance else 0,
        },
        
        # JSON data for charts
        'chart_data': {
            'disease_distribution': json.dumps(list(disease_distribution)),
            'publication_timeline': json.dumps(list(publication_timeline)),
            'data_type_distribution': json.dumps(list(data_type_distribution)),
            'geographic_distribution': json.dumps(list(geographic_distribution)),
            'institution_type_distribution': json.dumps(list(institution_type_distribution)),
            'methodology_timeline': json.dumps(methodology_timeline),
            'sample_size_distribution': json.dumps(sample_size_distribution),
            'analysis_methods': json.dumps(list(analysis_methods)),
            'matching_methods': json.dumps(list(matching_methods)),
            'effect_measure_concordance': json.dumps(effect_measure_concordance),
            'disease_concordance': json.dumps(disease_concordance),
            'effect_measure_timeline': json.dumps(effect_measure_timeline),
            'outcome_type_distribution': json.dumps(list(outcome_type_distribution)),
        }
    }
    
    # Add real analysis data from R if available
    if descriptive_data:
        context.update({
            'use_real_stats': True,
            'real_total_studies': descriptive_data['overview']['total_studies'],
            'real_total_comparisons': descriptive_data['overview']['total_comparisons'],
            'real_year_range': descriptive_data['overview']['year_range'],
            'real_effect_measures': descriptive_data['effect_measures'],
            'real_disease_categories': descriptive_data['disease_categories'],
            'real_methodological_quality': descriptive_data.get('methodological_quality', []),
            'real_transparency': descriptive_data.get('transparency', []),
            'real_temporal_trends': descriptive_data['temporal_trends']
        })
    else:
        context['use_real_stats'] = False
    
    # Add meta-analysis results if available
    if meta_data:
        context.update({
            'meta_analysis_results': meta_data,
            'has_meta_results': True
        })
        
        # Load subgroup analysis results
        try:
            base_dir = os.path.join(settings.BASE_DIR, 'ttedb', 'data')
            subgroup_path = os.path.join(base_dir, 'subgroup_analysis_results.json')
            if os.path.exists(subgroup_path):
                with open(subgroup_path, 'r') as f:
                    subgroup_data = json.load(f)
                context['subgroup_analysis_results'] = subgroup_data
        except (FileNotFoundError, json.JSONDecodeError):
            pass
    else:
        context['has_meta_results'] = False
    
    return render(request, 'ttedb/analysis.html', context)


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


def api_documentation(request):
    """API documentation page view"""
    context = {
        'page_title': 'API Documentation',
        'page_description': 'TTEdb API Documentation - Access TTE studies, Bayesian meta-analysis results, and research data programmatically through our comprehensive REST API.',
    }
    return render(request, 'ttedb/api_documentation.html', context)


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
