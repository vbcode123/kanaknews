from django.urls import path
from . import views

urlpatterns = [
    # ==========================================
    # 1. Authentication / Login URLs (Admin, Reporter & Desk)
    # ==========================================
    path('', views.login_view, name='login_home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reporter/logout/', views.reporter_logout_view, name='reporter_logout'),
    path('desk/logout/', views.desk_logout_view, name='desk_logout'),

    # ==========================================
    # 2. Admin Dashboard & Profile
    # ==========================================
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),

    # ==========================================
    # 3. Reporter Management URLs (Admin Control)
    # ==========================================
    path('reporters/', views.reporter_list_view, name='reporter_list'),
    path('reporters/add/', views.reporter_add_view, name='reporter_add'),
    path('reporters/view/<int:pk>/', views.reporter_detail_view, name='reporter_view'),
    path('reporters/edit/<int:pk>/', views.reporter_edit_view, name='reporter_edit'),
    path('reporters/delete/<int:pk>/', views.reporter_delete_view, name='reporter_delete'),

    # ==========================================
    # 4. Desk Management URLs (Admin Control)
    # ==========================================
    path('desks/', views.desk_list_view, name='desk_list'),
    path('desks/add/', views.desk_add_view, name='desk_add'),
    path('desks/view/<int:pk>/', views.desk_detail_view, name='desk_view'),
    path('desks/edit/<int:pk>/', views.desk_edit_view, name='desk_edit'),
    path('desks/delete/<int:pk>/', views.desk_delete_view, name='desk_delete'),

    # ==========================================
    # 5. Reporter Portal URLs (Reporter Access)
    # ==========================================
    path('reporter/dashboard/', views.reporter_dashboard_view, name='reporter_dashboard'),
    path('reporter/profile/', views.reporter_profile_view, name='reporter_profile'),

    # ==========================================
    # 6. Desk Portal URLs (Desk Staff Access)
    # ==========================================
    path('desk/dashboard/', views.desk_dashboard_view, name='desk_dashboard'),
    path('desk/profile/', views.desk_profile_view, name='desk_profile'),

    # ==========================================
    # 7. News Management URLs (Reporter, Admin & Desk)
    # ==========================================
    path('news/', views.news_list_view, name='news_list'),
    path('news/add/', views.news_add_view, name='news_add'),
    path('news/view/<int:pk>/', views.news_detail_view, name='news_view'),
    path('news/edit/<int:pk>/', views.news_edit_view, name='news_edit'),
    path('news/delete/<int:pk>/', views.news_delete_view, name='news_delete'),

    # Convenient portal aliases
    path('reporter/news/', views.news_list_view, name='reporter_news_list'),
    path('reporter/news/add/', views.news_add_view, name='reporter_news_add'),
    path('desk/news/', views.news_list_view, name='desk_news_list'),
    path('desk/news/add/', views.news_add_view, name='desk_news_add'),
]

