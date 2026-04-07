from django.urls import path
from .views import login_view, logout_view
from .views import (
    login_view,
    logout_view,

    master_tables,
    view_master,
    add_master,
    seed_master_data,

    admin_dashboard,
    teacher_dashboard,
    teacher_list,
    add_teacher,
    delete_teacher,
    edit_teacher,
    
    show_report,
    
    student_dashboard,
    student_list,
    add_student,
    delete_student,
    edit_student,

    create_quiz,
    review_quiz,
    list_quiz,
    assign_quiz,
    attempt_quiz
)

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('master-tables/', master_tables),
    path('view-master/<str:master_type>/', view_master),
    path('add-master/<str:master_type>/', add_master),
    path('seed-master-data/', seed_master_data),

    path('admin-dashboard/', admin_dashboard),
    path('teacher-dashboard/', teacher_dashboard),
    path('teachers/', teacher_list),
    path('add-teacher/', add_teacher),
    path('delete-teacher/<int:teacher_id>/', delete_teacher),
    path('edit-teacher/<int:teacher_id>/', edit_teacher),

    path('show-report/<int:quiz_id>/', show_report),

    path('student-dashboard/', student_dashboard),
    path('students/', student_list),
    path('add-student/', add_student),
    path('delete-student/<int:student_id>/', delete_student),
    path('edit-student/<int:student_id>/', edit_student),

    path('create-quiz/', create_quiz),
    path('review-quiz/<int:quiz_id>/', review_quiz),
    path('list-quiz/', list_quiz),
    path('assign-quiz/', assign_quiz),
    path('attempt-quiz/<int:quiz_id>/', attempt_quiz),
]