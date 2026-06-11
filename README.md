# ⚡ HackTeam AI

> AI-powered hackathon team-matching platform for college students.
> Find teammates, track competitions, close skill gaps, and win more hackathons.

---

## 🚀 Quick Setup (5 minutes)

### 1. Clone / Download the project

```bash
# If downloaded as zip:
cd hackteam_ai
```

### 2. Create a virtual environment & install dependencies

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Apply database migrations

```bash
python manage.py migrate
```

### 4. Seed the database (25 students, 8 hackathons, 5 teams)

```bash
python manage.py seed_data
```

### 5. Run the development server

```bash
python manage.py runserver
```

### 6. Open in browser

```
http://127.0.0.1:8000/
```

---

## 🔑 Login Credentials

| Role    | Username      | Password      |
|---------|---------------|---------------|
| Admin   | `admin`       | `admin123`    |
| Student | `aryan.sharma`| `hackteam123` |
| Student | `priya.patel` | `hackteam123` |
| Student | `rahul.verma` | `hackteam123` |

All 25 seeded students use password: **hackteam123**

Admin panel: http://127.0.0.1:8000/admin/

---

## 📁 Project Structure

```
hackteam_ai/
│
├── config/               ← Django project settings & URLs
│   ├── settings.py
│   └── urls.py
│
├── accounts/             ← Auth: signup, login, logout
├── profiles/             ← Student profiles, skills, interests
│   └── management/
│       └── commands/
│           └── seed_data.py   ← Seed 25 students + data
│
├── teams/                ← Team creation, membership, invites, connections
├── hackathons/           ← Hackathon listings, applications, bookmarks
├── matching/             ← AI matching engine + skill gap analysis
│   └── engine.py         ← Core algorithm (weighted scoring)
├── messaging/            ← DMs, team chat, notifications
├── analytics/            ← Dashboard, leaderboard
│
├── templates/            ← All HTML templates (Jinja/Django)
│   ├── base.html         ← Sidebar + topbar layout
│   ├── landing.html
│   ├── accounts/
│   ├── profiles/
│   ├── teams/
│   ├── hackathons/
│   ├── matching/
│   ├── messaging/
│   └── analytics/
│
├── static/
│   ├── css/main.css      ← Full custom design system
│   └── js/main.js        ← Interactions, animations, chat UX
│
├── media/                ← Uploaded avatars / hackathon images
├── manage.py
└── requirements.txt
```

---

## 🎯 Features

| Feature | Status |
|---------|--------|
| Student signup & login | ✅ |
| Profile with skills, roles, domains | ✅ |
| AI team matching (weighted scoring) | ✅ |
| Skill gap analysis + learning paths | ✅ |
| Suggested 4-person balanced team | ✅ |
| Student discovery with filters | ✅ |
| Team create / join / leave | ✅ |
| Team invites (send / accept / reject) | ✅ |
| Connection requests | ✅ |
| Direct messaging | ✅ |
| Team chat room | ✅ |
| Notifications | ✅ |
| Hackathon listings | ✅ |
| Apply with team | ✅ |
| Bookmark hackathons | ✅ |
| Analytics dashboard | ✅ |
| Skill distribution chart | ✅ |
| Participation leaderboard | ✅ |
| Admin panel | ✅ |
| 25 seeded student profiles | ✅ |
| 8 seeded hackathons | ✅ |
| 5 seeded teams | ✅ |
| Dark/light mode (CSS ready) | 🔜 |
| Email notifications | 🔜 |

---

## 🧠 Matching Algorithm

Located in `matching/engine.py`. Weighted scoring:

| Component | Weight | Logic |
|-----------|--------|-------|
| Skill Complementarity | 30% | Skills B has that A lacks / total |
| Domain Interest Overlap | 20% | Jaccard similarity of domain sets |
| Role Balance | 20% | Complementary role map lookup |
| Experience Compatibility | 10% | Hackathon count proximity |
| Availability | 10% | Status: available=10, open=8, busy=3 |
| Collaboration Preference | 10% | Preferred team size alignment |

**Total score: 0–100.**

---

## 🗄️ Database Models

- `User` (Django built-in)
- `StudentProfile` — full student data + stats
- `Skill` + `StudentSkill` — skills with proficiency levels
- `InterestDomain` + `StudentInterest` — domains of interest
- `Team` + `TeamMembership` — team management
- `TeamInvite` — invite flow
- `ConnectionRequest` — peer connections
- `Hackathon` — competition listings
- `HackathonApplication` — team applications
- `HackathonBookmark` — saved hackathons
- `Message` — DMs + team chat
- `Notification` — all notification types
- `MatchScore` — cached match scores
- `ParticipationRecord` — event log

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+ / Django 4.2 |
| Database | SQLite (dev) → PostgreSQL (prod) |
| Frontend | HTML5 + Bootstrap 5.3 + Custom CSS |
| Charts | Chart.js 4.4 |
| Forms | django-crispy-forms + crispy-bootstrap5 |
| Icons | Bootstrap Icons |
| Fonts | Inter (Google Fonts) |

---

## 🗺️ Pages

| URL | Page |
|-----|------|
| `/` | Landing page |
| `/accounts/signup/` | Sign up |
| `/accounts/login/` | Login |
| `/dashboard/` | Student dashboard |
| `/profiles/` | Discover students |
| `/profiles/<pk>/` | Student profile |
| `/profiles/edit/` | Edit your profile |
| `/matching/` | AI teammate recommendations |
| `/matching/detail/<pk>/` | Full match analysis |
| `/teams/` | Browse teams |
| `/teams/create/` | Create team |
| `/teams/<pk>/` | Team detail + chat |
| `/teams/invites/` | Your pending invites |
| `/hackathons/` | Hackathon listings |
| `/hackathons/<pk>/` | Hackathon detail + apply |
| `/messages/` | DM inbox |
| `/messages/<user_pk>/` | Conversation |
| `/messages/team/<team_pk>/` | Team chat |
| `/messages/notifications/` | Notifications |
| `/dashboard/leaderboard/` | Student leaderboard |
| `/admin/` | Django admin panel |

---

## ⚙️ Migrating to PostgreSQL

1. Install psycopg2: `pip install psycopg2-binary`
2. Update `DATABASES` in `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hackteam_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
3. `python manage.py migrate`
4. `python manage.py seed_data`

---

## 🔮 Future Improvements

- [ ] WebSocket real-time chat (Django Channels)
- [ ] Email verification on signup
- [ ] OAuth (Google / GitHub login)
- [ ] AI chatbot for team recommendations
- [ ] Export team as PDF / shareable link
- [ ] GitHub repo integration on profile
- [ ] PWA / mobile app
- [ ] Slack / Discord notifications
- [ ] Public hackathon API
- [ ] Advanced leaderboard with badges

---

## 📄 License

MIT — free for academic, portfolio, and startup use.

Built for hackers, by hackers. ⚡
