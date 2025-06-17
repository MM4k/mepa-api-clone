from django.core.management.base import BaseCommand, CommandError

from universities.models import University
from users.models import UniversityUser


class Command(BaseCommand):
    help = "Seed university admin users for development/audit purposes"

    def add_arguments(self, parser):
        parser.add_argument(
            "--password", type=UniversityUser.Type, default="audit", help="Password for the seeded users"
        )
        parser.add_argument("-d", "--delete", action="store_true", help="Delete all existing users before seeding")

    def handle(self, *args, **kwargs):
        password = kwargs["password"]
        delete = kwargs["delete"]

        self.stdout.write("Seeding university admin users...")
        universities = University.objects.all()
        if not universities.exists():
            raise CommandError("No universities found. Please create universities first.")

        if delete:
            self.stdout.write(self.style.WARNING("About to delete all existing users..."))
            confirm = input("Are you sure? [y/N]: ")
            if confirm.lower() == "y":
                count = UniversityUser.objects.count()
                UniversityUser.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f"{count} users deleted successfully"))
            else:
                self.stdout.write("Deletion cancelled")

        created_users = []
        for university in universities:
            email = f"admin@{(university.acronym or 'unknown').lower()}.com"
            UniversityUser.objects.create_superuser(
                university=university,
                type=UniversityUser.Type.UNIVERSITY_ADMIN,
                first_name="Admin",
                last_name="Audit",
                email=email,
                password=password,
                is_seed_user=True,
            )
            created_users.append({"university": university.name, "email": email, "password": password})

        self.stdout.write("─" * 100)
        header = f"{'UNIVERSITY':<55} | {'EMAIL':<20} | PASSWORD"
        self.stdout.write(header)
        self.stdout.write("─" * 100)

        for user in created_users:
            row = f"{user['university']:<55} | {user['email']:<20} | {user['password']}"
            self.stdout.write(row)

        self.stdout.write("─" * 100)
        self.stdout.write(f"{len(created_users)} Users created successfully!")
