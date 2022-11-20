from django.contrib import admin
# <HINT> Import any new Models here
from .models import Course, Lesson, Instructor, Learner, Choice, Question

# <HINT> Register QuestionInline and ChoiceInline classes here


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']

class QuestionInline(admin.StackedInline):
    model = Question 
    extra = 5

class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('lesson_id', 'question_text', 'grade')

class ChoiceInline(admin.StackedInline):
    model = Choice 
    extra = 5

class ChoiceAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_id', 'choice_text', 'is_correct')

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']


# <HINT> Register Question and Choice models here

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question)
admin.site.register(Choice)
