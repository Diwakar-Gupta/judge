from django.db import models
from oj.models.problem import Problem
from oj.models.profile import Profile
from oj.models.runtime import Judge, Language
from oj.judgeapi import judge_submission

SUBMISSION_RESULT = (
    ('AC', 'Accepted'),
    ('WA', 'Wrong Answer'),
    ('TLE', 'Time Limit Exceeded'),
    ('MLE', 'Memory Limit Exceeded'),
    ('OLE', 'Output Limit Exceeded'),
    ('IR', 'Invalid Return'),
    ('RTE', 'Runtime Error'),
    ('CE', 'Compile Error'),
    ('IE', 'Internal Error'),
    ('SC', 'Short circuit'),
    ('AB', 'Aborted'),
)

class Submission(models.Model):
    USER_DISPLAY_CODE = {
        'AC': 'Accepted',
        'WA': 'Wrong Answer',
        'SC': "Short Circuited",
        'TLE': 'Time Limit Exceeded',
        'MLE': 'Memory Limit Exceeded',
        'OLE': 'Output Limit Exceeded',
        'IR': 'Invalid Return',
        'RTE': 'Runtime Error',
        'CE': 'Compile Error',
        'IE': 'Internal Error (judging server error)',
        'QU': 'Queued',
        'P': 'Processing',
        'G': 'Grading',
        'D': 'Completed',
        'AB': 'Aborted',
    }
    IN_PROGRESS_GRADING_STATUS = ('QU', 'P', 'G')
    RESULT = SUBMISSION_RESULT
    STATUS = (
        ('AC', 'Accepted'),
        ('WA', 'Wrong Answer'),
        ('SC', "Short Circuited"),
        ('TLE', 'Time Limit Exceeded'),
        ('MLE', 'Memory Limit Exceeded'),
        ('OLE', 'Output Limit Exceeded'),
        ('IR', 'Invalid Return'),
        ('RTE', 'Runtime Error'),
        ('CE', 'Compile Error'),
        ('IE', 'Internal Error (judging server error)'),
        ('QU', 'Queued'),
        ('P', 'Processing'),
        ('G', 'Grading'),
        ('D', 'Completed'),
        ('AB', 'Aborted'),
    )

    #STATUS = list(USER_DISPLAY_CODE.keys())
    problem = models.ForeignKey(Problem,related_name="submittion_problem", verbose_name="Problem for this submittion", on_delete=models.CASCADE)
    user = models.ForeignKey(Profile,related_name="submittion_profile", verbose_name="Profile for this submittion", on_delete=models.CASCADE)
    language = models.ForeignKey(Language, related_name="submittion_language", verbose_name="submittion language", on_delete=models.CASCADE)
    points = models.FloatField(verbose_name='points granted', null=True, db_index=True)
    date = models.DateTimeField(verbose_name='submission time', auto_now_add=True, db_index=True)
    time_taken = models.DecimalField("time taken by this code", max_digits=3, decimal_places=2, null=True)
    status = models.CharField(verbose_name='status', max_length=3, choices=STATUS, default='QU')
    result = models.CharField(verbose_name='result', max_length=3, choices=SUBMISSION_RESULT,
                              default=None, null=True, blank=True, db_index=True)
    case_points = models.FloatField(verbose_name='test case points', default=0)
    case_total = models.FloatField(verbose_name='test case total points', default=0)
    current_testcase = models.IntegerField(default=0)
    error = models.TextField(verbose_name='compile errors', null=True, blank=True)
    is_pretested = models.BooleanField(verbose_name='was ran on pretests only', default=False)
    batch = models.BooleanField(verbose_name='batched cases', default=False)
    judged_on = models.ForeignKey(Judge, verbose_name='judged on', null=True, blank=True,
                                  on_delete=models.SET_NULL)
    judged_date = models.DateTimeField(verbose_name='submission judge time', default=None, null=True)
    is_locked = models.BooleanField(default=False)

    def judge(self, *args, **kwargs):
        if not self.is_locked:
            return judge_submission(self, *args, **kwargs)
        return False
    
    def serilize(self):
        data = {
            'result' : self.result,
            'status': self.status,
            'time_taken': self.time_taken,
            'points':self.points,
            'language': self.language.common_name,
            'case_points':self.case_points,
            'current_testcase':self.current_testcase,
            'compile_errors':self.error
        }
        return data

    def update_contest(self):
        pass


class SubmissionSource(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, verbose_name='associated submission',related_name='source')
    source = models.TextField(verbose_name='source code', max_length=65536)

    def __str__(self):
        return 'Source of %s' % self.submission

class SubmissionTestCase(models.Model):
    RESULT = SUBMISSION_RESULT

    submission = models.ForeignKey(Submission, verbose_name='associated submission',
                                   related_name='test_cases', on_delete=models.CASCADE)
    case = models.IntegerField(verbose_name='test case ID')
    status = models.CharField(max_length=3, verbose_name='status flag', choices=SUBMISSION_RESULT)
    time = models.FloatField(verbose_name='execution time', null=True)
    memory = models.FloatField(verbose_name='memory usage', null=True)
    points = models.FloatField(verbose_name='points granted', null=True)
    total = models.FloatField(verbose_name='points possible', null=True)
    batch = models.IntegerField(verbose_name='batch number', null=True)
    feedback = models.CharField(max_length=50, verbose_name='judging feedback', blank=True)
    extended_feedback = models.TextField(verbose_name='extended judging feedback', blank=True)
    output = models.TextField(verbose_name='program output', blank=True)

    @property
    def long_status(self):
        return Submission.USER_DISPLAY_CODES.get(self.status, '')

    class Meta:
        unique_together = ('submission', 'case')
        verbose_name = ('submission test case')
        verbose_name_plural = ('submission test cases')
