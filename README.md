# Cloud_Dashboard

Project Overview
This project is a Cloud Infrastructure Management Platform designed to provide centralized management for cloud resources including virtual machines, storage, network policies, billing, monitoring, and support. It supports role-based user access, resource provisioning, real-time health monitoring, cost tracking, and ticketing for support.

The platform enables enterprises and service providers to automate cloud resource administration, improve visibility into usage and costs, and ensure security compliance across multi-cloud environments.

Technology Stack:

    Django and React

Features :
User registration, login, role-based access control

    Resource management: create, approve, monitor cloud VMs, storage, databases

    Real-time monitoring metrics and alerts

    Billing and budget tracking with cost summaries

    Support ticketing system for user queries and issues

    Network policy and firewall rules management

    Admin dashboard with comprehensive statistics

Testing
Automated tests written with pytest and pytest-django

Use Django REST Framework’s APIClient for authenticated API testing

Tests cover functional scenarios, edge cases, permission validations, and API behaviors

Includes basic performance and concurrency tests to simulate load and ensure stability

Test runner script generates a graphical report summarizing passed test cases per module

Running Tests
Activate backend virtual environment

bash
source backend/venv/bin/activate
Run the test suite and generate report

bash
./backend/run_all_tests.sh
View the generated graph backend/test_report.png for test summary visualization

Getting Started
Setup backend with Django and required Python packages

Setup frontend React environment with Node.js, npm, and Vite

Configure database and environment variables as needed

Run backend server (python manage.py runserver) and frontend dev server (npm run dev)

Use the web interface to interact with the platform

Contribution
Contributions are welcome! Please ensure you add corresponding tests when adding new features. Run tests before submitting pull requests.
