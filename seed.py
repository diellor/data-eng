import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scraping_app.settings")
django.setup()

from django.contrib.auth.models import User
from etl.services import VikingsShowService, NorsemenShowService, VikingsNFLService
from scraping.services import (
    VikingsShowRawDataService,
    NorsemenShowRawDataService,
    NFLRawDataService,
)


def create_admin_user(username, email, password):

    try:
        admin_user, created = User.objects.update_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )
        admin_user.set_password(password)
        admin_user.save()

        if created:
            print(f"Admin user '{username}' created successfully.")
        else:
            print(f"Admin user '{username}' already exists and has been overwritten.")

    except Exception as e:
        print(f"An error occurred while creating/updating the admin user: {e}")


def run_seed():

    print("Starting the data seeding process...")
    try:
        VikingsShowRawDataService().handle()
        VikingsShowService().handle()
        
        NorsemenShowRawDataService().handle()
        NorsemenShowService().handle()

        NFLRawDataService().handle()
        VikingsNFLService().handle()

        print("Data seeding process completed successfully.")
    except Exception as e:
        print(f"An error occurred during data seeding: {e}")


if __name__ == "__main__":
    admin_username = "test"
    admin_email = "test@example.com"
    admin_password = "testtest"

    print("Creating or updating the admin user...")
    create_admin_user(admin_username, admin_email, admin_password)

    run_seed()
