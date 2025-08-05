from django.urls import path
from . import views

app_name = 'ttedb'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('tte/', views.tte_list, name='tte_list'),
    path('tte-vs-rct/', views.tte_vs_rct, name='tte_vs_rct'),
    path('learning-hub/', views.learning_hub, name='learning_hub'),
    path('analysis/', views.analysis, name='analysis'),
    path('about/', views.about, name='about'),
    
    # Detail pages
    path('tte/<slug:slug>/', views.tte_detail, name='tte_detail'),
    path('learning-hub/<int:resource_id>/', views.learning_resource_detail, name='learning_resource_detail'),
    
    # Search and filter endpoints
    path('search/', views.search, name='search'),
] 