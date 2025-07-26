import pandas as pd
import numpy as np
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from ttedb.models import TTEStudy, PICOComparison
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Import TTE data from CSV files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--studies-csv',
            type=str,
            default='dataset/TTE_Metaresearch_Clean_Dataset - Studies characteristics.csv',
            help='Path to the studies characteristics CSV file'
        )
        parser.add_argument(
            '--picos-csv',
            type=str,
            default='dataset/TTE_Metaresearch_Clean_Dataset - PICOs.csv',
            help='Path to the PICOs CSV file'
        )
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear existing data before importing'
        )

    def handle(self, *args, **options):
        studies_csv_path = options['studies_csv']
        picos_csv_path = options['picos_csv']
        
        # Check if files exist
        if not os.path.exists(studies_csv_path):
            raise CommandError(f'Studies CSV file not found: {studies_csv_path}')
        
        if not os.path.exists(picos_csv_path):
            raise CommandError(f'PICOs CSV file not found: {picos_csv_path}')
        
        if options['clear_existing']:
            self.stdout.write('Clearing existing data...')
            PICOComparison.objects.all().delete()
            TTEStudy.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))
        
        # Import studies
        self.stdout.write('Loading studies data...')
        studies_df = pd.read_csv(studies_csv_path)
        studies_count = self.import_studies(studies_df)
        
        # Import PICO comparisons
        self.stdout.write('Loading PICO comparisons data...')
        picos_count = self.import_picos(picos_csv_path)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully imported {studies_count} studies and {picos_count} PICO comparisons'
            )
        )

    @transaction.atomic
    def import_studies(self, df):
        """Import studies from the characteristics CSV"""
        created_count = 0
        
        for index, row in df.iterrows():
            # Skip empty rows
            if pd.isna(row['first_author']):
                continue
            
            # Clean and prepare data
            study_data = self.clean_study_data(row)
            
            try:
                study, created = TTEStudy.objects.get_or_create(
                    doi=study_data['doi'],
                    defaults=study_data
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f'Created study: {study.first_author} ({study.year})')
                else:
                    # Update existing study with new data
                    for key, value in study_data.items():
                        setattr(study, key, value)
                    study.save()
                    self.stdout.write(f'Updated study: {study.first_author} ({study.year})')
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating study for row {index}: {e}')
                )
        
        return created_count

    def import_picos(self, picos_csv_path):
        """Import PICO comparisons data"""
        self.stdout.write('Loading PICO comparisons data...')
        
        df = pd.read_csv(picos_csv_path)
        
        for index, row in df.iterrows():
            try:
                # Find the corresponding TTEStudy
                first_author = self.safe_str(row.get('first_author'))
                year = self.safe_int(row.get('year'))
                
                if not first_author or not year:
                    self.stdout.write(f'Skipping PICO at row {index + 1}: Missing author or year')
                    continue
                
                # Try to find the study - handle duplicates
                try:
                    tte_study = TTEStudy.objects.get(first_author=first_author, year=year)
                except TTEStudy.DoesNotExist:
                    self.stdout.write(f'Study not found for PICO at row {index + 1}: {first_author} ({year})')
                    continue
                except TTEStudy.MultipleObjectsReturned:
                    # Handle duplicate studies by using the first one or trying to find unique identifier
                    studies = TTEStudy.objects.filter(first_author=first_author, year=year)
                    self.stdout.write(f'Multiple studies found for {first_author} ({year}), using first one')
                    tte_study = studies.first()
                
                # Clean and prepare PICO data
                pico_data = self.clean_pico_data(row)
                
                # Skip if essential fields are missing
                if not pico_data.get('outcome'):
                    self.stdout.write(f'Skipping PICO at row {index + 1}: Missing outcome')
                    continue
                
                # Create or update PICO comparison
                pico, created = PICOComparison.objects.get_or_create(
                    tte_study=tte_study,
                    outcome=pico_data['outcome'],
                    target_trial_name=pico_data.get('target_trial_name', ''),
                    effect_measure=pico_data.get('effect_measure', 'HR'),
                    defaults=pico_data
                )
                
                if created:
                    self.stdout.write(f'Created PICO: {tte_study.first_author} - {pico_data["outcome"]}')
                else:
                    # Update existing PICO
                    for key, value in pico_data.items():
                        setattr(pico, key, value)
                    pico.save()
                    self.stdout.write(f'Updated PICO: {tte_study.first_author} - {pico_data["outcome"]}')
                    
            except Exception as e:
                self.stdout.write(f'Error creating PICO for row {index + 1}: {e}')
                continue
        
        return df.shape[0] # Return the number of rows processed

    def safe_str(self, value):
        """Safely convert to string, handling NaN"""
        if pd.isna(value):
            return None
        return str(value).strip() if str(value).strip() else None

    def safe_int(self, value):
        """Safely convert to int, handling NaN"""
        if pd.isna(value) or value == '':
            return None
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None

    def safe_bool(self, value):
        """Safely convert to boolean"""
        if pd.isna(value):
            return False
        if isinstance(value, str):
            return value.lower() in ['yes', 'true', '1', 'y']
        return bool(value)

    def clean_url(self, value):
        """Clean URL field"""
        if pd.isna(value) or value == 'Unavailable' or value == 'NA':
            return None
        url = str(value).strip()
        if url and not url.startswith('http'):
            url = 'https://' + url
        return url

    # Map data types to model choices
    data_type_mapping = {
        'Claims': 'claims',
        'EHR': 'ehr',
        'EMR': 'ehr',
        'Registry': 'registry',
        'National database': 'national_database',
        'RCTs': 'rcts',
        'Survey': 'survey',
    }
    
    institution_type_mapping = {
        'Academic': 'academic',
        'Academia': 'academic',
        'Industry': 'industry',
        'Government': 'government',
        'Mixed': 'mixed',
    }

    def clean_study_data(self, row):
        """Clean and transform study characteristics data"""
        
        data_type = self.safe_str(row.get('data_type', ''))
        data_type = self.data_type_mapping.get(data_type, 'other') if data_type else 'other'
        
        institution_type = self.safe_str(row.get('institution_type', ''))
        institution_type = self.institution_type_mapping.get(institution_type, None)
        
        return {
            'first_author': self.safe_str(row['first_author']),
            'year': self.safe_int(row['year']),
            'doi': self.safe_str(row['doi']),
            'preprint': self.safe_str(row.get('preprint')),
            'protocol': self.safe_str(row.get('protocol')),
            'institution_type': institution_type,
            'institution_names': self.safe_str(row.get('institution_names')),
            'coi': self.safe_str(row.get('coi')),
            'coi_institutions': self.safe_str(row.get('coi_institutions')),
            'funding': self.safe_str(row.get('funding')),
            'funding_institutions': self.safe_str(row.get('funding_institutions')),
            'data_url': self.clean_url(row.get('data_url')),
            'code_url': self.clean_url(row.get('code_url')),
            'disease': self.safe_str(row.get('disease', '')),
            'disease_category': self.safe_str(row.get('disease_category', '')),
            'data_type': data_type,
            'data_sources_n': self.safe_int(row.get('data_sources_n')),
            'data_geography': self.safe_str(row.get('data_geography', '')),
            'missing_method': self.safe_str(row.get('missing_method')),
            'matching_method': self.safe_str(row.get('matching_method')),
            'analysis_method': self.safe_str(row.get('analysis_method')),
            'estimand': self.safe_str(row.get('estimand')),
            'dag': self.safe_bool(row.get('dag')),
            'qba': self.safe_bool(row.get('qba')),
            'n_covariates': self.safe_int(row.get('n_covariates')),
            'trts_n': self.safe_int(row.get('trts_n')),
            'eligible_sample': self.safe_str(row.get('eligible_sample')),
            'n_trt': self.safe_int(row.get('n_trt')),
            'n_ctrl': self.safe_int(row.get('n_ctrl')),
            'n_emulations': self.safe_int(row.get('n_emulations')),
            'target_trial_name': self.safe_str(row.get('target_trial_name')),
            'target_trial_reg_no': self.safe_str(row.get('target_trial_reg_no')),
            'target_trial_doi': self.clean_url(row.get('target_trial_doi')),
        }

    def clean_pico_data(self, row):
        """Clean and transform PICO comparison data"""
        
        def safe_str(value):
            """Safely convert to string, handling NaN"""
            if pd.isna(value):
                return ''
            return str(value).strip()
        
        def safe_float(value):
            """Safely convert to float, handling NaN"""
            if pd.isna(value) or value == '':
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        def clean_url(value):
            """Clean URL field"""
            if pd.isna(value) or value == 'NA':
                return None
            url = str(value).strip()
            if url and not url.startswith('http'):
                url = 'https://' + url
            return url
        
        # Determine outcome type based on context
        outcome_type = 'efficacy'  # Default
        outcome_text = safe_str(row.get('outcome', '')).lower()
        if any(word in outcome_text for word in ['adverse', 'safety', 'toxicity', 'side effect']):
            outcome_type = 'safety'
        
        return {
            'target_trial_name': safe_str(row.get('target_trial_name', '')),
            'target_trial_reg_no': safe_str(row.get('target_trial_reg_no')),
            'target_trial_doi': clean_url(row.get('target_trial_doi')),
            'population': safe_str(row.get('population', '')),
            'intervention': safe_str(row.get('intervention', '')),
            'comparison': safe_str(row.get('comparison', '')),
            'outcome': safe_str(row.get('outcome', '')),
            'outcome_type': outcome_type,
            'effect_measure': safe_str(row.get('effect_measure', 'HR')),
            'rct_estimate': safe_float(row.get('rct_estimate')),
            'rct_lb': safe_float(row.get('rct_lb')),
            'rct_ub': safe_float(row.get('rct_ub')),
            'tte_estimate': safe_float(row.get('tte_estimate')),
            'tte_lb': safe_float(row.get('tte_lb')),
            'tte_ub': safe_float(row.get('tte_ub')),
            'tte_rct_diff_estimate': safe_float(row.get('tte_rct_diff_estimate')),
            'tte_rct_diff_lb': safe_float(row.get('tte_rct_diff_lb')),
            'tte_rct_diff_ub': safe_float(row.get('tte_rct_diff_ub')),
            'rct2_estimate': safe_float(row.get('rct2_estimate')),
            'rct2_lb': safe_float(row.get('rct2_lb')),
            'rct2_ub': safe_float(row.get('rct2_ub')),
            'rct3_estimate': safe_float(row.get('rct3_estimate')),
            'rct3_lb': safe_float(row.get('rct3_lb')),
            'rct3_ub': safe_float(row.get('rct3_ub')),
            'rct4_estimate': safe_float(row.get('rct4_estimate')),
            'rct4_lb': safe_float(row.get('rct4_lb')),
            'rct4_ub': safe_float(row.get('rct4_ub')),
        } 