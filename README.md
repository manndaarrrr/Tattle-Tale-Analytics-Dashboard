https://www.tatletale.com

# Tattle Tale Analytics Dashboard

A Flask and Plotly analytics dashboard built for **Tattle Tale**, a Sheffield, UK art community platform focused on creative workshops, community storytelling, and intergenerational participation.

The project combines a public-facing community website with a protected admin analytics dashboard. The dashboard uses synthetic, deterministic data to demonstrate community growth, workshop participation, survey insights, engagement trends, and content performance.

![Tattle Tale Analytics Dashboard](dash_img/Screenshot%202026-05-12%20162036.png)

---

## Project Highlights

- Public-facing website pages for the Tattle Tale art community
- Protected admin dashboard with session-based login
- Interactive Plotly analytics dashboard
- Community survey, contact, and feedback form endpoints
- Email delivery support through Flask-Mail and SMTP
- Event booking page with Ticket Tailor integration
- Responsive frontend pages with custom CSS styling
- Synthetic analytics data for demo and presentation use
- Passenger WSGI entry point for shared-hosting deployment

---

## Dashboard Preview

### Dashboard Overview

![Dashboard Overview](dash_img/Screenshot%202026-05-12%20162036.png)

### Analytics View 1

![Analytics View 1](dash_img/Screenshot%202026-05-12%20162046.png)

### Analytics View 2

![Analytics View 2](dash_img/Screenshot%202026-05-12%20162053.png)

### Analytics View 3

![Analytics View 3](dash_img/Screenshot%202026-05-12%20162102.png)

### Analytics View 4

![Analytics View 4](dash_img/Screenshot%202026-05-12%20162110.png)

### Analytics View 5

![Analytics View 5](dash_img/Screenshot%202026-05-12%20162117.png)

### Analytics View 6

![Analytics View 6](dash_img/Screenshot%202026-05-12%20162126.png)

### Analytics View 7

![Analytics View 7](dash_img/Screenshot%202026-05-12%20162142.png)

### Analytics View 8

![Analytics View 8](dash_img/Screenshot%202026-05-12%20162153.png)

---

## Tech Stack

| Area | Technology |
|---|---|
| Backend | Python, Flask |
| Templates | Jinja2, HTML |
| Styling | CSS, responsive design, Wix-exported page assets |
| Analytics | Plotly, synthetic Python data generators |
| Email | Flask-Mail, SMTP, python-dotenv |
| Authentication | Flask session-based demo login |
| Deployment | Passenger WSGI / shared hosting compatible |

---

## Main Features

### Public Community Website

The project includes public pages for:

- Homepage
- About / founder story
- Tattle Tale story page
- Workshop chapters
- Event booking
- Community survey
- FAQ
- Privacy policy

### Analytics Dashboard

The dashboard contains:

- KPI cards for members, active members, workshops, survey responses, and ratings
- Daily engagement trends
- Community growth chart
- Workshop performance chart
- Discovery channel breakdown
- Art medium interest insights
- Experience ratings
- Age demographic chart
- Content performance table
- Workshop details table

### Forms and Email Workflows

The backend supports:

- Feedback form submissions
- Community survey submissions
- Contact form submissions

Submissions are formatted and sent by email using Flask-Mail. No local database is required for form storage.

### Synthetic Analytics Data

The analytics module uses deterministic synthetic data generated in Python. This makes the dashboard suitable for demonstrations, portfolio use, stakeholder presentations, and development without exposing real community data.

---

## Project Structure

```text
.
├── app.py
├── passenger_wsgi.py
├── requirements.txt
├── README.md
├── LICENSE
├── .env.example
├── .gitignore
├── dash_img/
│   ├── Screenshot 2026-05-12 162036.png
│   ├── Screenshot 2026-05-12 162046.png
│   ├── Screenshot 2026-05-12 162053.png
│   ├── Screenshot 2026-05-12 162102.png
│   ├── Screenshot 2026-05-12 162110.png
│   ├── Screenshot 2026-05-12 162117.png
│   ├── Screenshot 2026-05-12 162126.png
│   ├── Screenshot 2026-05-12 162142.png
│   └── Screenshot 2026-05-12 162153.png
├── dashboard/
│   ├── __init__.py
│   ├── charts.py
│   ├── dashboard_routes.py
│   └── synthetic_data.py
├── static/
│   ├── css/
│   ├── images/
│   ├── js/
│   └── videos/
└── templates/
    ├── index.html
    ├── login.html
    ├── dashboard.html
    ├── event-booking.html
    ├── community-survey.html
    ├── about-lana.html
    ├── faq.html
    ├── privacy-policy.html
    └── ...
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/mandaarrrr/Tattle-Tale-Analytics-Dashboard.git
cd Tattle-Tale-Analytics-Dashboard
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your environment file

Copy the example environment file:

```bash
cp .env.example .env
```

Update `.env` with your own values:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
MAIL_TO=recipient@example.com
SECRET_KEY=change-this-secret-key
```

Do **not** commit `.env` to GitHub.

### 5. Run the application

```bash
python app.py
```

Open the app in your browser:

```text
http://localhost:5000
```

---

## Admin Dashboard Access

Go to:

```text
http://localhost:5000/login
```

This project currently uses demo login logic:

- Any valid email format is accepted
- Any non-empty password is accepted

After login, the dashboard is available at:

```text
http://localhost:5000/dashboard/
```

For production use, replace the demo login with secure authentication, password hashing, role management, and proper access control.

---

## Important Routes

| Route | Description |
|---|---|
| `/` | Homepage |
| `/login` | Admin login page |
| `/logout` | Ends admin session |
| `/dashboard/` | Protected analytics dashboard |
| `/dashboard/api/data` | Full dashboard JSON data |
| `/dashboard/api/kpis` | KPI-only JSON response |
| `/community-survey` | Survey page |
| `/event-booking` | Workshop booking page |
| `/faq` | FAQ page |
| `/privacy-policy` | Privacy policy page |
| `/api/feedback` | Feedback form endpoint |
| `/api/community-survey` | Community survey endpoint |
| `/api/contact` | Contact form endpoint |

---

## Deployment Notes

This project includes `passenger_wsgi.py`, making it suitable for Passenger-based shared hosting environments.

Before deployment:

1. Set production environment variables on the server.
2. Do not upload `.env` with real secrets to public repositories.
3. Confirm the correct Python version is selected on the host.
4. Install dependencies from `requirements.txt`.
5. Replace demo authentication before using the dashboard with real admin data.
6. Test email delivery with your SMTP provider.

---

## Security Notes

This repository should not include:

- Real email passwords
- Gmail app passwords
- Production secret keys
- Virtual environment folders
- Python cache files
- Private user or community data

Only `.env.example` should be committed. The real `.env` file should stay local and private.

The included dashboard data is synthetic and generated for demonstration purposes.

---

## Future Improvements

- Add a real database for survey responses and dashboard metrics
- Replace demo login with secure admin authentication
- Add password hashing and role-based access control
- Add automated tests for routes and APIs
- Add CI/CD deployment workflow
- Connect dashboard charts to real community engagement data
- Improve form validation and spam protection
- Add accessibility testing for public pages

---

## Acknowledgement

Built as a digital platform and analytics dashboard concept for the Tattle Tale art community in Sheffield, UK.
