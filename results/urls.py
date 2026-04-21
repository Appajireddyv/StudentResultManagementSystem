from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/',  views.login_view,  name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Students
    path('students/',           views.student_list,   name='student_list'),
    path('students/add/',       views.student_add,    name='student_add'),
    path('students/<int:pk>/',       views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/',  views.student_edit,   name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Subjects
    path('subjects/',                  views.subject_list,   name='subject_list'),
    path('subjects/add/',              views.subject_add,    name='subject_add'),
    path('subjects/<int:pk>/edit/',    views.subject_edit,   name='subject_edit'),
    path('subjects/<int:pk>/delete/',  views.subject_delete, name='subject_delete'),

    # Results / Marks
    path('results/',                  views.result_list,   name='result_list'),
    path('results/add/',              views.result_add,    name='result_add'),
    path('results/<int:pk>/edit/',    views.result_edit,   name='result_edit'),
    path('results/<int:pk>/delete/',  views.result_delete, name='result_delete'),

    # Student Views
    path('my-marksheet/', views.my_marksheet, name='my_marksheet'),
    path('api/chart-data/', views.chart_data, name='chart_data'),

    # Departments
    path('departments/',                views.department_list, name='department_list'),
    path('departments/add/',            views.department_add,  name='department_add'),
    path('departments/<int:pk>/edit/',  views.department_edit, name='department_edit'),
]
