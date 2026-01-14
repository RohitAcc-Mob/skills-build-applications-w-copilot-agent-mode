from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write('Deleting old data...')
            User.objects.all().delete()
            Team.objects.all().delete()
            Activity.objects.all().delete()
            Workout.objects.all().delete()
            Leaderboard.objects.all().delete()

            self.stdout.write('Creating teams...')
            marvel = Team.objects.create(name='Marvel', description='Marvel Superheroes')
            dc = Team.objects.create(name='DC', description='DC Superheroes')

            self.stdout.write('Creating users...')
            users = [
                User(name='Iron Man', email='ironman@marvel.com', team=marvel),
                User(name='Captain America', email='cap@marvel.com', team=marvel),
                User(name='Thor', email='thor@marvel.com', team=marvel),
                User(name='Hulk', email='hulk@marvel.com', team=marvel),
                User(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
                User(name='Superman', email='superman@dc.com', team=dc),
                User(name='Batman', email='batman@dc.com', team=dc),
                User(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
                User(name='Flash', email='flash@dc.com', team=dc),
                User(name='Aquaman', email='aquaman@dc.com', team=dc),
            ]
            for user in users:
                user.save()

            self.stdout.write('Creating activities...')
            Activity.objects.create(user=users[0], type='Running', duration=30, calories=300, date='2026-01-14')
            Activity.objects.create(user=users[5], type='Swimming', duration=45, calories=400, date='2026-01-13')

            self.stdout.write('Creating workouts...')
            workout1 = Workout.objects.create(name='Strength', description='Strength training')
            workout2 = Workout.objects.create(name='Cardio', description='Cardio training')
            workout1.suggested_for.add(users[0], users[1], users[2])
            workout2.suggested_for.add(users[5], users[6], users[7])

            self.stdout.write('Creating leaderboard...')
            Leaderboard.objects.create(team=marvel, points=500)
            Leaderboard.objects.create(team=dc, points=450)

            self.stdout.write(self.style.SUCCESS('Test data populated successfully.'))
