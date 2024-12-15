from django.core.management.base import BaseCommand
from admin_management.models import Admin
from django.contrib.auth.hashers import make_password
import os
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
    help = 'Creates a default superuser admin'

    def handle(self, *args, **kwargs):
        try:
            username = os.getenv('ADMIN_USERNAME', 'admin')
            password = os.getenv('ADMIN_PASSWORD', 'Admin@1234')
            email = os.getenv('ADMIN_EMAIL', 'admin@example.com')

            hashed_password = make_password(password)

            if not Admin.objects.filter(username=username).exists():
                Admin.objects.create(
                    username=username,
                    password=hashed_password,
                    email=email,
                    is_superuser=True
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created admin user: {username}')
                )
            else:
                admin = Admin.objects.get(username=username)
                admin.password = hashed_password
                admin.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Updated password for admin user: {username}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin user: {str(e)}')
            )