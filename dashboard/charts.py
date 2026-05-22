"""
Plotly Chart Factory for Tattle Tale Analytics Dashboard
=========================================================
Generates interactive Plotly chart HTML snippets for embedding
in the Flask dashboard template. All charts use a consistent
dark-themed design language.
"""

import plotly.graph_objects as go
import plotly.io as pio
from collections import Counter

# ---------------------------------------------------------------------------
# Theme Constants
# ---------------------------------------------------------------------------

COLORS = {
    "primary": "#6C63FF",
    "secondary": "#00D9A6",
    "accent": "#FF6B8A",
    "warning": "#FFB74D",
    "info": "#4FC3F7",
    "purple_light": "#A78BFA",
    "bg_dark": "#0F1117",
    "bg_card": "#1A1D2E",
    "bg_surface": "#242738",
    "text_primary": "#E8E8F0",
    "text_secondary": "#9CA3AF",
    "grid": "#2D3148",
}

PALETTE = [
    "#6C63FF", "#00D9A6", "#FF6B8A", "#FFB74D", "#4FC3F7",
    "#A78BFA", "#F472B6", "#34D399", "#FBBF24", "#60A5FA",
]

LAYOUT_DEFAULTS = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, system-ui, sans-serif", color=COLORS["text_primary"], size=13),
    margin=dict(l=50, r=30, t=50, b=50),
    hoverlabel=dict(
        bgcolor=COLORS["bg_card"],
        font_size=13,
        font_family="Inter, system-ui, sans-serif",
        bordercolor=COLORS["primary"],
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text_secondary"], size=11),
    ),
)


def _to_html(fig, chart_id="chart"):
    """Convert a Plotly figure to an embeddable HTML div."""
    return pio.to_html(
        fig, full_html=False, include_plotlyjs=False,
        div_id=chart_id,
        config={"displayModeBar": False, "responsive": True}
    )


# ---------------------------------------------------------------------------
# 1. User Growth Area Chart
# ---------------------------------------------------------------------------

def create_user_growth_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["labels"], y=data["total_members"],
        mode="lines", name="Total Members",
        line=dict(color=COLORS["primary"], width=3),
        fill="tozeroy",
        fillcolor="rgba(108,99,255,0.15)",
    ))
    fig.add_trace(go.Scatter(
        x=data["labels"], y=data["new_members"],
        mode="lines+markers", name="New Members",
        line=dict(color=COLORS["secondary"], width=2, dash="dot"),
        marker=dict(size=6, color=COLORS["secondary"]),
    ))
    fig.add_trace(go.Scatter(
        x=data["labels"], y=data["returning_participants"],
        mode="lines+markers", name="Returning Participants",
        line=dict(color=COLORS["warning"], width=2, dash="dash"),
        marker=dict(size=6, color=COLORS["warning"]),
    ))
    fig.add_trace(go.Bar(
        x=data["labels"], y=data["inactive_members"],
        name="Inactive Members", marker_color=COLORS["accent"],
        opacity=0.6,
    ))
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title=dict(text="Community Growth Over Time", font=dict(size=16)),
        xaxis=dict(gridcolor=COLORS["grid"], showgrid=False),
        yaxis=dict(gridcolor=COLORS["grid"], gridwidth=1),
        barmode="overlay", height=400,
    )
    return _to_html(fig, "user-growth-chart")


# ---------------------------------------------------------------------------
# 2. Workshop Performance Horizontal Bar
# ---------------------------------------------------------------------------

def create_workshop_chart(workshops):
    titles = [w["title"] for w in workshops]
    enrolled = [w["enrolled"] for w in workshops]
    capacity = [w["capacity"] for w in workshops]
    ratings = [w["avg_rating"] for w in workshops]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=titles, x=capacity, name="Available Places",
        orientation="h", marker_color=COLORS["bg_surface"],
        opacity=0.5,
    ))
    fig.add_trace(go.Bar(
        y=titles, x=enrolled, name="Participants",
        orientation="h", marker_color=COLORS["primary"],
        text=[f"★ {r}" for r in ratings], textposition="auto",
        textfont=dict(color="#fff", size=11),
    ))
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title=dict(text="Workshop Participation vs Available Places", font=dict(size=16)),
        barmode="overlay", height=450,
        xaxis=dict(gridcolor=COLORS["grid"]),
        yaxis=dict(autorange="reversed"),
    )
    return _to_html(fig, "workshop-chart")


# ---------------------------------------------------------------------------
# 3. Community Support Stacked Area
# ---------------------------------------------------------------------------

def create_community_support_chart(data):
    fig = go.Figure()
    sources = [
        ("Volunteer Hours", data["volunteer_hours"], COLORS["primary"]),
        ("Donated Materials", data["donated_materials"], COLORS["secondary"]),
        ("Grant-Supported Sessions", data["grant_sessions"], COLORS["warning"]),
        ("Partner Support", data["partner_support"], COLORS["accent"]),
        ("Community Outreach Support", data["outreach_support"], COLORS["info"]),
    ]
    for name, values, color in sources:
        fig.add_trace(go.Scatter(
            x=data["labels"], y=values,
            mode="lines", name=name, stackgroup="support",
            line=dict(width=0.5, color=color),
        ))
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title=dict(text="Community Support Breakdown", font=dict(size=16)),
        xaxis=dict(gridcolor=COLORS["grid"], showgrid=False),
        yaxis=dict(gridcolor=COLORS["grid"]),
        height=400,
    )
    return _to_html(fig, "support-chart")


# ---------------------------------------------------------------------------
# 4. Discovery Channels Donut
# ---------------------------------------------------------------------------

def create_discovery_donut(survey_data):
    channels = survey_data["discovery_channels"]
    fig = go.Figure(go.Pie(
        labels=list(channels.keys()),
        values=list(channels.values()),
        hole=0.55,
        marker=dict(colors=PALETTE),
        textinfo="label+percent",
        textfont=dict(size=11, color="#fff"),
        hoverinfo="label+value+percent",
    ))
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title=dict(text="How Members Discover Us", font=dict(size=16)),
        height=380,
        showlegend=False,
        annotations=[dict(
            text="Sources", x=0.5, y=0.5, font_size=14,
            font_color=COLORS["text_secondary"], showarrow=False
        )],
    )
    return _to_html(fig, "discovery-chart")


# ---------------------------------------------------------------------------
# 5. Engagement Time-Series
# ---------------------------------------------------------------------------

def create_engagement_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["dates"], y=data["page_views"],
        mode="lines", name="Page Views",
        line=dict(color=COLORS["info"], width=2),
        fill="tozeroy", fillcolor="rgba(79,195,247,0.1)",
    ))
    fig.add_trace(go.Scatter(
        x=data["dates"], y=data["unique_visitors"],
        mode="lines", name="Unique Visitors",
        line=dict(color=COLORS["secondary"], width=2),
    ))
    fig.add_trace(go.Scatter(
        x=data["dates"], y=data["interactions"],
        mode="lines", name="Interactions",
        line=dict(color=COLORS["accent"], width=1.5, dash="dash"),
    ))
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title=dict(text="Daily Engagement (90 Days)", font=dict(size=16)),
        xaxis=dict(gridcolor=COLORS["grid"], showgrid=False,
                   rangeslider=dict(visible=True, bgcolor=COLORS["bg_card"])),
        yaxis=dict(gridcolor=COLORS["grid"]),
        height=420,
    )
    return _to_html(fig, "engagement-chart")


# ---------------------------------------------------------------------------
# 6. Medium Interest Radar
# ---------------------------------------------------------------------------

def create_medium_radar(survey_data):
    medium = survey_data["medium_interest"]
    labels = list(medium.keys())
    values = list(medium.values())
    # Close the polygon
    labels.append(labels[0])
    values.append(values[0])

    fig = go.Figure(go.Scatterpolar(
        r=values, theta=labels,
        fill="toself",
        fillcolor="rgba(108,99,255,0.2)",
        line=dict(color=COLORS["primary"], width=2),
        marker=dict(size=6, color=COLORS["primary"]),
    ))
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title=dict(text="Art Medium Interest Distribution", font=dict(size=16)),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, gridcolor=COLORS["grid"],
                            color=COLORS["text_secondary"]),
            angularaxis=dict(gridcolor=COLORS["grid"],
                             color=COLORS["text_primary"]),
        ),
        height=420, showlegend=False,
    )
    return _to_html(fig, "medium-radar-chart")


# ---------------------------------------------------------------------------
# 7. Experience Ratings Histogram
# ---------------------------------------------------------------------------

def create_ratings_chart(survey_data):
    ratings = survey_data["experience_ratings"]
    counts = Counter(ratings)
    stars = [1, 2, 3, 4, 5]
    vals = [counts.get(s, 0) for s in stars]
    colors = [COLORS["accent"], COLORS["warning"], COLORS["warning"],
              COLORS["secondary"], COLORS["primary"]]

    fig = go.Figure(go.Bar(
        x=[f"{s} ★" for s in stars], y=vals,
        marker_color=colors,
        text=vals, textposition="outside",
        textfont=dict(color=COLORS["text_primary"], size=13),
    ))
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title=dict(text="Participant Feedback Summary", font=dict(size=16)),
        xaxis=dict(gridcolor=COLORS["grid"], showgrid=False),
        yaxis=dict(gridcolor=COLORS["grid"]),
        height=350,
    )
    return _to_html(fig, "ratings-chart")


# ---------------------------------------------------------------------------
# 8. Age Demographics Bar
# ---------------------------------------------------------------------------

def create_age_chart(survey_data):
    age = survey_data["age_distribution"]
    fig = go.Figure(go.Bar(
        x=list(age.keys()), y=list(age.values()),
        marker=dict(
            color=list(age.values()),
            colorscale=[[0, COLORS["info"]], [1, COLORS["primary"]]],
        ),
        text=list(age.values()), textposition="outside",
        textfont=dict(color=COLORS["text_primary"]),
    ))
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title=dict(text="Community Reach by Age Group", font=dict(size=16)),
        xaxis=dict(gridcolor=COLORS["grid"], showgrid=False),
        yaxis=dict(gridcolor=COLORS["grid"]),
        height=350,
    )
    return _to_html(fig, "age-chart")


# ---------------------------------------------------------------------------
# Convenience: Generate all charts
# ---------------------------------------------------------------------------

def generate_all_charts(dashboard_data):
    """Return a dict of all chart HTML strings keyed by chart name."""
    return {
        "user_growth": create_user_growth_chart(dashboard_data["user_growth"]),
        "workshops": create_workshop_chart(dashboard_data["workshops"]),
        "community_support": create_community_support_chart(dashboard_data["community_support"]),
        "discovery": create_discovery_donut(dashboard_data["surveys"]),
        "engagement": create_engagement_chart(dashboard_data["engagement"]),
        "medium_radar": create_medium_radar(dashboard_data["surveys"]),
        "ratings": create_ratings_chart(dashboard_data["surveys"]),
        "age_demographics": create_age_chart(dashboard_data["surveys"]),
    }
