from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError, CommandParser
from models import Category, Post

class Command(BaseCommand):
    help = 'delete all news from database'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('category', type=str)

    def handle(self, *args: Any, **options: Any) -> str | None:
        answer = input('Do you really want to delete all news from category {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('action canceled'))

            try:
                category = Category.get(name=options['category'])
                Post.objects.filter(category=category).delete()
                self.stdout.write('Operation succesfully finished')
            except Post.DoesNotExist:
                self.stdout.write(self.style.ERROR('Could not find category {}'))
