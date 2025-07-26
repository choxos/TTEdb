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
        picos_df = pd.read_csv(picos_csv_path)
        picos_count = self.import_picos(picos_df)
        
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

    @transaction.atomic
    def import_picos(self, df):
        """Import PICO comparisons from the PICOs CSV"""
        created_count = 0
        
        for index, row in df.iterrows():
            # Skip empty rows
            if pd.isna(row['first_author']):
                continue
            
            try:
                # Find the corresponding TTE study
                study = TTEStudy.objects.get(
                    first_author=str(row['first_author']).strip(),
                    year=int(row['year'])
                )
                
                # Clean and prepare PICO data
                pico_data = self.clean_pico_data(row, study)
                
                # Create PICO comparison
                pico = PICOComparison.objects.create(**pico_data)
                created_count += 1
                
                self.stdout.write(f'Created PICO: {study.first_author} - {pico.outcome}')
                
            except TTEStudy.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f'Study not found for PICO at row {index}: '
                        f'{row["first_author"]} ({row["year"]})'
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating PICO for row {index}: {e}')
                )
        
        return created_count

    def clean_study_data(self, row):
        """Clean and transform study characteristics data"""
        
        def safe_str(value):
            """Safely convert to string, handling NaN"""
            if pd.isna(value):
                return None
            return str(value).strip() if str(value).strip() else None
        
        def safe_int(value):
            """Safely convert to int, handling NaN"""
            if pd.isna(value) or value == '':
                return None
            try:
                return int(float(value))
            except (ValueError, TypeError):
                return None
        
        def safe_bool(value):
            """Safely convert to boolean"""
            if pd.isna(value):
                return False
            if isinstance(value, str):
                return value.lower() in ['yes', 'true', '1', 'y']
            return bool(value)
        
        def clean_url(value):
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
        
        data_type = safe_str(row.get('data_type', ''))
        data_type = data_type_mapping.get(data_type, 'other') if data_type else 'other'
        
        institution_type = safe_str(row.get('institution_type', ''))
        institution_type = institution_type_mapping.get(institution_type, None)
        
        return {
            'first_author': safe_str(row['first_author']),
            'year': safe_int(row['year']),
            'doi': safe_str(row['doi']),
            'preprint': safe_str(row.get('preprint')),
            'protocol': safe_str(row.get('protocol')),
            'institution_type': institution_type,
            'institution_names': safe_str(row.get('institution_names')),
            'coi': safe_str(row.get('coi')),
            'coi_institutions': safe_str(row.get('coi_institutions')),
            'funding': safe_str(row.get('funding')),
            'funding_institutions': safe_str(row.get('funding_institutions')),
            'data_url': clean_url(row.get('data_url')),
            'code_url': clean_url(row.get('code_url')),
            'disease': safe_str(row.get('disease', '')),
            'disease_category': safe_str(row.get('disease_category', '')),
            'data_type': data_type,
            'data_sources_n': safe_int(row.get('data_sources_n')),
            'data_geography': safe_str(row.get('data_geography', '')),
            'missing_method': safe_str(row.get('missing_method')),
            'matching_method': safe_str(row.get('matching_method')),
            'analysis_method': safe_str(row.get('analysis_method')),
            'estimand': safe_str(row.get('estimand')),
            'dag': safe_bool(row.get('dag')),
            'qba': safe_bool(row.get('qba')),
            'n_covariates': safe_int(row.get('n_covariates')),
            'trts_n': safe_int(row.get('trts_n')),
            'eligible_sample': safe_str(row.get('eligible_sample')),
            'n_trt': safe_int(row.get('n_trt')),
            'n_ctrl': safe_int(row.get('n_ctrl')),
            'n_emulations': safe_int(row.get('n_emulations')),
            'target_trial_name': safe_str(row.get('target_trial_name')),
            'target_trial_reg_no': safe_str(row.get('target_trial_reg_no')),
            'target_trial_doi': clean_url(row.get('target_trial_doi')),
        }

    def clean_pico_data(self, row, study):
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
            'tte_study': study,
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