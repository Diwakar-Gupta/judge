from django.core.management.base import BaseCommand

from oj.bridge.daemon import judge_daemon


class Command(BaseCommand):
    def handle(self, *args, **options):
        judge_daemon()
