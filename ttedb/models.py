from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import uuid


class TTEStudy(models.Model):
    """
    Main model representing a Target Trial Emulation study.
    Based on the Studies characteristics CSV structure.
    """
    
    # Basic identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_author = models.CharField(max_length=255)
    year = models.IntegerField()
    doi = models.URLField(max_length=500, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    # Publication details
    preprint = models.CharField(max_length=255, blank=True, null=True, help_text="Preprint DOI or 'No preprint'")
    protocol = models.CharField(max_length=500, blank=True, null=True, help_text="Protocol registration URL")
    
    # Institution information
    INSTITUTION_TYPES = [
        ('academic', 'Academic'),
        ('industry', 'Industry'),
        ('government', 'Government'),
        ('mixed', 'Mixed'),
    ]
    institution_type = models.CharField(max_length=20, choices=INSTITUTION_TYPES, blank=True, null=True)
    institution_names = models.TextField(blank=True, null=True)
    
    # Transparency and research practices
    coi = models.CharField(max_length=255, blank=True, null=True, help_text="Conflicts of interest declaration")
    coi_institutions = models.TextField(blank=True, null=True)
    funding = models.CharField(max_length=255, blank=True, null=True)
    funding_institutions = models.TextField(blank=True, null=True)
    data_url = models.URLField(max_length=500, blank=True, null=True)
    code_url = models.URLField(max_length=500, blank=True, null=True)
    
    # Study context and design
    disease = models.TextField()
    disease_category = models.CharField(max_length=100, blank=True)
    
    # Data characteristics
    DATA_TYPES = [
        ('ehr', 'Electronic Health Records'),
        ('claims', 'Claims Database'),
        ('registry', 'Registry'),
        ('trial', 'Trial Data'),
        ('cohort', 'Cohort Study'),
        ('survey', 'Survey Data'),
        ('other', 'Other'),
    ]
    data_type = models.CharField(max_length=20, choices=DATA_TYPES)
    data_geography = models.CharField(max_length=200, blank=True)
    data_sources_n = models.IntegerField(null=True, blank=True, help_text="Number of data sources")
    
    # Sample characteristics
    eligible_sample = models.CharField(max_length=100, blank=True)
    n_trt = models.IntegerField(null=True, blank=True, help_text="Treatment group size")
    n_ctrl = models.IntegerField(null=True, blank=True, help_text="Control group size")
    n_emulations = models.IntegerField(null=True, blank=True, help_text="Number of emulations")
    trts_n = models.IntegerField(null=True, blank=True, help_text="Number of treatments")
    n_covariates = models.IntegerField(null=True, blank=True, help_text="Number of covariates")
    
    # Methodology
    missing_method = models.CharField(max_length=200, blank=True)
    matching_method = models.CharField(max_length=200, blank=True)
    analysis_method = models.TextField(blank=True)  # Changed from CharField to TextField
    estimand = models.CharField(max_length=200, blank=True)
    
    # Quality indicators
    dag = models.BooleanField(default=False, help_text="Directed Acyclic Graph used")
    qba = models.BooleanField(default=False, help_text="Quantitative Bias Analysis performed")
    
    # Target trial information
    target_trial_name = models.CharField(max_length=255, blank=True, null=True)
    target_trial_reg_no = models.CharField(max_length=100, blank=True, null=True)
    target_trial_doi = models.URLField(max_length=500, blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', 'first_author']
        verbose_name = "TTE Study"
        verbose_name_plural = "TTE Studies"
        indexes = [
            models.Index(fields=['year']),
            models.Index(fields=['disease_category']),
            models.Index(fields=['data_type']),
            models.Index(fields=['first_author']),
        ]
    
    def __str__(self):
        return f"{self.first_author} ({self.year}) - {self.disease}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.first_author}-{self.year}-{self.disease}")
            self.slug = base_slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('ttedb:study_detail', kwargs={'slug': self.slug})
    
    @property
    def has_transparency_indicators(self):
        """Check if study has good transparency practices"""
        return bool(self.protocol or self.data_url or self.code_url)
    
    @property
    def total_sample_size(self):
        """Calculate total sample size if available"""
        if self.n_trt and self.n_ctrl:
            return self.n_trt + self.n_ctrl
        return None


class PICOComparison(models.Model):
    """
    Model representing PICO elements and effect estimates for TTE vs RCT comparisons.
    Based on the PICOs CSV structure.
    """
    
    # Foreign key to the TTE study
    tte_study = models.ForeignKey(TTEStudy, on_delete=models.CASCADE, related_name='pico_comparisons')
    
    # Target trial information
    target_trial_name = models.CharField(max_length=255)
    target_trial_reg_no = models.CharField(max_length=100, blank=True, null=True)
    target_trial_doi = models.URLField(max_length=500, blank=True, null=True)
    
    # PICO elements
    population = models.TextField()
    intervention = models.TextField()
    comparison = models.TextField()
    outcome = models.TextField()
    
    # RCT intervention/comparison (may differ from TTE)
    intervention_rct = models.TextField(blank=True, null=True)
    comparison_rct = models.TextField(blank=True, null=True)
    
    # Outcome classification
    OUTCOME_TYPES = [
        ('efficacy', 'Efficacy'),
        ('safety', 'Safety'),
    ]
    outcome_type = models.CharField(max_length=20, choices=OUTCOME_TYPES)
    
    # Effect measure details
    EFFECT_MEASURES = [
        ('HR', 'Hazard Ratio'),
        ('OR', 'Odds Ratio'),
        ('RR', 'Risk Ratio'),
        ('RD', 'Risk Difference'),
        ('MD', 'Mean Difference'),
        ('SMD', 'Standardized Mean Difference'),
    ]
    effect_measure = models.CharField(max_length=10, choices=EFFECT_MEASURES)
    
    # RCT estimates (allowing null for cases where estimates are not available)
    rct_estimate = models.FloatField(null=True, blank=True)
    rct_lb = models.FloatField(null=True, blank=True, help_text="Lower bound of 95% CI")
    rct_ub = models.FloatField(null=True, blank=True, help_text="Upper bound of 95% CI")
    
    # TTE estimates (allowing null for cases where estimates are not available)
    tte_estimate = models.FloatField(null=True, blank=True)
    tte_lb = models.FloatField(null=True, blank=True, help_text="Lower bound of 95% CI")
    tte_ub = models.FloatField(null=True, blank=True, help_text="Upper bound of 95% CI")
    
    # Difference metrics (calculated)
    tte_rct_diff_estimate = models.FloatField(null=True, blank=True)
    tte_rct_diff_lb = models.FloatField(null=True, blank=True)
    tte_rct_diff_ub = models.FloatField(null=True, blank=True)
    
    # Additional RCT comparisons (for studies with multiple RCTs)
    rct2_estimate = models.FloatField(null=True, blank=True)
    rct2_lb = models.FloatField(null=True, blank=True)
    rct2_ub = models.FloatField(null=True, blank=True)
    
    rct3_estimate = models.FloatField(null=True, blank=True)
    rct3_lb = models.FloatField(null=True, blank=True)
    rct3_ub = models.FloatField(null=True, blank=True)
    
    rct4_estimate = models.FloatField(null=True, blank=True)
    rct4_lb = models.FloatField(null=True, blank=True)
    rct4_ub = models.FloatField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['tte_study', 'outcome']
        verbose_name = "PICO Comparison"
        verbose_name_plural = "PICO Comparisons"
        indexes = [
            models.Index(fields=['effect_measure']),
            models.Index(fields=['outcome_type']),
            models.Index(fields=['target_trial_name']),
        ]
    
    def __str__(self):
        return f"{self.tte_study.first_author} - {self.outcome} ({self.effect_measure})"
    
    @property
    def rct_ci_string(self):
        """Format RCT confidence interval as string"""
        if self.rct_lb is not None and self.rct_ub is not None:
            return f"[{self.rct_lb:.2f}, {self.rct_ub:.2f}]"
        return "Not available"
    
    @property
    def tte_ci_string(self):
        """Format TTE confidence interval as string"""
        if self.tte_lb is not None and self.tte_ub is not None:
            return f"[{self.tte_lb:.2f}, {self.tte_ub:.2f}]"
        return "Not available"
    
    @property
    def estimates_overlap(self):
        """Check if confidence intervals overlap"""
        if all(x is not None for x in [self.tte_lb, self.tte_ub, self.rct_lb, self.rct_ub]):
            return not (self.tte_ub < self.rct_lb or self.rct_ub < self.tte_lb)
        return None
    
    @property
    def concordance_direction(self):
        """Check if estimates point in the same direction for ratio measures"""
        if self.rct_estimate is None or self.tte_estimate is None:
            return None
            
        if self.effect_measure in ['HR', 'OR', 'RR']:
            # For ratio measures, 1.0 is the null value
            rct_direction = 'benefit' if self.rct_estimate < 1.0 else 'harm' if self.rct_estimate > 1.0 else 'null'
            tte_direction = 'benefit' if self.tte_estimate < 1.0 else 'harm' if self.tte_estimate > 1.0 else 'null'
        else:
            # For difference measures, 0.0 is the null value
            rct_direction = 'benefit' if self.rct_estimate < 0.0 else 'harm' if self.rct_estimate > 0.0 else 'null'
            tte_direction = 'benefit' if self.tte_estimate < 0.0 else 'harm' if self.tte_estimate > 0.0 else 'null'
        
        return rct_direction == tte_direction


class LearningResource(models.Model):
    """
    Model for storing learning hub resources like methodological papers, 
    causal inference resources, DAG materials, QBA content, etc.
    """
    
    RESOURCE_TYPES = [
        ('methodological_paper', 'Methodological Paper'),
        ('causal_inference', 'Causal Inference'),
        ('dag', 'Directed Acyclic Graphs'),
        ('qba', 'Quantitative Bias Analysis'),
        ('guidelines', 'Guidelines'),
        ('software', 'Software/Tools'),
        ('tutorial', 'Tutorial'),
        ('book', 'Book'),
        ('course', 'Course'),
    ]
    
    title = models.CharField(max_length=500)
    authors = models.CharField(max_length=500, blank=True, null=True)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    description = models.TextField()
    url = models.URLField(max_length=500)
    doi = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField(null=True, blank=True)
    journal = models.CharField(max_length=255, blank=True, null=True)
    
    # Categorization
    tags = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated tags")
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], default='intermediate')
    
    # Quality indicators
    is_featured = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', '-year', 'title']
        verbose_name = "Learning Resource"
        verbose_name_plural = "Learning Resources"
    
    def __str__(self):
        return f"{self.title} ({self.resource_type})"


class DatabaseStatistic(models.Model):
    """
    Model for storing pre-calculated database statistics for the Statistics page.
    """
    
    STATISTIC_TYPES = [
        ('overview', 'Overview Statistics'),
        ('tte_vs_rct', 'TTE vs RCT Statistics'),
        ('tte_general', 'General TTE Statistics'),
        ('disease_distribution', 'Disease Distribution'),
        ('methodology_trends', 'Methodology Trends'),
        ('transparency_metrics', 'Transparency Metrics'),
    ]
    
    statistic_type = models.CharField(max_length=50, choices=STATISTIC_TYPES)
    name = models.CharField(max_length=255)
    value = models.JSONField()  # Store complex statistics as JSON
    description = models.TextField(blank=True, null=True)
    
    # Metadata
    calculated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['statistic_type', 'name']
        ordering = ['statistic_type', 'name']
        verbose_name = "Database Statistic"
        verbose_name_plural = "Database Statistics"
    
    def __str__(self):
        return f"{self.statistic_type}: {self.name}"
