from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import TTEStudy, PICOComparison, LearningResource, DatabaseStatistic
import csv
import io


@admin.register(TTEStudy)
class TTEStudyAdmin(admin.ModelAdmin):
    list_display = [
        'first_author', 'year', 'disease', 'disease_category', 
        'data_type', 'institution_type', 'has_transparency_indicators',
        'dag', 'qba', 'pico_count'
    ]
    list_filter = [
        'year', 'disease_category', 'data_type', 'institution_type',
        'dag', 'qba', 'coi', 'funding'
    ]
    search_fields = [
        'first_author', 'disease', 'institution_names', 
        'target_trial_name', 'doi'
    ]
    readonly_fields = ['id', 'slug', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_author', 'year', 'doi', 'slug')
        }),
        ('Publication Details', {
            'fields': ('preprint', 'protocol')
        }),
        ('Institution & Funding', {
            'fields': ('institution_type', 'institution_names', 'coi', 'coi_institutions', 
                      'funding', 'funding_institutions')
        }),
        ('Study Context', {
            'fields': ('disease', 'disease_category', 'data_type', 'data_sources_n', 
                      'data_geography')
        }),
        ('Methodology', {
            'fields': ('missing_method', 'matching_method', 'analysis_method', 
                      'estimand', 'dag', 'qba')
        }),
        ('Sample Characteristics', {
            'fields': ('n_covariates', 'trts_n', 'eligible_sample', 'n_trt', 
                      'n_ctrl', 'n_emulations')
        }),
        ('Target Trial', {
            'fields': ('target_trial_name', 'target_trial_reg_no', 'target_trial_doi')
        }),
        ('Transparency', {
            'fields': ('data_url', 'code_url')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def pico_count(self, obj):
        return obj.pico_comparisons.count()
    pico_count.short_description = 'PICO Comparisons'
    
    def has_transparency_indicators(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if obj.has_transparency_indicators else 'red',
            '✓' if obj.has_transparency_indicators else '✗'
        )
    has_transparency_indicators.short_description = 'Transparency'


class PICOComparisonInline(admin.TabularInline):
    model = PICOComparison
    extra = 0
    readonly_fields = ['created_at', 'updated_at']
    fields = [
        'target_trial_name', 'outcome', 'outcome_type', 'effect_measure',
        'rct_estimate', 'rct_lb', 'rct_ub',
        'tte_estimate', 'tte_lb', 'tte_ub'
    ]


@admin.register(PICOComparison)
class PICOComparisonAdmin(admin.ModelAdmin):
    list_display = [
        'tte_study', 'target_trial_name', 'outcome', 'effect_measure',
        'outcome_type', 'rct_estimate', 'tte_estimate', 'estimates_overlap',
        'concordance_direction'
    ]
    list_filter = [
        'effect_measure', 'outcome_type', 'target_trial_name',
        'tte_study__disease_category', 'tte_study__year'
    ]
    search_fields = [
        'tte_study__first_author', 'target_trial_name', 'outcome',
        'population', 'intervention', 'comparison'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Study Information', {
            'fields': ('tte_study', 'target_trial_name', 'target_trial_reg_no', 
                      'target_trial_doi')
        }),
        ('PICO Elements', {
            'fields': ('population', 'intervention', 'comparison', 'outcome',
                      'intervention_rct', 'comparison_rct', 'outcome_type')
        }),
        ('Effect Measures', {
            'fields': ('effect_measure',)
        }),
        ('RCT Results', {
            'fields': ('rct_estimate', 'rct_lb', 'rct_ub')
        }),
        ('TTE Results', {
            'fields': ('tte_estimate', 'tte_lb', 'tte_ub')
        }),
        ('Difference Metrics', {
            'fields': ('tte_rct_diff_estimate', 'tte_rct_diff_lb', 'tte_rct_diff_ub'),
            'classes': ('collapse',)
        }),
        ('Additional RCT Comparisons', {
            'fields': ('rct2_estimate', 'rct2_lb', 'rct2_ub',
                      'rct3_estimate', 'rct3_lb', 'rct3_ub',
                      'rct4_estimate', 'rct4_lb', 'rct4_ub'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def estimates_overlap(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if obj.estimates_overlap else 'red',
            '✓' if obj.estimates_overlap else '✗'
        )
    estimates_overlap.short_description = 'CI Overlap'
    
    def concordance_direction(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if obj.concordance_direction else 'orange',
            '✓' if obj.concordance_direction else '?'
        )
    concordance_direction.short_description = 'Direction Agreement'


@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'resource_type', 'year', 'difficulty_level',
        'is_featured', 'view_count'
    ]
    list_filter = [
        'resource_type', 'difficulty_level', 'is_featured', 'year'
    ]
    search_fields = ['title', 'authors', 'description', 'tags']
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'authors', 'resource_type', 'year')
        }),
        ('Content', {
            'fields': ('description', 'url', 'doi', 'journal')
        }),
        ('Categorization', {
            'fields': ('tags', 'difficulty_level', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(DatabaseStatistic)
class DatabaseStatisticAdmin(admin.ModelAdmin):
    list_display = ['statistic_type', 'name', 'calculated_at']
    list_filter = ['statistic_type', 'calculated_at']
    search_fields = ['name', 'description']
    readonly_fields = ['calculated_at']
    
    fieldsets = (
        ('Statistic Information', {
            'fields': ('statistic_type', 'name', 'description')
        }),
        ('Data', {
            'fields': ('value',)
        }),
        ('Metadata', {
            'fields': ('calculated_at',)
        })
    )


# Custom admin actions
class TTEDataImportAdmin(admin.ModelAdmin):
    """Custom admin view for importing TTE data from CSV files"""
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv, name='import_csv'),
        ]
        return custom_urls + urls
    
    def import_csv(self, request):
        if request.method == "POST":
            # Handle CSV import logic here
            csv_file = request.FILES.get("csv_file")
            if csv_file:
                # Process the CSV file
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                # Implementation will be added in the next step
                messages.success(request, "CSV file processed successfully")
            return HttpResponseRedirect("../")
        
        return render(request, "admin/import_csv.html")


# Customize the admin site
admin.site.site_header = "TTEdb Administration"
admin.site.site_title = "TTEdb Admin"
admin.site.index_title = "Target Trial Emulation Database Administration"
