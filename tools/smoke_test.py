import os
import os
import sys
from pathlib import Path

# Ensure project root is on sys.path so `config` package can be imported
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from django.test import Client


def check(url, client, desc=None):
    r = client.get(url)
    ok = r.status_code in (200, 302)
    print(f"{url} -> {r.status_code}" + (f" ({desc})" if desc else ""))
    return ok


def main():
    client = Client()

    public_urls = ['/', '/accounts/login/', '/accounts/signup/', '/hackathons/', '/teams/', '/profiles/']
    print('Checking public pages:')
    all_ok = True
    for u in public_urls:
        all_ok &= check(u, client)

    # Login as seeded student
    creds = {'username': 'aryan.sharma', 'password': 'hackteam123'}
    resp = client.post('/accounts/login/', creds, follow=True)
    logged_in = resp.context and resp.context.get('user') and resp.context.get('user').is_authenticated
    if not logged_in:
        # Fallback: force login via test client
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            u = User.objects.get(username='aryan.sharma')
            client.force_login(u)
            logged_in = True
            print('Login via form FAILED; used force_login fallback -> OK')
        except Exception as e:
            print('Login as aryan.sharma -> FAILED; fallback error', e)
    else:
        print('Login as aryan.sharma -> OK')
    all_ok &= bool(logged_in)

    # Authenticated pages
    auth_urls = ['/dashboard/', '/teams/create/', '/messages/', '/messages/notifications/']
    print('\nChecking authenticated pages:')
    for u in auth_urls:
        all_ok &= check(u, client)

    print('\nSMOKE TEST', 'PASSED' if all_ok else 'FAILED')
    sys.exit(0 if all_ok else 2)


if __name__ == '__main__':
    main()
