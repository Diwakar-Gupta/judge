from django.db import models
from oj.models.profile import Profile
from oj.models.problem import Problem
from oj.models.submission import Submission


class Course_Ordered_Problem(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    index = models.IntegerField(default=100)
    is_public = models.BooleanField(default=False)

    def detail(self, forlist=False):
        data = {
            'name': self.problem.name,
            'code': self.problem.code
        }
        return data


class Course_Sub_Topics(models.Model):
    name = models.CharField(max_length=30, unique=True)
    problems = models.ManyToManyField(Course_Ordered_Problem)

    def __str__(self) -> str:
        return self.name

    def detail(self, forlist=False):
        data = {'name': self.name, 'id': self.id}
        
        if forlist:
            return data
            
        data['problems'] = [p.detail(forlist=True) for p in self.problems.all()]

        return data


class Course_Topics(models.Model):
    name = models.CharField(max_length=30, unique=True)
    subtopics = models.ManyToManyField(Course_Sub_Topics, blank=True)

    def __str__(self) -> str:
        return self.name
    
    def detail(self, forlist=False):
        data = {
            'name':self.name,
            'id': self.id,
        }

        data['subtopics'] = [cst.detail(forlist=True) for cst in self.subtopics.all()]
        return data

class Course(models.Model):
    name = models.CharField(max_length=30, unique=True)
    organizers = models.ManyToManyField(
        Profile, help_text='These people will be able to edit the contest')
    description = models.TextField(help_text='Course Description', blank=True)
    is_visible = models.BooleanField(
        default=False, help_text='publicly visible')
    is_private = models.BooleanField(
        default=False, verbose_name='private to specific users')
    private_contestants = models.ManyToManyField(Profile, blank=True, verbose_name='private contestants',
                                                 help_text='If private, only these users may see the contest', related_name='private_contestants+')
    is_locked = models.BooleanField(
        verbose_name='contest lock', default=False, help_text='Prevent submissions for this contest')
    alltopics = models.ManyToManyField(
        Course_Topics, blank=True, help_text='Topic covered in this course')
    # hide_problem_tags = models.BooleanField(verbose_name='hide problem tags')

    def __str__(self) -> str:
        return self.name

    def detail(self, forlist=False):
        desc = {'name': self.name,
                'id': self.id,
                'description': self.description,
                'locked': self.is_locked, }

        if forlist:
            return desc
        
        desc['topics'] = [st.detail(forlist=True) for st in self.alltopics.all()]
        return desc


class Course_Profile(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_index=True)
    scores = models.IntegerField(default=0)


class Course_Submissions(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_index=True)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    profile = models.ForeignKey(Course_Profile, on_delete=models.CASCADE, db_index=True)
