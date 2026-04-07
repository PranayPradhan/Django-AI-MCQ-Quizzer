from accounts.models import *


def run():

    # Prevent duplicate creation
    if Teacher.objects.exists():
        return

    # Admin
    Admin.objects.create(
        name="Admin",
        user_id="admin",
        password="admin123"
    )

    # Teacher
    Teacher.objects.create(
        name="Teacher 1",
        user_id="t1",
        password="pass123"
    )

    # Student
    Student.objects.create(
        name="Student 1",
        user_id="s1",
        password="pass123",
        standard="8",
        section="A"
    )

    # Master Tables

    MStandard.objects.bulk_create([
        MStandard(name="6"),
        MStandard(name="7"),
        MStandard(name="8"),
        MStandard(name="9"),
        MStandard(name="10"),
    ])

    MSection.objects.bulk_create([
        MSection(name="A"),
        MSection(name="B"),
        MSection(name="C"),
    ])

    MSubject.objects.bulk_create([
        MSubject(name="English"),
        MSubject(name="Mathematics"),
        MSubject(name="Physics"),
        MSubject(name="Chemistry"),
        MSubject(name="Biology"),
    ])