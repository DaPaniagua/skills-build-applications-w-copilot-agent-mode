from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

# Sample data
USERS = [
    {"name": "Tony Stark", "email": "tony@marvel.com", "team": "Marvel"},
    {"name": "Steve Rogers", "email": "steve@marvel.com", "team": "Marvel"},
    {"name": "Bruce Wayne", "email": "bruce@dc.com", "team": "DC"},
    {"name": "Clark Kent", "email": "clark@dc.com", "team": "DC"},
]
TEAMS = [
    {"name": "Marvel", "members": ["tony@marvel.com", "steve@marvel.com"]},
    {"name": "DC", "members": ["bruce@dc.com", "clark@dc.com"]},
]
ACTIVITIES = [
    {"user_email": "tony@marvel.com", "activity": "Ironman suit training", "duration": 60},
    {"user_email": "steve@marvel.com", "activity": "Shield practice", "duration": 45},
    {"user_email": "bruce@dc.com", "activity": "Martial arts", "duration": 50},
    {"user_email": "clark@dc.com", "activity": "Flight", "duration": 70},
]
LEADERBOARD = [
    {"team": "Marvel", "points": 105},
    {"team": "DC", "points": 120},
]
WORKOUTS = [
    {"name": "Super Strength", "suggested_for": ["Marvel", "DC"]},
    {"name": "Flight Training", "suggested_for": ["DC"]},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient("mongodb://localhost:27017")
        db = client["octofit_db"]
        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()
        # Create unique index on email for users
        db.users.create_index("email", unique=True)
        # Insert data
        db.users.insert_many(USERS)
        db.teams.insert_many(TEAMS)
        db.activities.insert_many(ACTIVITIES)
        db.leaderboard.insert_many(LEADERBOARD)
        db.workouts.insert_many(WORKOUTS)
        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
