"""
Management command: python manage.py seed_data
Seeds 25 realistic student profiles, skills, interests, teams, and hackathons.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
import random


SKILLS_POOL = [
    ('Python', 'Programming'), ('JavaScript', 'Programming'), ('React', 'Frontend'),
    ('Vue.js', 'Frontend'), ('Django', 'Backend'), ('Flask', 'Backend'),
    ('Node.js', 'Backend'), ('FastAPI', 'Backend'), ('TypeScript', 'Programming'),
    ('HTML/CSS', 'Frontend'), ('Tailwind CSS', 'Frontend'), ('PostgreSQL', 'Database'),
    ('MySQL', 'Database'), ('MongoDB', 'Database'), ('Redis', 'Database'),
    ('Docker', 'DevOps'), ('Kubernetes', 'DevOps'), ('AWS', 'Cloud'),
    ('GCP', 'Cloud'), ('Git', 'Tools'), ('Linux', 'DevOps'),
    ('TensorFlow', 'AI/ML'), ('PyTorch', 'AI/ML'), ('Scikit-learn', 'AI/ML'),
    ('Pandas', 'Data'), ('NumPy', 'Data'), ('OpenCV', 'AI/ML'),
    ('Figma', 'Design'), ('Adobe XD', 'Design'), ('Sketch', 'Design'),
    ('Flutter', 'Mobile'), ('React Native', 'Mobile'), ('Swift', 'Mobile'),
    ('Kotlin', 'Mobile'), ('Solidity', 'Blockchain'), ('Web3.js', 'Blockchain'),
    ('Rust', 'Systems'), ('C++', 'Systems'), ('Java', 'Programming'),
    ('Spring Boot', 'Backend'), ('SQL', 'Database'), ('Tableau', 'Data'),
    ('R', 'Data'), ('Keras', 'AI/ML'), ('NLTK', 'AI/ML'),
    ('Penetration Testing', 'Security'), ('Wireshark', 'Security'),
    ('Public Speaking', 'Soft Skills'), ('Business Analysis', 'Soft Skills'),
    ('UI Prototyping', 'Design'), ('Wireframing', 'Design'),
]

DOMAINS = [
    ('ai', 'Artificial Intelligence'), ('web', 'Web Development'),
    ('mobile', 'Mobile Apps'), ('cybersecurity', 'Cybersecurity'),
    ('healthtech', 'HealthTech'), ('agritech', 'AgriTech'),
    ('fintech', 'FinTech'), ('edtech', 'EdTech'), ('iot', 'IoT'),
    ('blockchain', 'Blockchain'), ('data', 'Data Science'),
    ('gaming', 'Gaming'), ('sustainability', 'Sustainability'),
    ('social', 'Social Impact'),
]

STUDENTS = [
    # (first, last, role, year, college, branch, skills_subset, domain_slugs, bio)
    ('Aryan', 'Sharma',    'ml',          '3', 'IIT Delhi',         'Computer Science',
     ['Python','TensorFlow','PyTorch','Pandas','NumPy','Scikit-learn','OpenCV'],
     ['ai','data'], "ML researcher passionate about computer vision and NLP."),

    ('Priya', 'Patel',     'frontend',    '2', 'BITS Pilani',       'Computer Science',
     ['React','TypeScript','Tailwind CSS','Figma','HTML/CSS','Vue.js'],
     ['web','edtech'], "Building beautiful, accessible UIs is my superpower."),

    ('Rahul', 'Verma',     'backend',     '4', 'NIT Trichy',        'Information Tech',
     ['Django','PostgreSQL','Docker','Redis','Python','FastAPI','AWS'],
     ['fintech','web'], "Backend dev who loves scalable architecture and clean APIs."),

    ('Sneha', 'Reddy',     'uiux',        '3', 'Manipal University','Design',
     ['Figma','Adobe XD','UI Prototyping','Wireframing','Sketch'],
     ['healthtech','social'], "UX designer focused on human-centred design for social good."),

    ('Karan', 'Mehta',     'fullstack',   '3', 'VIT Vellore',       'Computer Science',
     ['React','Node.js','MongoDB','Python','Docker','JavaScript','Git'],
     ['web','edtech'], "Full-stack dev who ships fast and breaks things less."),

    ('Ananya', 'Singh',    'ml',          '4', 'IIIT Hyderabad',    'CSE',
     ['Python','Keras','NLTK','Pandas','Scikit-learn','TensorFlow'],
     ['ai','healthtech'], "NLP enthusiast building smarter healthcare chatbots."),

    ('Vikram', 'Nair',     'devops',      '4', 'IIT Bombay',        'Computer Science',
     ['Docker','Kubernetes','AWS','Linux','Git','GCP','CI/CD'],
     ['web','sustainability'], "DevOps engineer automating everything. k8s lover."),

    ('Divya', 'Kumar',     'mobile',      '2', 'SRM University',    'IT',
     ['Flutter','Dart','Firebase','React Native','Kotlin'],
     ['mobile','healthtech'], "Building cross-platform apps that users love."),

    ('Aditya', 'Joshi',    'blockchain',  '3', 'IIT Kharagpur',     'Computer Science',
     ['Solidity','Web3.js','Python','JavaScript','Ethereum'],
     ['blockchain','fintech'], "Web3 dev exploring decentralised finance and NFTs."),

    ('Meera', 'Iyer',      'data',        '3', 'IISc Bangalore',    'Data Science',
     ['Python','R','Tableau','SQL','Pandas','NumPy'],
     ['data','agritech'], "Data scientist turning raw numbers into real insights."),

    ('Rohan', 'Gupta',     'backend',     '2', 'NIT Warangal',      'CSE',
     ['Java','Spring Boot','MySQL','Docker','AWS','Git'],
     ['fintech','web'], "Java backend dev, microservices enthusiast."),

    ('Pooja', 'Desai',     'presenter',   '4', 'IIM Ahmedabad',     'Business',
     ['Public Speaking','Business Analysis','PowerPoint','Market Research'],
     ['fintech','social'], "Bridging tech and business for impactful pitches."),

    ('Siddharth', 'Rao',   'cybersecurity','3','IIT Madras',        'CSE',
     ['Penetration Testing','Wireshark','Linux','Python','Kali Linux'],
     ['cybersecurity','web'], "Ethical hacker and CTF addict."),

    ('Tanvi', 'Shah',      'frontend',    '1', 'BITS Goa',          'CSE',
     ['React','HTML/CSS','JavaScript','Tailwind CSS'],
     ['web','edtech'], "First-year dev on a mission to build cool web stuff."),

    ('Nikhil', 'Malhotra', 'ml',          '3', 'IIT Roorkee',       'CSE',
     ['Python','PyTorch','OpenCV','NumPy','C++'],
     ['ai','gaming'], "Computer vision researcher, robotics hobbyist."),

    ('Kavya', 'Nambiar',   'mobile',      '4', 'Amrita University', 'ECE',
     ['Swift','iOS','React Native','Firebase','Flutter'],
     ['mobile','healthtech'], "iOS developer building apps for accessibility."),

    ('Abhishek', 'Tiwari', 'fullstack',   '3', 'PESIT Bangalore',   'CSE',
     ['Vue.js','Flask','MongoDB','JavaScript','Docker'],
     ['agritech','sustainability'], "Full-stack dev passionate about agritech solutions."),

    ('Shruti', 'Bose',     'uiux',        '2', 'NID Ahmedabad',     'UX Design',
     ['Figma','Adobe XD','Wireframing','UI Prototyping'],
     ['social','edtech'], "Designing inclusive experiences for Bharat."),

    ('Varun', 'Kapoor',    'backend',     '4', 'IIT Guwahati',      'CSE',
     ['Python','FastAPI','PostgreSQL','Redis','AWS','Docker'],
     ['fintech','web'], "Building high-performance APIs and distributed systems."),

    ('Nisha', 'Pillai',    'data',        '3', 'IITM Pravartak',    'Data Science',
     ['Pandas','Tableau','SQL','Python','R','Power BI'],
     ['data','healthtech'], "Data analyst turning healthcare data into life-saving insights."),

    ('Harsh', 'Agarwal',   'devops',      '3', 'IIIT Bangalore',    'CSE',
     ['Kubernetes','Docker','AWS','Terraform','Linux','CI/CD'],
     ['web','sustainability'], "Infrastructure nerd automating cloud deployments."),

    ('Sakshi', 'Jain',     'frontend',    '2', 'VIT Chennai',       'IT',
     ['React','TypeScript','CSS','Figma','JavaScript'],
     ['web','social'], "React developer building accessible, beautiful web apps."),

    ('Manav', 'Trivedi',   'blockchain',  '4', 'IIT Kanpur',        'CSE',
     ['Solidity','Rust','Web3.js','Ethereum','Python'],
     ['blockchain','fintech'], "Defi builder and Rust enthusiast."),

    ('Ritika', 'Chauhan',  'ml',          '2', 'Delhi University',  'CSE',
     ['Python','Scikit-learn','Pandas','TensorFlow'],
     ['ai','social'], "Learning ML to build smarter social-impact tools."),

    ('Arnav', 'Sethi',     'presenter',   '3', 'IIT Delhi',         'Dual Degree',
     ['Public Speaking','Business Analysis','Python','SQL'],
     ['fintech','sustainability'], "Tech-biz hybrid. Loves pitching ideas on stage."),
]

HACKATHONS = [
    {
        'title': 'Smart India Hackathon 2024',
        'organizer': 'Ministry of Education, GoI',
        'description': 'India\'s biggest hackathon for college students to solve real government and industry problems. Participate in 5 tracks: Software, Hardware, Innovation, Robotics & Drones, and Smart Automation.',
        'domain': 'ai', 'mode': 'offline', 'status': 'upcoming',
        'start_date': date.today() + timedelta(days=45),
        'end_date': date.today() + timedelta(days=47),
        'registration_deadline': date.today() + timedelta(days=20),
        'min_team_size': 2, 'max_team_size': 6,
        'eligibility': 'All UG/PG students of recognised institutes',
        'prize_pool': '₹1,00,000', 'is_featured': True,
        'tags': 'government,innovation,india,interdisciplinary',
    },
    {
        'title': 'HackWithInfy 2024',
        'organizer': 'Infosys',
        'description': 'A national-level hackathon by Infosys for engineering students. Solve business and technology challenges across tracks: FinTech, HealthTech, EdTech, and Sustainability.',
        'domain': 'fintech', 'mode': 'hybrid', 'status': 'upcoming',
        'start_date': date.today() + timedelta(days=30),
        'end_date': date.today() + timedelta(days=32),
        'registration_deadline': date.today() + timedelta(days=15),
        'min_team_size': 3, 'max_team_size': 5,
        'eligibility': 'B.E/B.Tech students (2025/2026 batch)',
        'prize_pool': '₹3,00,000 + PPO', 'is_featured': True,
        'tags': 'infosys,fintech,healthtech,ppo',
    },
    {
        'title': 'MLH Global Hack Week',
        'organizer': 'Major League Hacking',
        'description': 'A week-long global virtual hackathon. Build anything you want with unlimited resources, mentors, and workshops. Open to all skill levels worldwide.',
        'domain': 'web', 'mode': 'online', 'status': 'upcoming',
        'start_date': date.today() + timedelta(days=10),
        'end_date': date.today() + timedelta(days=17),
        'registration_deadline': date.today() + timedelta(days=8),
        'min_team_size': 1, 'max_team_size': 4,
        'eligibility': 'Open to all students worldwide',
        'prize_pool': '$10,000 + Swag', 'is_featured': True,
        'tags': 'mlh,global,online,beginner-friendly',
    },
    {
        'title': 'IITB TechFest HacX',
        'organizer': 'IIT Bombay',
        'description': 'Premier 36-hour hackathon hosted during IIT Bombay\'s annual technical festival. Tracks: AI/ML, Web3, Healthcare, Climate Tech, and Open Innovation.',
        'domain': 'ai', 'mode': 'offline', 'status': 'upcoming',
        'start_date': date.today() + timedelta(days=60),
        'end_date': date.today() + timedelta(days=62),
        'registration_deadline': date.today() + timedelta(days=40),
        'min_team_size': 3, 'max_team_size': 5,
        'eligibility': 'UG/PG students from any college',
        'prize_pool': '₹2,50,000', 'is_featured': False,
        'tags': 'iitb,ai,web3,climate',
    },
    {
        'title': 'DevPost Impact Hackathon',
        'organizer': 'DevPost',
        'description': 'Build technology for social impact. Create solutions for climate change, education, healthcare access, and poverty reduction. Cash prizes and startup mentorship for winners.',
        'domain': 'social', 'mode': 'online', 'status': 'ongoing',
        'start_date': date.today() - timedelta(days=5),
        'end_date': date.today() + timedelta(days=9),
        'registration_deadline': date.today() + timedelta(days=2),
        'min_team_size': 1, 'max_team_size': 5,
        'eligibility': 'Open to everyone globally',
        'prize_pool': '$25,000', 'is_featured': True,
        'tags': 'social-impact,climate,education,health,devpost',
    },
    {
        'title': 'Flipkart Grid 6.0',
        'organizer': 'Flipkart',
        'description': 'Flipkart\'s flagship hackathon for engineering students. Solve real e-commerce challenges in areas like supply chain, ML personalization, and customer experience.',
        'domain': 'ai', 'mode': 'hybrid', 'status': 'upcoming',
        'start_date': date.today() + timedelta(days=50),
        'end_date': date.today() + timedelta(days=51),
        'registration_deadline': date.today() + timedelta(days=25),
        'min_team_size': 2, 'max_team_size': 3,
        'eligibility': 'B.E/B.Tech/M.Tech students (2025/2026)',
        'prize_pool': '₹5,00,000 + PPO', 'is_featured': False,
        'tags': 'flipkart,ecommerce,ml,supply-chain',
    },
    {
        'title': 'CipherQuest Cybersec CTF',
        'organizer': 'DRDO x IIT Madras',
        'description': 'Capture the Flag competition focused on cybersecurity. Solve real-world security challenges across forensics, reverse engineering, cryptography, and web exploitation.',
        'domain': 'cybersecurity', 'mode': 'online', 'status': 'upcoming',
        'start_date': date.today() + timedelta(days=14),
        'end_date': date.today() + timedelta(days=15),
        'registration_deadline': date.today() + timedelta(days=10),
        'min_team_size': 1, 'max_team_size': 4,
        'eligibility': 'Open to all college students',
        'prize_pool': '₹75,000', 'is_featured': False,
        'tags': 'ctf,security,drdo,forensics,crypto',
    },
    {
        'title': 'HackBio 2024',
        'organizer': 'Biocon & NIBMG',
        'description': 'Bioinformatics hackathon for students at the intersection of biology and technology. Challenges in genomics, drug discovery, and healthcare data analysis.',
        'domain': 'healthtech', 'mode': 'hybrid', 'status': 'upcoming',
        'start_date': date.today() + timedelta(days=35),
        'end_date': date.today() + timedelta(days=37),
        'registration_deadline': date.today() + timedelta(days=18),
        'min_team_size': 2, 'max_team_size': 4,
        'eligibility': 'CSE/Biotech/Life Sciences students',
        'prize_pool': '₹1,50,000', 'is_featured': False,
        'tags': 'bioinformatics,genomics,healthtech,biocon',
    },
]

TEAMS_DATA = [
    {
        'name': 'Neural Ninjas',
        'description': 'Building AI-powered solutions for healthcare diagnostics. We combine ML, backend, and UX expertise.',
        'domain_focus': 'ai', 'max_size': 4, 'status': 'active', 'is_open': True,
        'looking_for_roles': 'uiux presenter',
        'leader_idx': 0,  # Aryan
        'member_idxs': [5, 2],  # Ananya, Rahul
    },
    {
        'name': 'FinTech Founders',
        'description': 'Full-stack fintech team building a smart expense tracker with ML-based predictions.',
        'domain_focus': 'fintech', 'max_size': 4, 'status': 'active', 'is_open': True,
        'looking_for_roles': 'ml data',
        'leader_idx': 2,  # Rahul
        'member_idxs': [4, 3],  # Karan, Sneha
    },
    {
        'name': 'GreenCode',
        'description': 'Sustainability-focused team building carbon footprint tracking and environmental impact tools.',
        'domain_focus': 'sustainability', 'max_size': 5, 'status': 'forming', 'is_open': True,
        'looking_for_roles': 'data ml presenter',
        'leader_idx': 6,  # Vikram
        'member_idxs': [16, 19],  # Abhishek, Nisha
    },
    {
        'name': 'Blockchain Bulls',
        'description': 'DeFi team building a decentralised lending protocol on Ethereum with real-time analytics.',
        'domain_focus': 'blockchain', 'max_size': 4, 'status': 'active', 'is_open': False,
        'looking_for_roles': '',
        'leader_idx': 8,  # Aditya
        'member_idxs': [22, 1],  # Manav, Priya
    },
    {
        'name': 'HealthHack',
        'description': 'Cross-platform mobile app for remote patient monitoring and telemedicine in rural India.',
        'domain_focus': 'healthtech', 'max_size': 4, 'status': 'active', 'is_open': True,
        'looking_for_roles': 'backend ml',
        'leader_idx': 7,  # Divya
        'member_idxs': [15, 3],  # Kavya, Sneha
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with realistic test data'

    def handle(self, *args, **options):
        from profiles.models import Skill, InterestDomain, StudentProfile, StudentSkill, StudentInterest
        from teams.models import Team, TeamMembership
        from hackathons.models import Hackathon

        self.stdout.write(self.style.MIGRATE_HEADING('🌱  Seeding HackTeam AI database...'))

        # ── Create superuser ────────────────────────────
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@hackteam.ai', 'admin123')
            self.stdout.write('  ✓ Superuser: admin / admin123')

        # ── Create skills ────────────────────────────────
        skill_objs = {}
        for name, category in SKILLS_POOL:
            skill, _ = Skill.objects.get_or_create(name=name, defaults={'category': category})
            skill_objs[name] = skill
        self.stdout.write(f'  ✓ {len(skill_objs)} skills created')

        # ── Create domains ───────────────────────────────
        domain_objs = {}
        for slug, name in DOMAINS:
            d, _ = InterestDomain.objects.get_or_create(slug=slug, defaults={'name': name})
            domain_objs[slug] = d
        self.stdout.write(f'  ✓ {len(domain_objs)} interest domains created')

        # ── Create students ──────────────────────────────
        profiles = []
        for i, s in enumerate(STUDENTS):
            first, last, role, year, college, branch, skills, domains, bio = s
            username = f"{first.lower()}.{last.lower()}"
            email    = f"{username}@college.edu"

            user, created = User.objects.get_or_create(
                username=username,
                defaults={'first_name': first, 'last_name': last, 'email': email}
            )
            if created:
                user.set_password('hackteam123')
                user.save()

            profile, _ = StudentProfile.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': f"{first} {last}",
                    'college': college,
                    'branch': branch,
                    'year': year,
                    'preferred_role': role,
                    'availability': random.choice(['available', 'available', 'open', 'busy']),
                    'bio': bio,
                    'hackathons_participated': random.randint(0, 8),
                    'teams_participated': random.randint(0, 5),
                    'wins': random.randint(0, 3),
                    'preferred_team_size': random.choice([3, 4, 4, 5]),
                    'github': f"https://github.com/{username}",
                    'linkedin': f"https://linkedin.com/in/{username}",
                    'languages_known': 'English, Hindi',
                    'achievements': f"Top {random.randint(1,10)} at college hackathon. {random.choice(['Winner','Runner-up','Finalist'])} at {random.choice(['InnoHacks','CodeStorm','HackFest'])} 2023.",
                }
            )

            # Skills
            for skill_name in skills:
                if skill_name in skill_objs:
                    proficiency = random.choice(['intermediate', 'intermediate', 'advanced', 'expert', 'beginner'])
                    StudentSkill.objects.get_or_create(
                        student=profile, skill=skill_objs[skill_name],
                        defaults={'proficiency': proficiency, 'years_experience': round(random.uniform(0.5, 4.0), 1)}
                    )

            # Interests
            for j, slug in enumerate(domains):
                if slug in domain_objs:
                    StudentInterest.objects.get_or_create(
                        student=profile, domain=domain_objs[slug],
                        defaults={'is_primary': (j == 0)}
                    )

            profiles.append(profile)

        self.stdout.write(f'  ✓ {len(profiles)} student profiles created')

        # ── Create hackathons ────────────────────────────
        admin_user = User.objects.get(username='admin')
        for h in HACKATHONS:
            Hackathon.objects.get_or_create(
                title=h['title'],
                defaults={**h, 'created_by': admin_user}
            )
        self.stdout.write(f'  ✓ {len(HACKATHONS)} hackathons created')

        # ── Create teams ─────────────────────────────────
        for td in TEAMS_DATA:
            leader_profile = profiles[td['leader_idx']]
            team, created = Team.objects.get_or_create(
                name=td['name'],
                defaults={
                    'description': td['description'],
                    'leader': leader_profile.user,
                    'max_size': td['max_size'],
                    'status': td['status'],
                    'is_open': td['is_open'],
                    'domain_focus': td['domain_focus'],
                    'looking_for_roles': td['looking_for_roles'],
                }
            )
            if created:
                # Add leader
                TeamMembership.objects.get_or_create(
                    team=team, profile=leader_profile,
                    defaults={'role_in_team': leader_profile.preferred_role, 'team_role': 'leader'}
                )
                # Add members
                for midx in td['member_idxs']:
                    if midx < len(profiles):
                        mp = profiles[midx]
                        TeamMembership.objects.get_or_create(
                            team=team, profile=mp,
                            defaults={'role_in_team': mp.preferred_role, 'team_role': 'member'}
                        )

        self.stdout.write(f'  ✓ {len(TEAMS_DATA)} teams created')

        # ── Update participation counts ──────────────────
        for profile in StudentProfile.objects.all():
            profile.teams_participated = profile.team_memberships.filter(is_active=True).count()
            profile.save()

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅  Seed complete! Login credentials:'))
        self.stdout.write('   Admin  → admin / admin123')
        self.stdout.write('   Student → aryan.sharma / hackteam123')
        self.stdout.write('   Student → priya.patel / hackteam123')
        self.stdout.write('   (all 25 students use password: hackteam123)')
