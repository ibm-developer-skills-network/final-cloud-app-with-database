from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice


class ChoiceInline(admin.StackedInline):
    model = Choice


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline, ]


class LessonInline(admin.StackedInline):
    model = Lesson
    inlines = [Question]
    extra = 5


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline, ]


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Choice)
admin.site.register(Question, QuestionAdmin)
