from django.core.management.base import BaseCommand
from ttedb.models import LearningResource


class Command(BaseCommand):
    help = 'Populate learning hub with relevant methodological resources'

    def handle(self, *args, **options):
        resources = [
            # Target Trial Emulation Papers
            {
                'title': 'Using big data to emulate a target trial when a randomized trial is not available',
                'authors': 'Hernán MA, Robins JM',
                'resource_type': 'methodological_paper',
                'description': 'Foundational paper introducing the target trial framework for causal inference using observational data.',
                'url': 'https://doi.org/10.1093/aje/kww079',
                'doi': '10.1093/aje/kww079',
                'year': 2016,
                'journal': 'American Journal of Epidemiology',
                'tags': 'target trial, emulation, causal inference, observational data',
                'difficulty_level': 'intermediate',
                'is_featured': True,
            },
            {
                'title': 'The target trial approach: an emerging framework for studies of medical interventions',
                'authors': 'Hernán MA, Wang W, Leaf DE',
                'resource_type': 'methodological_paper',
                'description': 'Comprehensive overview of the target trial approach and its applications in medical research.',
                'url': 'https://doi.org/10.1001/jama.2021.21646',
                'doi': '10.1001/jama.2021.21646',
                'year': 2022,
                'journal': 'JAMA',
                'tags': 'target trial, medical interventions, study design',
                'difficulty_level': 'beginner',
                'is_featured': True,
            },
            {
                'title': 'Benchmarking observational methods by comparing randomized trials and their emulations',
                'authors': 'Franklin JM, Patorno E, Desai RJ, et al.',
                'resource_type': 'methodological_paper',
                'description': 'Systematic comparison of observational studies emulating randomized trials to assess validity.',
                'url': 'https://doi.org/10.1097/EDE.0000000000000692',
                'doi': '10.1097/EDE.0000000000000692',
                'year': 2017,
                'journal': 'Epidemiology',
                'tags': 'benchmarking, observational methods, emulation',
                'difficulty_level': 'advanced',
                'is_featured': False,
            },
            
            # Causal Inference Resources
            {
                'title': 'Causal Inference: What If',
                'authors': 'Hernán MA, Robins JM',
                'resource_type': 'book',
                'description': 'Comprehensive textbook on causal inference methods, freely available online.',
                'url': 'https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/',
                'year': 2020,
                'tags': 'causal inference, textbook, epidemiology, biostatistics',
                'difficulty_level': 'intermediate',
                'is_featured': True,
            },
            {
                'title': 'Causal inference in statistics: An overview',
                'authors': 'Pearl J',
                'resource_type': 'methodological_paper',
                'description': 'Foundational overview of causal inference from a statistical perspective by Judea Pearl.',
                'url': 'https://doi.org/10.1214/09-SS057',
                'doi': '10.1214/09-SS057',
                'year': 2009,
                'journal': 'Statistical Surveys',
                'tags': 'causal inference, Pearl, statistics',
                'difficulty_level': 'advanced',
                'is_featured': False,
            },
            
            # Directed Acyclic Graphs (DAGs)
            {
                'title': 'A crash course in good and bad controls',
                'authors': 'Cinelli C, Forney A, Pearl J',
                'resource_type': 'methodological_paper',
                'description': 'Practical guide to selecting control variables using causal graphs.',
                'url': 'https://doi.org/10.1177/00491241211011068',
                'doi': '10.1177/00491241211011068',
                'year': 2022,
                'journal': 'Sociological Methods & Research',
                'tags': 'DAG, control variables, confounding, causal graphs',
                'difficulty_level': 'intermediate',
                'is_featured': True,
            },
            {
                'title': 'DAGitty: A graphical tool for analyzing causal diagrams',
                'authors': 'Textor J, van der Zander B, Gilthorpe MS, et al.',
                'resource_type': 'software',
                'description': 'Web-based application for drawing and analyzing causal diagrams (DAGs).',
                'url': 'http://www.dagitty.net/',
                'year': 2016,
                'journal': 'Epidemiology',
                'tags': 'DAG, software, causal diagrams, tool',
                'difficulty_level': 'beginner',
                'is_featured': True,
            },
            {
                'title': 'Causal diagrams for epidemiologic research',
                'authors': 'Greenland S, Pearl J, Robins JM',
                'resource_type': 'methodological_paper',
                'description': 'Classic paper introducing causal diagrams to epidemiologic research.',
                'url': 'https://doi.org/10.1097/00001648-199901000-00008',
                'doi': '10.1097/00001648-199901000-00008',
                'year': 1999,
                'journal': 'Epidemiology',
                'tags': 'causal diagrams, epidemiology, DAG',
                'difficulty_level': 'intermediate',
                'is_featured': False,
            },
            
            # Quantitative Bias Analysis (QBA)
            {
                'title': 'Modern Epidemiology, 4th Edition',
                'authors': 'Rothman KJ, Greenland S, Lash TL',
                'resource_type': 'book',
                'description': 'Authoritative textbook including chapters on bias analysis and uncertainty quantification.',
                'url': 'https://www.wolterskluwer.com/en/solutions/ovid/modern-epidemiology-1488',
                'year': 2021,
                'tags': 'epidemiology, bias analysis, methodology',
                'difficulty_level': 'advanced',
                'is_featured': False,
            },
            {
                'title': 'Applying Quantitative Bias Analysis to Epidemiologic Data',
                'authors': 'Lash TL, Fox MP, Fink AK',
                'resource_type': 'book',
                'description': 'Comprehensive guide to quantitative bias analysis methods in epidemiology.',
                'url': 'https://link.springer.com/book/10.1007/978-0-387-87959-8',
                'year': 2009,
                'tags': 'quantitative bias analysis, QBA, epidemiology',
                'difficulty_level': 'advanced',
                'is_featured': True,
            },
            {
                'title': 'The E-value: A tool for quantifying bias in observational studies',
                'authors': 'VanderWeele TJ, Ding P',
                'resource_type': 'methodological_paper',
                'description': 'Introduction to E-values for sensitivity analysis of unmeasured confounding.',
                'url': 'https://doi.org/10.7326/M16-2607',
                'doi': '10.7326/M16-2607',
                'year': 2017,
                'journal': 'Annals of Internal Medicine',
                'tags': 'E-value, sensitivity analysis, confounding, bias',
                'difficulty_level': 'intermediate',
                'is_featured': True,
            },
            
            # Statistical Methods
            {
                'title': 'Propensity score methods for bias reduction in the comparison of a treatment to a non-randomized control group',
                'authors': 'Rosenbaum PR, Rubin DB',
                'resource_type': 'methodological_paper',
                'description': 'Foundational paper on propensity score methods for causal inference.',
                'url': 'https://doi.org/10.2307/2335942',
                'doi': '10.2307/2335942',
                'year': 1983,
                'journal': 'Biometrika',
                'tags': 'propensity scores, matching, causal inference',
                'difficulty_level': 'advanced',
                'is_featured': False,
            },
            {
                'title': 'Marginal structural models and causal inference in epidemiology',
                'authors': 'Robins JM, Hernán MA, Brumback B',
                'resource_type': 'methodological_paper',
                'description': 'Introduction to marginal structural models for time-varying treatments.',
                'url': 'https://doi.org/10.1097/00001648-200009000-00011',
                'doi': '10.1097/00001648-200009000-00011',
                'year': 2000,
                'journal': 'Epidemiology',
                'tags': 'marginal structural models, time-varying treatment, causal inference',
                'difficulty_level': 'advanced',
                'is_featured': False,
            },
            
            # Online Courses and Tutorials
            {
                'title': 'Introduction to Causal Inference (Harvard)',
                'authors': 'Miguel Hernán',
                'resource_type': 'course',
                'description': 'Free online course on causal inference methods taught by Miguel Hernán.',
                'url': 'https://www.edx.org/course/introduction-to-causal-inference',
                'year': 2023,
                'tags': 'causal inference, online course, tutorial',
                'difficulty_level': 'beginner',
                'is_featured': True,
            },
            {
                'title': 'Target Trial Emulation Tutorial',
                'authors': 'Dickerman BA, García-Albéniz X, Logan RW, et al.',
                'resource_type': 'tutorial',
                'description': 'Practical tutorial on implementing target trial emulation with example code.',
                'url': 'https://doi.org/10.1097/EDE.0000000000001434',
                'doi': '10.1097/EDE.0000000000001434',
                'year': 2022,
                'journal': 'Epidemiology',
                'tags': 'target trial emulation, tutorial, practical guide',
                'difficulty_level': 'intermediate',
                'is_featured': True,
            },
            
            # Guidelines and Recommendations
            {
                'title': 'STROBE-MR: Guidelines for reporting Mendelian randomization studies',
                'authors': 'Davey Smith G, Davies NM, Dimou N, et al.',
                'resource_type': 'guidelines',
                'description': 'Reporting guidelines for Mendelian randomization studies.',
                'url': 'https://doi.org/10.1136/bmj.n2233',
                'doi': '10.1136/bmj.n2233',
                'year': 2021,
                'journal': 'BMJ',
                'tags': 'guidelines, Mendelian randomization, reporting',
                'difficulty_level': 'intermediate',
                'is_featured': False,
            },
            
            # Software and Tools
            {
                'title': 'The tableone package for R',
                'authors': 'Yoshida K, Bohn J',
                'resource_type': 'software',
                'description': 'R package for creating baseline characteristic tables in medical research.',
                'url': 'https://cran.r-project.org/package=tableone',
                'year': 2022,
                'tags': 'R package, baseline characteristics, software',
                'difficulty_level': 'beginner',
                'is_featured': False,
            },
            {
                'title': 'DoWhy: A Python library for causal inference',
                'authors': 'Sharma A, Kiciman E',
                'resource_type': 'software',
                'description': 'Python library that provides a unified interface for causal inference methods.',
                'url': 'https://github.com/microsoft/dowhy',
                'year': 2020,
                'tags': 'Python, causal inference, software, machine learning',
                'difficulty_level': 'intermediate',
                'is_featured': True,
            },
        ]

        created_count = 0
        for resource_data in resources:
            resource, created = LearningResource.objects.get_or_create(
                title=resource_data['title'],
                defaults=resource_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created resource: {resource.title}')
            else:
                self.stdout.write(f'Resource already exists: {resource.title}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully processed {len(resources)} resources. Created {created_count} new resources.')
        ) 