"""
Synthetic Data Generator for Tattle Tale Analytics Dashboard
=============================================================
Generates realistic synthetic datasets for the art community platform.
"""

import random
from datetime import datetime, timedelta
from collections import OrderedDict

ART_MEDIUMS = [
    "Painting", "Drawing", "Textiles", "Photography",
    "Mixed Media", "Digital Art", "Sculpture"
]

WORKSHOP_TITLES = [
    "Community Painting Circle", "Beginner Drawing Workshop",
    "Textile Art for Wellbeing", "Youth Creative Studio",
    "Mixed Media Makers", "Digital Art Introduction",
    "Photography Walk", "Family Craft Session"
]

EVENT_TYPES = [
    "Gallery Opening", "Open Studio Night", "Art Walk",
    "Community Mural Project", "Live Painting Session",
    "Artist Talk", "Pop-Up Exhibition", "Art Swap Meet"
]

DISCOVERY_CHANNELS = [
    "Word of Mouth", "Community Partners", "Social Media",
    "Local Events", "School / College Referral", "Website"
]

AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]

CITIES = [
    "London", "Manchester", "Birmingham", "Bristol",
    "Leeds", "Glasgow", "Edinburgh", "Liverpool", "Brighton", "Oxford"
]


def _seed(seed_value=42):
    random.seed(seed_value)


def generate_kpi_summary(seed_value=42):
    _seed(seed_value)
    total_members = random.randint(500, 2500)
    active_members = int(total_members * random.uniform(0.3, 0.5))
    return {
        "total_members": total_members,
        "active_members": active_members,
        "workshops_hosted": random.randint(20, 150),
        "total_events": random.randint(15, 60),
        "survey_responses": random.randint(80, 700),
        "avg_rating": round(random.uniform(4.1, 4.9), 1),
        "community_support_hours": random.randint(300, 2000),
        "member_growth_pct": round(random.uniform(3.5, 12.2), 1),
        "engagement_rate": round(random.uniform(45.0, 68.0), 1),
        "retention_rate": round(random.uniform(62.0, 85.0), 1),
    }


def generate_user_growth(months=12, seed_value=42):
    _seed(seed_value)
    labels, new_members, total_members, inactive, returning = [], [], [], [], []
    base_date = datetime(2025, 6, 1)
    cumulative = random.randint(400, 800)

    for i in range(months):
        dt = base_date + timedelta(days=30 * i)
        labels.append(dt.strftime("%b %Y"))
        month_num = dt.month
        sf = 1.25 if month_num in (3,4,9,10) else (0.85 if month_num in (6,7,12) else 1.0)
        new = int(random.randint(20, 80) * sf)
        low_activity = int(new * random.uniform(0.12, 0.35))
        ret = int(cumulative * random.uniform(0.05, 0.15))
        cumulative += new - low_activity
        new_members.append(new)
        total_members.append(cumulative)
        inactive.append(low_activity)
        returning.append(ret)

    return {
        "labels": labels,
        "new_members": new_members,
        "total_members": total_members,
        "inactive_members": inactive,
        "returning_participants": returning
    }


def generate_workshop_data(count=10, seed_value=42):
    _seed(seed_value)
    workshops = []
    for i in range(count):
        cap = random.choice([10, 12, 15, 20, 25, 30])
        enrolled = random.randint(int(cap * 0.65), cap)
        workshops.append({
            "title": WORKSHOP_TITLES[i % len(WORKSHOP_TITLES)],
            "medium": ART_MEDIUMS[i % len(ART_MEDIUMS)],
            "enrolled": enrolled, "capacity": cap,
            "completion_rate": round(random.uniform(0.70, 0.98), 2),
            "avg_rating": round(random.uniform(4.1, 4.9), 1),
            "free_places_delivered": enrolled,
            "date": (datetime(2025,6,1) + timedelta(days=random.randint(0,365))).strftime("%Y-%m-%d"),
        })
    return workshops


def generate_event_data(count=8, seed_value=42):
    _seed(seed_value)
    events = []
    for i in range(count):
        cap = random.choice([30, 50, 75, 100])
        tickets = random.randint(int(cap * 0.55), cap)
        events.append({
            "name": f"{EVENT_TYPES[i % len(EVENT_TYPES)]} #{i+1}",
            "type": EVENT_TYPES[i % len(EVENT_TYPES)],
            "tickets_distributed": tickets, "capacity": cap,
            "satisfaction": round(random.uniform(3.5, 5.0), 1),
            "date": (datetime(2025,6,1) + timedelta(days=random.randint(0,365))).strftime("%Y-%m-%d"),
            "city": random.choice(CITIES),
        })
    return events


def generate_survey_data(response_count=400, seed_value=42):
    _seed(seed_value)
    discovery = {}
    for _ in range(response_count):
        ch = random.choice(DISCOVERY_CHANNELS)
        discovery[ch] = discovery.get(ch, 0) + 1

    medium_interest = {}
    for _ in range(response_count):
        m = random.choice(ART_MEDIUMS)
        medium_interest[m] = medium_interest.get(m, 0) + 1

    freq_opts = ["Daily", "Several times/week", "Weekly", "Monthly", "Rarely"]
    freq_w = [0.08, 0.18, 0.32, 0.28, 0.14]
    creation_freq = {}
    for _ in range(response_count):
        f = random.choices(freq_opts, weights=freq_w, k=1)[0]
        creation_freq[f] = creation_freq.get(f, 0) + 1

    workshop_interest = {"Definitely": 0, "Probably": 0, "Maybe": 0, "Unlikely": 0}
    wk_w = [0.35, 0.30, 0.25, 0.10]
    for _ in range(response_count):
        w = random.choices(list(workshop_interest.keys()), weights=wk_w, k=1)[0]
        workshop_interest[w] += 1

    ratings = [random.choices([1,2,3,4,5], weights=[.02,.05,.13,.38,.42], k=1)[0]
               for _ in range(response_count)]

    age_dist = {}
    age_w = [0.15, 0.28, 0.22, 0.18, 0.12, 0.05]
    for _ in range(response_count):
        a = random.choices(AGE_GROUPS, weights=age_w, k=1)[0]
        age_dist[a] = age_dist.get(a, 0) + 1

    city_dist = {}
    for _ in range(response_count):
        c = random.choice(CITIES)
        city_dist[c] = city_dist.get(c, 0) + 1

    experience_levels = {"Beginner": 0, "Intermediate": 0, "Advanced": 0}
    exp_w = [0.65, 0.25, 0.10]
    for _ in range(response_count):
        e = random.choices(list(experience_levels.keys()), weights=exp_w, k=1)[0]
        experience_levels[e] += 1

    return {
        "discovery_channels": OrderedDict(sorted(discovery.items(), key=lambda x: x[1], reverse=True)),
        "medium_interest": OrderedDict(sorted(medium_interest.items(), key=lambda x: x[1], reverse=True)),
        "creation_frequency": creation_freq,
        "workshop_interest": workshop_interest,
        "experience_ratings": ratings,
        "age_distribution": age_dist,
        "city_distribution": OrderedDict(sorted(city_dist.items(), key=lambda x: x[1], reverse=True)),
        "experience_levels": experience_levels,
    }


def generate_engagement_timeseries(days=90, seed_value=42):
    _seed(seed_value)
    dates, page_views, interactions, unique_visitors = [], [], [], []
    start = datetime.now() - timedelta(days=days)
    for i in range(days):
        dt = start + timedelta(days=i)
        dates.append(dt.strftime("%Y-%m-%d"))
        is_wknd = dt.weekday() >= 5
        pv = random.randint(250, 550) if is_wknd else random.randint(150, 350)
        page_views.append(pv)
        interactions.append(int(pv * random.uniform(0.25, 0.45)))
        unique_visitors.append(int(pv * random.uniform(0.55, 0.75)))
    return {"dates": dates, "page_views": page_views,
            "interactions": interactions, "unique_visitors": unique_visitors}


def generate_community_support_data(months=12, seed_value=42):
    _seed(seed_value)
    labels, vh, dm, gs, ps, os, total = [], [], [], [], [], [], []
    base_date = datetime(2025, 6, 1)
    for i in range(months):
        dt = base_date + timedelta(days=30 * i)
        labels.append(dt.strftime("%b %Y"))
        v = round(random.uniform(100, 300), 1)  # Volunteer Hours
        d = round(random.uniform(30, 80), 1)   # Donated Materials (units)
        g = round(random.uniform(5, 15), 1)    # Grant-Supported Sessions
        p = round(random.uniform(20, 60), 1)   # Partner Support Units
        o = round(random.uniform(15, 40), 1)   # Outreach Support
        vh.append(v); dm.append(d); gs.append(g); ps.append(p); os.append(o)
        total.append(round(v+d+g+p+o, 1))
    return {"labels": labels, "volunteer_hours": vh, "donated_materials": dm,
            "grant_sessions": gs, "partner_support": ps, "outreach_support": os, "total": total}


def generate_content_performance(seed_value=42):
    _seed(seed_value)
    pages = ["Home", "About Lana", "Turtle Tales Story", "Workshop Chapters",
             "Event Booking", "Community Survey", "FAQ", "Privacy Policy"]
    results = []
    for page in pages:
        views = random.randint(500, 8000)
        results.append({
            "page": page, "views": views,
            "avg_time_sec": random.randint(15, 280),
            "bounce_rate": round(random.uniform(18.0, 72.0), 1),
            "conversions": random.randint(5, max(6, int(views * 0.08))),
        })
    results.sort(key=lambda x: x["views"], reverse=True)
    return results


def get_all_dashboard_data(seed_value=42):
    return {
        "kpis": generate_kpi_summary(seed_value),
        "user_growth": generate_user_growth(seed_value=seed_value),
        "workshops": generate_workshop_data(seed_value=seed_value),
        "events": generate_event_data(seed_value=seed_value),
        "surveys": generate_survey_data(seed_value=seed_value),
        "engagement": generate_engagement_timeseries(seed_value=seed_value),
        "community_support": generate_community_support_data(seed_value=seed_value),
        "content_performance": generate_content_performance(seed_value=seed_value),
    }
