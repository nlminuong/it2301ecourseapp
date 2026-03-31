import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecourseapisv2.settings')
django.setup()

from django.contrib.auth import get_user_model
from courses.models import Category, Course, Lesson, Tag, Comment

User = get_user_model()

# ===== XÓA DATA CŨ =====
Comment.objects.all().delete()
Lesson.objects.all().delete()
Course.objects.all().delete()
Category.objects.all().delete()
Tag.objects.all().delete()
User.objects.exclude(is_superuser=True).delete()

print("Old data cleared")

# ===== USER =====
users = []
for i in range(5):
    user = User.objects.create_user(
        username=f"user{i+1}",
        password="123456",
        email=f"user{i+1}@gmail.com"
    )
    users.append(user)

print("Created Users")

# ===== CATEGORY =====
category_names = ["Programming", "Design", "Marketing", "Business", "Data"]

categories = []
for name in category_names:
    cat = Category.objects.create(name=name)
    categories.append(cat)

print("Created Categories")

# ===== TAG =====
tag_names = ["Beginner", "Intermediate", "Advanced", "Hot", "New"]

tags = []
for name in tag_names:
    tag = Tag.objects.create(name=name)
    tags.append(tag)

print("Created Tags")

# ===== COURSE + LESSON + COMMENT =====
course_count = 10

for i in range(course_count):
    category = random.choice(categories)

    course = Course.objects.create(
        subject=f"Course {i+1} - {category.name}",
        description=f"This is course {i+1}",
        category=category
    )

    # mỗi course 2 lesson
    for j in range(2):
        lesson = Lesson.objects.create(
            subject=f"Lesson {j+1} of Course {i+1}",
            content="Sample content",
            course=course
        )

        # add random tags
        lesson.tags.add(*random.sample(tags, k=random.randint(1, 3)))

        # ===== COMMENT =====
        for k in range(random.randint(2, 5)):  # mỗi lesson 2-5 comment
            Comment.objects.create(
                user=random.choice(users),
                lesson=lesson,
                content=f"Comment {k+1} on {lesson.subject}"
            )

print("Created Courses, Lessons & Comments")

print("DONE SEED DATA ")