"""
Dashboard Blueprint Routes
============================
Flask Blueprint providing analytics dashboard endpoints.
Integrates synthetic data + Plotly charts into a unified view.
"""

from flask import Blueprint, render_template, jsonify, session, redirect, url_for
from .synthetic_data import get_all_dashboard_data, generate_kpi_summary
from .charts import generate_all_charts

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    template_folder="../templates",
    url_prefix="/dashboard",
)


@dashboard_bp.before_request
def require_login():
    """Redirect unauthenticated users to the login page."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))


@dashboard_bp.route("/", strict_slashes=False)
def dashboard_home():
    """Main analytics dashboard view with KPIs and all charts."""
    data = get_all_dashboard_data(seed_value=42)
    charts = generate_all_charts(data)

    return render_template(
        "dashboard.html",
        kpis=data["kpis"],
        charts=charts,
        workshops=data["workshops"],
        events=data["events"],
        content_performance=data["content_performance"],
    )


@dashboard_bp.route("/api/data")
def dashboard_api():
    """JSON API endpoint for all dashboard data (for AJAX / frontend use)."""
    data = get_all_dashboard_data(seed_value=42)
    return jsonify(data)


@dashboard_bp.route("/api/kpis")
def kpi_api():
    """JSON API endpoint for KPI summary only."""
    return jsonify(generate_kpi_summary(seed_value=42))
