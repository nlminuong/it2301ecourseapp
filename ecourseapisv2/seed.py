import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecourseapisv2.settings')  # sửa lại tên project
django.setup()

from courses.models import Category, Course, Lesson, Tag

# ===== XÓA DATA CŨ (optional) =====
Lesson.objects.all().delete()
Course.objects.all().delete()
Category.objects.all().delete()
Tag.objects.all().delete()

print("Old data cleared")

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

# ===== COURSE + LESSON =====
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

        # add random tags (1-3 tags)
        lesson.tags.add(*random.sample(tags, k=random.randint(1, 3)))

print("Created Courses & Lessons")

print("DONE SEED DATA")