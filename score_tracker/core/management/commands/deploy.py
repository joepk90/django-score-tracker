from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError
from django.conf import settings

# https://docs.djangoproject.com/en/dev/howto/custom-management-commands/
# https://stackoverflow.com/questions/54571411/automatically-run-django-admin-migrate-on-startup
# https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html


def load_db(self,):

    self.stdout.write("Running new migrations")

    try:
        call_command('migrate')

    except DatabaseError as dbe:
        self.stdout.write(
            self.style.ERROR('Could not connect to database')
        )
        # self.stdout.write("Could not connect to database")
        return dbe

    self.stdout.write(
        self.style.SUCCESS('Successfully updated database')
    )


class Command(BaseCommand):
    help = "handle required updates for deployments"

    def handle(self, *args, **options):

        # TODO create alternative step for deployment updates
        # - during CI/CD, run application in alternative deployment environment
        # - within this environment run databae migrations (lock the whole database if possible)
        # - don't deploy this image
        # OR...
        #  create a separate cloud run container specifically for deployments (DB access/host access)
        if settings.ENVIRONMENT != 'PROD':
            print("Environment is not PROD, setup steps ignored")
            self.stdout.write(
                "Environment is not PROD, deployment setup steps ignored")

            raise CommandError(
                'Environment is not PROD, deployment setup steps ignored')
        load_db(self)
