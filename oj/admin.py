from django.contrib import admin
from django.db.models import fields
from oj.models.problem import Problem
from oj.models.profile import Profile
from oj.models.submission import Submission, SubmissionSource
# from oj.models.organization import Organization, QrganizationJoinRequest
from oj.models.runtime import Language, Judge

# Register your models here.

# class JudgeAdmin(admin.ModelAdmin):


admin.site.register(Problem)
admin.site.register(Profile)
admin.site.register(Language)
admin.site.register(Submission, fields=['user', 'problem', 'language', 'points', 'date', 'time_taken', 'status', 'result','case_points','case_total','current_testcase', 'error','judged_on', 'judged_date'], readonly_fields=['points', 'date', 'time_taken', 'status', 'result','case_points','case_total','current_testcase', 'error','judged_on', 'judged_date'])
admin.site.register(SubmissionSource)
# admin.site.register(Organization)
# admin.site.register(QrganizationJoinRequest)
admin.site.register(Judge, fields=['name', 'created', 'auth_key', 'is_blocked', 'online', 'start_time', 'ping', 'load', 'description', 'last_ip', 'problems'], readonly_fields=['created', 'online', 'start_time', 'ping', 'load', 'last_ip', 'problems'])
