from django.db import models


class Admin(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    standard = models.CharField(max_length=10)
    section = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    teacher_id = models.IntegerField()
    standard = models.CharField(max_length=10)
    section = models.CharField(max_length=10)
    subject = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="draft")

    def __str__(self):
        return self.title
    

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    question = models.TextField()

    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)

    correct_option = models.IntegerField()  # 0–3
    order = models.IntegerField()

    def __str__(self):
        return self.question
    

class QuizAssignment(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    standard = models.CharField(max_length=10)
    section = models.CharField(max_length=10)
    subject = models.CharField(max_length=50)

    assigned_date = models.DateField()

    def __str__(self):
        return f"{self.quiz.title} - {self.standard}{self.section}"
    

class QuizResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    score = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return f"{self.student.name} - {self.quiz.title}"
    

class MStandard(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class MSection(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class MSubject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name