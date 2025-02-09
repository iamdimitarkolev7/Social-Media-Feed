#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django
from django.conf import settings

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.social_media_feed.settings')
    django.setup()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run tests manually from `tst/`
        from django.test.utils import get_runner
        TestRunner = get_runner(settings)
        test_runner = TestRunner()
        failures = test_runner.run_tests(["tst"])  # Explicitly point to `tst/`
        sys.exit(bool(failures))
    else:
     execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
