from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def calculate_points(self):
        return 10
        # from judge.models import Problem
        # public_problems = Problem.get_public_problems()
        # data = (
        #     public_problems.filter(submission__user=self, submission__points__isnull=False)
        #                    .annotate(max_points=Max('submission__points')).order_by('-max_points')
        #                    .values_list('max_points', flat=True).filter(max_points__gt=0)
        # )
        # extradata = (
        #     public_problems.filter(submission__user=self, submission__result='AC').values('id').distinct().count()
        # )
        # bonus_function = settings.DMOJ_PP_BONUS_FUNCTION
        # points = sum(data)
        # problems = len(data)
        # entries = min(len(data), len(table))
        # pp = sum(map(mul, table[:entries], data[:entries])) + bonus_function(extradata)
        # if self.points != points or problems != self.problem_count or self.performance_points != pp:
        #     self.points = points
        #     self.problem_count = problems
        #     self.performance_points = pp
        #     self.save(update_fields=['points', 'problem_count', 'performance_points'])
        # return points

