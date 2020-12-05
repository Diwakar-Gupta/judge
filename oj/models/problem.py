from django.db import models
from oj.models.profile import Profile

class Problem(models.Model):
    code = models.CharField(max_length=20,verbose_name='problem code',help_text='at max 20 characters')
    name = models.CharField(max_length=50,verbose_name='problem name', help_text='at max 20 characters')
    description = models.TextField(verbose_name='problem body')
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING,related_name = 'problemauthor', default=None)
    curators = models.ManyToManyField(Profile, verbose_name='curator', blank=True,related_name = 'problemcurators', help_text='These users will be able to edit the problem, and be listed as authors.')
    contestcount = models.IntegerField(default=0)
    is_public = models.BooleanField(default=True)
    time_limit = models.FloatField(verbose_name='time limit',
                                   help_text='The time limit for this problem, in seconds. '
                                               'Fractional seconds (e.g. 1.5) are supported.')
    memory_limit = models.PositiveIntegerField(verbose_name='memory limit',
                                               help_text='The memory limit for this problem, in kilobytes '
                                                           '(e.g. 64mb = 65536 kilobytes).')
    partial = models.BooleanField(verbose_name='allows partial points', default=False)
    points = models.FloatField(verbose_name='points',
                               help_text='Points awarded for problem completion. '
                                           "Points are displayed with a 'p' suffix if partial.",)

    def update_stats(self):
        pass