"""
HackTeam AI — Matching Engine
Weighted scoring:
  Skill complementarity : 30%
  Domain interest overlap: 20%
  Role balance          : 20%
  Experience compat.    : 10%
  Availability          : 10%
  Communication pref.   : 10%
"""

PROFICIENCY_WEIGHT = {'beginner': 1, 'intermediate': 2, 'advanced': 3, 'expert': 4}

COMPLEMENTARY_ROLES = {
    'frontend': ['backend', 'uiux', 'ml', 'devops'],
    'backend':  ['frontend', 'uiux', 'devops', 'data'],
    'ml':       ['frontend', 'backend', 'data', 'presenter'],
    'uiux':     ['frontend', 'backend', 'ml'],
    'devops':   ['backend', 'frontend', 'cybersecurity'],
    'data':     ['ml', 'backend', 'presenter'],
    'presenter':['ml', 'frontend', 'backend', 'data'],
    'blockchain':['backend', 'frontend', 'cybersecurity'],
    'mobile':   ['uiux', 'backend', 'frontend'],
    'cybersecurity': ['backend', 'devops', 'blockchain'],
    'fullstack':['ml', 'uiux', 'data', 'presenter'],
    'other':    [],
}

SKILL_ROLE_MAP = {
    'frontend': ['React', 'Vue', 'HTML', 'CSS', 'JavaScript', 'TypeScript', 'Angular', 'Tailwind'],
    'backend':  ['Python', 'Django', 'Flask', 'Node.js', 'Java', 'Spring', 'FastAPI', 'PostgreSQL', 'MySQL'],
    'ml':       ['Python', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy', 'Keras', 'OpenCV'],
    'uiux':     ['Figma', 'Adobe XD', 'Sketch', 'Canva', 'Prototyping', 'Wireframing'],
    'devops':   ['Docker', 'Kubernetes', 'AWS', 'GCP', 'Azure', 'CI/CD', 'Linux', 'Bash'],
    'data':     ['SQL', 'Pandas', 'Tableau', 'Power BI', 'Excel', 'R', 'NumPy'],
    'blockchain':['Solidity', 'Web3.js', 'Ethereum', 'Hardhat', 'Smart Contracts'],
    'mobile':   ['Flutter', 'React Native', 'Swift', 'Kotlin', 'Android', 'iOS'],
    'cybersecurity': ['Kali Linux', 'Metasploit', 'Wireshark', 'Penetration Testing', 'CTF'],
    'presenter': ['Public Speaking', 'PowerPoint', 'Business Analysis', 'Market Research'],
}

LEARNING_PATHS = {
    'frontend': [
        {'skill': 'HTML/CSS', 'level': 'beginner', 'resource': 'freeCodeCamp.org'},
        {'skill': 'JavaScript', 'level': 'beginner', 'resource': 'javascript.info'},
        {'skill': 'React', 'level': 'intermediate', 'resource': 'react.dev'},
        {'skill': 'TypeScript', 'level': 'intermediate', 'resource': 'typescriptlang.org'},
    ],
    'backend': [
        {'skill': 'Python', 'level': 'beginner', 'resource': 'python.org'},
        {'skill': 'Django/Flask', 'level': 'intermediate', 'resource': 'djangoproject.com'},
        {'skill': 'SQL / PostgreSQL', 'level': 'intermediate', 'resource': 'postgresqltutorial.com'},
        {'skill': 'REST APIs', 'level': 'intermediate', 'resource': 'restfulapi.net'},
        {'skill': 'Docker', 'level': 'advanced', 'resource': 'docs.docker.com'},
    ],
    'ml': [
        {'skill': 'Python + NumPy/Pandas', 'level': 'beginner', 'resource': 'kaggle.com/learn'},
        {'skill': 'Scikit-learn', 'level': 'intermediate', 'resource': 'scikit-learn.org'},
        {'skill': 'Deep Learning (PyTorch)', 'level': 'advanced', 'resource': 'fast.ai'},
        {'skill': 'MLOps basics', 'level': 'advanced', 'resource': 'mlops.community'},
    ],
    'uiux': [
        {'skill': 'Design Principles', 'level': 'beginner', 'resource': 'nngroup.com'},
        {'skill': 'Figma', 'level': 'beginner', 'resource': 'figma.com/learn'},
        {'skill': 'Prototyping', 'level': 'intermediate', 'resource': 'uxdesign.cc'},
    ],
    'devops': [
        {'skill': 'Linux & Bash', 'level': 'beginner', 'resource': 'linuxcommand.org'},
        {'skill': 'Git & GitHub', 'level': 'beginner', 'resource': 'learngitbranching.js.org'},
        {'skill': 'Docker', 'level': 'intermediate', 'resource': 'docs.docker.com'},
        {'skill': 'CI/CD (GitHub Actions)', 'level': 'intermediate', 'resource': 'docs.github.com'},
        {'skill': 'Kubernetes', 'level': 'advanced', 'resource': 'kubernetes.io/docs'},
    ],
}


def compute_match_score(profile_a, profile_b):
    """Return a dict with component scores and explanation strings."""
    result = {
        'total': 0,
        'skill_score': 0,
        'domain_score': 0,
        'role_score': 0,
        'experience_score': 0,
        'availability_score': 0,
        'collab_score': 0,
        'reasons': [],
        'warnings': [],
    }

    # ── 1. Skill complementarity (30 pts) ──────────────────────────────────
    skills_a = set(s.skill.name for s in profile_a.student_skills.select_related('skill').all())
    skills_b = set(s.skill.name for s in profile_b.student_skills.select_related('skill').all())
    overlap = skills_a & skills_b
    unique_b = skills_b - skills_a  # skills B has that A lacks

    if skills_b:
        complementary_ratio = len(unique_b) / len(skills_b)
    else:
        complementary_ratio = 0

    skill_score = min(30, complementary_ratio * 30 + (5 if overlap else 0))
    result['skill_score'] = round(skill_score, 1)
    if unique_b:
        result['reasons'].append(f"Brings {len(unique_b)} complementary skill(s): {', '.join(list(unique_b)[:3])}")
    if len(overlap) > 3:
        result['warnings'].append(f"High skill overlap ({len(overlap)} shared skills)")

    # ── 2. Domain interest overlap (20 pts) ────────────────────────────────
    domains_a = set(i.domain.slug for i in profile_a.interests.select_related('domain').all())
    domains_b = set(i.domain.slug for i in profile_b.interests.select_related('domain').all())
    common_domains = domains_a & domains_b
    if domains_a or domains_b:
        domain_score = (len(common_domains) / max(len(domains_a | domains_b), 1)) * 20
    else:
        domain_score = 0
    result['domain_score'] = round(domain_score, 1)
    if common_domains:
        result['reasons'].append(f"Shares interest in: {', '.join(list(common_domains)[:3])}")

    # ── 3. Role balance (20 pts) ────────────────────────────────────────────
    role_a = profile_a.preferred_role
    role_b = profile_b.preferred_role
    complementary = COMPLEMENTARY_ROLES.get(role_a, [])
    if role_b in complementary:
        role_score = 20
        result['reasons'].append(f"{role_b.title()} role complements your {role_a.title()} role perfectly")
    elif role_a != role_b:
        role_score = 10
        result['reasons'].append(f"Different roles: {role_a} + {role_b} = good balance")
    else:
        role_score = 0
        result['warnings'].append(f"Same role ({role_a}) — may create redundancy")
    result['role_score'] = role_score

    # ── 4. Experience compatibility (10 pts) ───────────────────────────────
    hacks_a = profile_a.hackathons_participated
    hacks_b = profile_b.hackathons_participated
    diff = abs(hacks_a - hacks_b)
    exp_score = max(0, 10 - diff * 2)
    result['experience_score'] = round(exp_score, 1)
    if diff <= 1:
        result['reasons'].append("Similar hackathon experience level")

    # ── 5. Availability (10 pts) ────────────────────────────────────────────
    avail_map = {'available': 10, 'open': 8, 'busy': 3, 'not_available': 0}
    avail_score = avail_map.get(profile_b.availability, 0)
    result['availability_score'] = avail_score
    if avail_score >= 8:
        result['reasons'].append("Currently available for teamwork")
    elif avail_score <= 3:
        result['warnings'].append("May have limited availability")

    # ── 6. Collaboration preference (10 pts) ───────────────────────────────
    size_diff = abs(profile_a.preferred_team_size - profile_b.preferred_team_size)
    collab_score = max(0, 10 - size_diff * 2)
    result['collab_score'] = collab_score

    total = skill_score + domain_score + role_score + exp_score + avail_score + collab_score
    result['total'] = round(min(100, total), 1)
    return result


def get_skill_gaps(profile):
    """Identify missing skills for the student's target role and suggest learning paths."""
    role = profile.preferred_role
    target_skills = set(SKILL_ROLE_MAP.get(role, []))
    current_skills = set(s.skill.name for s in profile.student_skills.select_related('skill').all())
    missing = target_skills - current_skills

    # Also check domain-specific skills
    domain_slugs = set(i.domain.slug for i in profile.interests.select_related('domain').all())
    domain_missing = []
    for slug in domain_slugs:
        if slug in SKILL_ROLE_MAP:
            domain_missing += list(set(SKILL_ROLE_MAP[slug]) - current_skills)

    learning_path = LEARNING_PATHS.get(role, [])
    # Filter to only uncovered steps
    current_lower = {s.lower() for s in current_skills}
    filtered_path = [step for step in learning_path
                     if not any(step['skill'].lower().split('/')[0] in s for s in current_lower)]

    return {
        'role': role,
        'missing_skills': list(missing)[:8],
        'domain_missing': list(set(domain_missing))[:5],
        'learning_path': filtered_path,
        'current_count': len(current_skills),
        'target_count': len(target_skills),
        'completion_pct': round(len(current_skills & target_skills) / max(len(target_skills), 1) * 100),
    }


def get_team_recommendations(my_profile, all_profiles):
    """Suggest a balanced 4-person team for my_profile."""
    IDEAL_ROLES = ['frontend', 'backend', 'ml', 'uiux']
    my_role = my_profile.preferred_role

    # Remove my role from needed
    needed_roles = [r for r in IDEAL_ROLES if r != my_role]

    team = []
    used_users = {my_profile.pk}

    for needed_role in needed_roles:
        candidates = [
            p for p in all_profiles
            if p.preferred_role == needed_role and p.pk not in used_users
        ]
        if not candidates:
            # Fallback: any available person with complementary role
            candidates = [p for p in all_profiles if p.pk not in used_users]

        if candidates:
            # Pick best match
            scored = [(p, compute_match_score(my_profile, p)['total']) for p in candidates]
            scored.sort(key=lambda x: x[1], reverse=True)
            best = scored[0][0]
            team.append({'profile': best, 'score': scored[0][1], 'role': needed_role})
            used_users.add(best.pk)

    missing_roles = [r for r in IDEAL_ROLES if r != my_role and r not in [t['role'] for t in team]]
    return {'team': team, 'missing_roles': missing_roles}
