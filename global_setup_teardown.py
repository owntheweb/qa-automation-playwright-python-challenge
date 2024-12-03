from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def global_setup():
    print("Starting global setup...")
    # OPTIONAL: This could be helpful for creating test users and/or other initial data to be referenced
    # locally during tests. The usefulness may be greatly reduced for this QA coding challenge, yet
    # it's here as a starter if it can help.


def global_teardown():
    print("Starting global teardown...")
    # OPTIONAL: Helpful for removing temporary data and other features created in setup