from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Question, QuizControl


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'username',
        'score',
        'current_question',
        'warning_count',
        'is_finished',
        'is_staff'
    )

    fieldsets = UserAdmin.fieldsets + (
        ("Quiz Info", {
            "fields": (
                "score",
                "current_question",
                "warning_count",
                "start_time",
                "end_time",
                "is_finished",
                "session_key",
            )
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Question)
admin.site.register(QuizControl)
