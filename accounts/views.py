from django.shortcuts import render, redirect
from .models import Admin, Teacher, Student
from .models import Quiz, QuizQuestion, QuizAssignment, QuizResult
from .models import MStandard, MSection, MSubject
from datetime import date
from .utils import generate_ai_questions  
import json

# Toggle
# USE_AI = False
USE_AI = True

# Create your views here.
def logout_view(request):
    request.session.flush()
    return redirect("/")

def login_view(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")

        # Loop through TEMP users
        # for user in USERS:
        #     if user["user_id"] == user_id and user["password"] == password:

        #         # Redirect based on role
        #         if user["role"] == "admin":
        #             return redirect("/admin-dashboard/")
        #         elif user["role"] == "teacher":
        #             return redirect("/teacher-dashboard/")
        #         elif user["role"] == "student":
        #             return redirect("/student-dashboard/")

         # Check Admin
        try:
            admin = Admin.objects.get(user_id=user_id, password=password)

            request.session["user_id"] = admin.user_id
            request.session["role"] = "admin"
            request.session["name"] = admin.name

            return redirect("/admin-dashboard/")
        except Admin.DoesNotExist:
            pass

        # Check Teacher
        try:
            teacher = Teacher.objects.get(user_id=user_id, password=password)

            request.session["user_id"] = teacher.id  # type: ignore
            request.session["role"] = "teacher"
            request.session["name"] = teacher.name

            return redirect("/teacher-dashboard/")
        except Teacher.DoesNotExist:
            pass

        # Check Student
        try:
            student = Student.objects.get(user_id=user_id, password=password)

            request.session["user_id"] = student.id         # type: ignore
            request.session["login_id"] = student.user_id   # optional
            request.session["role"] = "student"
            request.session["name"] = student.name
            request.session["standard"] = student.standard
            request.session["section"] = student.section    

            return redirect("/student-dashboard/")
        except Student.DoesNotExist:
            pass

        # Invalid login
        return render(request, "login.html", {"error": "Invalid User ID or Password"})

    return render(request, "login.html")

# admin dashboard view
def admin_dashboard(request):
    
    if request.session.get("role") != "admin":
        return redirect("/")
    
    return render(request, "admin_dashboard.html", {
        "name": request.session.get("name")
    })


# teacher dashboard view
def teacher_dashboard(request):
    if request.session.get("role") != "teacher":
        return redirect("/")

    return render(request, "teacher_dashboard.html", {
        "name": request.session.get("name")
    })


# student dashboard view
def student_dashboard(request):
    if request.session.get("role") != "student":
        return redirect("/")
    
    student_id = request.session.get("user_id")
    student_standard = request.session.get("standard")
    student_section = request.session.get("section")

    assignments = QuizAssignment.objects.filter(
        standard=student_standard,
        section=student_section
    )

    # Get results of this student
    results = QuizResult.objects.filter(student_id=student_id)

    # Map quiz_id → result
    result_map = {
        r.quiz.pk: r for r in results # pk -> id
    }    

    return render(request, "student_dashboard.html", {
        "assignments": assignments,
        "result_map": result_map,
        "today": date.today()
    })


# student_list view
def student_list(request):
    if request.session.get("role") != "admin":
        return redirect("/")

    students = Student.objects.all()

    return render(request, "students.html", {
        "students": students
    })

# teacher list view
def teacher_list(request):
    # Protect route
    if request.session.get("role") != "admin":
        return redirect("/")

    teachers = Teacher.objects.all()

    return render(request, "teachers.html", {
        "teachers": teachers
    })

# add student view
from .models import MStandard, MSection  # ensure this import

def add_student(request):
    if request.session.get("role") != "admin":
        return redirect("/")

    if request.method == "POST":
        name = request.POST.get("name")
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")
        standard = request.POST.get("standard")
        section = request.POST.get("section")

        Student.objects.create(
            name=name,
            user_id=user_id,
            password=password,
            standard=standard,
            section=section
        )

        return redirect("/students/")

    return render(request, "student_form.html", {
        "standards": MStandard.objects.all(),
        "sections": MSection.objects.all()
    })

# add teacher view
def add_teacher(request):
    if request.session.get("role") != "admin":
        return redirect("/")

    if request.method == "POST":

        print("POST HIT")

        name = request.POST.get("name")
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")

        Teacher.objects.create(
            name=name,
            user_id=user_id,
            password=password
        )

        return redirect("/teachers/")

    return render(request, "teacher_form.html")

# delete teacher view
def delete_teacher(request, teacher_id):
    if request.session.get("role") != "admin":
        return redirect("/")

    Teacher.objects.filter(id=teacher_id).delete()
    return redirect("/teachers/")

# edit student view
def edit_student(request, student_id):
    if request.session.get("role") != "admin":
        return redirect("/")

    student = Student.objects.get(id=student_id)

    if request.method == "POST":
        student.name = request.POST.get("name")
        student.user_id = request.POST.get("user_id")
        student.password = request.POST.get("password")
        student.standard = request.POST.get("standard")
        student.section = request.POST.get("section")
        student.save()

        return redirect("/students/")

    return render(request, "student_form.html", {
        "student": student,
        "standards": MStandard.objects.all(),
        "sections": MSection.objects.all()
    })

# delete student view
def delete_student(request, student_id):
    if request.session.get("role") != "admin":
        return redirect("/")

    Student.objects.filter(id=student_id).delete()
    return redirect("/students/")

# edit teacher view
def edit_teacher(request, teacher_id):
    if request.session.get("role") != "admin":
        return redirect("/")

    teacher = Teacher.objects.get(id=teacher_id)

    if request.method == "POST":
        teacher.name = request.POST.get("name")
        teacher.user_id = request.POST.get("user_id")
        teacher.password = request.POST.get("password")
        teacher.save()

        return redirect("/teachers/")

    return render(request, "teacher_form.html", {
        "teacher": teacher
    })


# create_quiz view
def create_quiz(request):
    if request.session.get("role") != "teacher":
        return redirect("/")

    if request.method == "POST":
        title = request.POST.get("title")
        standard = request.POST.get("standard")
        section = request.POST.get("section")
        subject = request.POST.get("subject")
        num_questions = int(request.POST.get("num_questions"))
        content_type = request.POST.get("content_type")
        topic = request.POST.get("topic_content")

        quiz = Quiz.objects.create(
            title=title,
            teacher_id=request.session.get("user_id"),
            standard=standard,
            section=section,
            subject=subject,
            status="draft"
        )

        # Generate Questions
        questions = generate_questions(
            num_questions,
            subject,
            standard,
            content_type,
            topic
        )

        for index, q in enumerate(questions):
            QuizQuestion.objects.create(
                quiz=quiz,
                question=q["question"],
                option_1=q["options"][0],
                option_2=q["options"][1],
                option_3=q["options"][2],
                option_4=q["options"][3],
                correct_option=q["correct_option"],
                order=index + 1
            )

        print("Generated Questions:", questions)

        # return redirect("/teacher-dashboard/")
        return redirect("/list-quiz/")

    return render(request, "create_quiz.html", {
        "standards": MStandard.objects.all(),
        "sections": MSection.objects.all(),
        "subjects": MSubject.objects.all(),
        "name": request.session.get("name")
    })


# generate questions view
def generate_questions(num_questions, subject, standard, content_type, topic):
    
    if not USE_AI:
        # Load from JSON file
        with open("sample_questions.json") as f:
            data = json.load(f)

        questions = data[:num_questions]

        # Fix structure
        formatted = []
        for q in questions:
            formatted.append({
                "question": q["question"],
                "options": q["options"],
                "correct_option": q["correct_option"]
            })

        return formatted

    else:
        # AI FLOW
        return generate_ai_questions(
            num_questions,
            subject,
            standard,
            content_type,
            topic
        )        


# list quiz view
def list_quiz(request):
    if request.session.get("role") != "teacher":
        return redirect("/")

    quizzes = Quiz.objects.all()

    # keep only quizzes that have questions
    filtered_quizzes = []
    for quiz in quizzes:
        if QuizQuestion.objects.filter(quiz=quiz).exists():
            filtered_quizzes.append(quiz)

    return render(request, "list_quiz.html", {
        "quizzes": filtered_quizzes
    })


# review quiz view
def review_quiz(request, quiz_id):
    if request.session.get("role") != "teacher":
        return redirect("/")

    quiz = Quiz.objects.get(id=quiz_id)
    questions = QuizQuestion.objects.filter(quiz=quiz).order_by("order")

    if request.method == "POST":
        for q in questions:
            q.question = request.POST.get(f"question_{q.id}")           # type: ignore 
            q.option_1 = request.POST.get(f"option1_{q.id}")            # type: ignore 
            q.option_2 = request.POST.get(f"option2_{q.id}")            # type: ignore 
            q.option_3 = request.POST.get(f"option3_{q.id}")            # type: ignore 
            q.option_4 = request.POST.get(f"option4_{q.id}")            # type: ignore 
            q.correct_option = int(request.POST.get(f"correct_{q.id}")) # type: ignore 
            q.save()

        quiz.status = "published"
        quiz.save()

        # REDIRECT WITH PARAMETERS
        return redirect(
            f"/assign-quiz/?standard={quiz.standard}&section={quiz.section}&subject={quiz.subject}"
        )
    
    return render(request, "review_quiz.html", {
        "quiz": quiz,
        "questions": questions,
        "name": request.session.get("name")
    })


# assign quiz view
def assign_quiz(request):
    if request.session.get("role") != "teacher":
        return redirect("/")

    # Get dropdown values from master tables
    standards = MStandard.objects.all()
    sections = MSection.objects.all()
    subjects = MSubject.objects.all()

    if request.method == "GET":
        standard = request.GET.get("standard")
        section = request.GET.get("section")
        subject = request.GET.get("subject")

        if standard and section and subject:
            quizzes = Quiz.objects.filter(
                standard=standard,
                section=section,
                subject=subject,
                status="published"
            )

            # Build assignment map
            assignments = QuizAssignment.objects.filter(
                standard=standard,
                section=section,
                subject=subject
            )

            assignment_map = {
                a.quiz_id: a.assigned_date for a in assignments # type: ignore
            }

        else:
            quizzes = None
            assignment_map = {}

        return render(request, "assign_quiz.html", {
            "quizzes": quizzes,
            "assignment_map": assignment_map,
            "standard": standard,
            "section": section,
            "subject": subject,
            "standards": standards,
            "sections": sections,
            "subjects": subjects,
            "name": request.session.get("name")
        })

    if request.method == "POST":
        quiz_id = request.POST.get("quiz_id")
        date = request.POST.get("assigned_date")

        # print("ASSIGNING:", quiz_id, date)   # DEBUG

        existing = QuizAssignment.objects.filter(
            quiz_id=quiz_id,
            standard=request.POST.get("standard"),
            section=request.POST.get("section"),
            subject=request.POST.get("subject")
        ).first()

        if existing:
            existing.assigned_date = date
            existing.save()
        else:
            QuizAssignment.objects.create(
                quiz_id=quiz_id,
                standard=request.POST.get("standard"),
                section=request.POST.get("section"),
                subject=request.POST.get("subject"),
                assigned_date=date
            )

        standard = request.POST.get("standard")
        section = request.POST.get("section")
        subject = request.POST.get("subject")

        # return redirect(f"/assign-quiz/?standard={standard}&section={section}&subject={subject}")

    return redirect("/teacher-dashboard/")


# attempt quiz view
def attempt_quiz(request, quiz_id):
    if request.session.get("role") != "student":
        return redirect("/")

    student_id = request.session.get("user_id")

    # Get student
    student = Student.objects.get(id=student_id)

    # Check assignment (date + eligibility)
    assignment = QuizAssignment.objects.filter(
        quiz_id=quiz_id,
        standard=student.standard,
        section=student.section
    ).first()

    # If not assigned
    if not assignment:
        return redirect("/student-dashboard/")

    # If not today's quiz
    if assignment.assigned_date != date.today():
        return redirect("/student-dashboard/")

    # Prevent reattempt
    already_attempted = QuizResult.objects.filter(
        student=student,
        quiz_id=quiz_id
    ).exists()

    if already_attempted:
        return redirect("/student-dashboard/")

    # Load questions
    questions = QuizQuestion.objects.filter(quiz_id=quiz_id).order_by("order")

    if request.method == "POST":
        score = 0
        total = questions.count()

        for q in questions:
            selected = request.POST.get(f"question_{q.id}") # type: ignore

            if selected is not None and int(selected) == q.correct_option:
                score += 1

        # Save result
        QuizResult.objects.create(
            student=student,
            quiz_id=quiz_id,
            score=score,
            total=total
        )

        return render(request, "quiz_result.html", {
            "score": score,
            "total": total
        })

    return render(request, "attempt_quiz.html", {
        "questions": questions
    })

# master tables view
def master_tables(request):
    if request.session.get("role") != "admin":
        return redirect("/")

    return render(request, "masters.html", {
        "name": request.session.get("name")
    })


# view master data
def view_master(request, master_type):
    if request.session.get("role") != "admin":
        return redirect("/")

    if master_type == "standard":
        data = MStandard.objects.all()
    elif master_type == "section":
        data = MSection.objects.all()
    elif master_type == "subject":
        data = MSubject.objects.all()
    else:
        return redirect("/master-tables/")

    return render(request, "view_master.html", {
        "data": data,
        "type": master_type,
        "name": request.session.get("name")
    })


# add master data
def add_master(request, master_type):
    if request.session.get("role") != "admin":
        return redirect("/")

    if request.method == "POST":
        value = request.POST.get("name")

        if not value:
            return redirect(f"/add-master/{master_type}/")

        if master_type == "standard":
            MStandard.objects.create(name=value)
        elif master_type == "section":
            MSection.objects.create(name=value)
        elif master_type == "subject":
            MSubject.objects.create(name=value)

        return redirect(f"/view-master/{master_type}/")

    return render(request, "master_form.html", {
        "type": master_type,
        "name": request.session.get("name")
    })


# seed master tables 
def seed_master_data(request):
    from .models import MStandard, MSection, MSubject

    # Standards
    for s in ["6", "7", "8", "9", "10"]:
        MStandard.objects.get_or_create(name=s)

    # Sections
    for s in ["A", "B", "C", "D"]:
        MSection.objects.get_or_create(name=s)

    # Subjects
    for s in ["English", "Mathematics", "Physics", "Chemistry", "Biology"]:
        MSubject.objects.get_or_create(name=s)

    return redirect("/master-tables/")
    

# show report view
def show_report(request, quiz_id):
    if request.session.get("role") != "teacher":
        return redirect("/")

    # Get quiz
    quiz = Quiz.objects.get(id=quiz_id)

    # Get assignment (latest or first)
    assignment = QuizAssignment.objects.filter(quiz_id=quiz_id).first()

    assigned_date = assignment.assigned_date if assignment else None

    # Get students for that class + section
    students = Student.objects.filter(
        standard=quiz.standard,
        section=quiz.section
    )

    # Get results
    results = QuizResult.objects.filter(quiz_id=quiz_id)

    # Map student_id → result
    result_map = {
        r.student.id: r for r in results # type: ignore
    }

    return render(request, "show_report.html", {
        "quiz": quiz,
        "assigned_date": assigned_date,
        "students": students,
        "result_map": result_map,
        "name": request.session.get("name")
    })