# VELORA Salon Studio

A responsive salon website portfolio project built with Flask, HTML, CSS, JavaScript and a MySQL-compatible database.

## Features
- Luxury salon landing page with services, pricing, gallery and contact details
- Appointment request form (no online payment)
- Appointment records saved to MySQL/TiDB Cloud when database environment variables are configured
- SQLite fallback for a quick local preview
- Basic appointment admin view at `/admin`
- Health check at `/health`

## Run locally
1. Install Python 3.10 or newer.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set a strong `SECRET_KEY`.
4. Leave MySQL settings blank for SQLite preview, or enter your MySQL/TiDB connection details.
5. Run: `python app.py`
6. Open `http://127.0.0.1:5000`.

## Deploy on Render
1. Upload this folder to a GitHub repository.
2. Create a new **Web Service** on Render and connect the repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Add environment variables in Render: `SECRET_KEY`, `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`.
6. Use the database host, username, password, port and database name provided by your MySQL-compatible host. Follow that provider's TLS connection instructions.

The app creates its appointment table when it starts. `schema.sql` is also provided if you prefer to create the table manually.

## Important before real use
- The `/admin` page is intentionally a portfolio/demo view and is **not password protected**. Add authentication and role-based access before using it with real customer data.
- Use real business contact details only with permission. The salon name and address in this demo are fictional.
- Add a privacy notice and retention policy before collecting real customer information.
- Confirm your database provider's TLS requirements and current free-tier limits.
