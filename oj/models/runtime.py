from django.db import models

class Language(models.Model):
    key = models.CharField(max_length=6, verbose_name='short identifier',
                           help_text='The identifier for this language; the same as its executor id for judges.',
                           unique=True)
    name = models.CharField(max_length=20, verbose_name='long name',help_text='Longer name for the language, e.g. "Python 2" or "C++11".')
    short_name = models.CharField(max_length=10, verbose_name='short name',help_text='''More readable, but short, name to display publicly; e.g. "PY2" or 
                                              "C++11". If left blank, it will default to the short identifier.''',null=True, blank=True)
    common_name = models.CharField(max_length=10, verbose_name='common name',help_text='''Common name for the language. For example, the common name for C++03, 
                                               'C++11, and C++14 would be "C++"''')
    ace = models.CharField(max_length=20, verbose_name='ace mode name',help_text='''Language ID for Ace.js editor highlighting, appended to "mode-" to determine '
                                       'the Ace JavaScript file to use, e.g., "python".''')
    pygments = models.CharField(max_length=20, verbose_name='pygments name',help_text='Language ID for Pygments highlighting in source windows.')
    template = models.TextField(verbose_name='code template', help_text='Code template to display in submission editor.', blank=True)
    info = models.CharField(max_length=50, verbose_name='runtime info override', blank=True,help_text="""Do not set this unless you know what you're doing! It will override the usually more specific, judge-provided runtime info!""")
    description = models.TextField(verbose_name='language description',help_text='''Use this field to inform users of quirks with your environment, '
                                               'additional restrictions, etc.''', blank=True)
    extension = models.CharField(max_length=10, verbose_name='extension',
                                 help_text='The extension of source files, e.g., "py" or "cpp".')

    def __str__(self) -> str:
        return self.name

class RuntimeVersion(models.Model):
    language = models.ForeignKey(Language, verbose_name='language to which this runtime belongs', on_delete=models.CASCADE)
    judge = models.ForeignKey('Judge', verbose_name='judge on which this runtime exists', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, verbose_name='runtime name')
    version = models.CharField(max_length=64, verbose_name='runtime version', blank=True)
    priority = models.IntegerField(verbose_name='order in which to display this runtime', default=0)


class Judge(models.Model):
    name = models.CharField(max_length=50, help_text='Server name, hostname-style', unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='time of creation')
    auth_key = models.CharField(max_length=100, help_text='A key to authenticate this judge',
                                verbose_name='authentication key')
    is_blocked = models.BooleanField(verbose_name='block judge', default=False,
                                     help_text='Whether this judge should be blocked from connecting, '
                                                 'even if its key is correct.')
    online = models.BooleanField(verbose_name='judge online status', default=False)
    start_time = models.DateTimeField(verbose_name='judge start time', null=True)
    ping = models.FloatField(verbose_name='response time', null=True)
    load = models.FloatField(verbose_name='system load', null=True,
                             help_text='Load for the last minute, divided by processors to be fair.')
    description = models.TextField(blank=True, verbose_name='description')
    last_ip = models.GenericIPAddressField(verbose_name='Last connected IP', blank=True, null=True)
    problems = models.ManyToManyField('Problem', verbose_name='problems', related_name='judges')
    runtimes = models.ManyToManyField(Language, verbose_name='judges', related_name='judges')

    def __str__(self) -> str:
        return self.name + ' [' + ('Online' if self.online else 'Offline') + ']'