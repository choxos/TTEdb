from rest_framework import serializers
from .models import TTEStudy, PICOComparison, LearningResource, DatabaseStatistic


class TTEStudySerializer(serializers.ModelSerializer):
    """Serializer for TTE Study model"""
    
    total_sample_size = serializers.ReadOnlyField()
    has_transparency_indicators = serializers.ReadOnlyField()
    pico_count = serializers.SerializerMethodField()
    
    class Meta:
        model = TTEStudy
        fields = '__all__'
    
    def get_pico_count(self, obj):
        return obj.pico_comparisons.count()


class PICOComparisonSerializer(serializers.ModelSerializer):
    """Serializer for PICO Comparison model"""
    
    tte_study_author = serializers.CharField(source='tte_study.first_author', read_only=True)
    tte_study_year = serializers.IntegerField(source='tte_study.year', read_only=True)
    rct_ci_string = serializers.ReadOnlyField()
    tte_ci_string = serializers.ReadOnlyField()
    estimates_overlap = serializers.ReadOnlyField()
    concordance_direction = serializers.ReadOnlyField()
    
    class Meta:
        model = PICOComparison
        fields = '__all__'


class LearningResourceSerializer(serializers.ModelSerializer):
    """Serializer for Learning Resource model"""
    
    class Meta:
        model = LearningResource
        fields = '__all__'


class DatabaseStatisticSerializer(serializers.ModelSerializer):
    """Serializer for Database Statistic model"""
    
    class Meta:
        model = DatabaseStatistic
        fields = '__all__' 