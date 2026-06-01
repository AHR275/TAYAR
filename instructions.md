## Tayar Project — Team Instructions & Architecture Guide

This document defines how the project is structured and how each team member should work with the codebase. The goal is to keep everything consistent, modular, and easy to maintain.

## System Architecture & Guidelines
1. Data Center (data_center.py)
Purpose: Centralized layer for all data access. Handles reading and writing to JSON files (users.json, rooms.json, transactions.json).
Structure:
UsersData: get_users(), get_user(user_id), add_user(user)
RoomsData: get_rooms(), get_room(room_id), get_building_of_room(room_id)
TransData: get_transactions(), get_transaction(tx_id), add_transaction(transaction)
Usage Guidelines:
Always fetch fresh data inside request methods; do not store global variables for transaction or user lists.
Return safe defaults (like []) to prevent template errors if JSON keys are missing.
Keep JSON files small and readable; since this is a university project, full in-memory reads/writes are acceptable.
2. Flask Forms (forms/)
Purpose: Handle all user input validation and form management.
Implementation: Use Flask-WTF.
Example: TopupForm
Fields: room (IntegerField), amount (RadioField)
Validators: DataRequired(), NumberRange()
Usage Guidelines:
Always validate forms on POST requests using form.validate_on_submit().
Pass form instances to templates for rendering.
3. Flask Views (routes/)
Purpose: Serve as controllers connecting forms, data layer, and templates.
Types:
MethodView — for pages with GET/POST handling (e.g., TopupView)
View — for simpler GET-only pages (e.g., TopupHistoryView)
Blueprints:
Each module has its own blueprint for modular routing.
Example: topup_bp in routes/topup.py
Usage Guidelines:
Fetch data within the request method; do not rely on globals.
Pass all needed data to templates via render_template.
Keep business logic inside the data layer (data_center) rather than views.
4. Templates (templates/)
Purpose: Frontend rendering using Jinja2.
Structure:
base.html — common layout with navbar/footer.
Module-specific templates inherit from base.html.
Examples: topup.html, dashboard.html, payment.html.
Usage Guidelines:
Use {% block content %} to insert page-specific content.
Loop safely over lists passed from views (avoid NoneType by ensuring defaults in the data layer).
5. Static Files (static/)
Purpose: CSS, JS, and images for frontend.
Examples: Tailwind CSS, chart.js for analytics module.
Usage Guidelines:
Organize JS per module if possible (e.g., static/js/chart.js for analytics).
Keep CSS in one main file unless module-specific styling is required.
6. Best Practices for Team Members
Do not edit other member’s files without coordination.
Always pull latest changes before starting work.
Follow the naming conventions:
Templates: match route names exactly (forgot_password.html NOT forgot_passport.html)
JSON files: consistent naming (users.json, transactions.json)
Data Layer: Always use UsersData, RoomsData, TransData instead of manually opening JSON.
Forms: Keep input validation centralized in Flask-WTF forms.
Flask Views: Use blueprints for modular routing; fetch data fresh for every request.
Templates: Loop over data safely; use {% for item in items %} with default empty lists.

# Member 1 — Team Leader

### Files


routes/homepage.py
routes/topup.py

templates/index.html
templates/homepage.html
templates/topup.html


### Responsibilities

#### Project Leadership

* Flask setup
* Folder structure
* Route integration
* Navbar & Footer
* base.html
* GitHub management
* Testing
* Bug fixing
* Final integration

#### Homepage Module

* Hero Section
* Features Section
* Announcements
* Landing Page UI
* Responsive Homepage

#### Top-Up Module

* Electricity Recharge Page
* Room Number Input
* Amount Selection Cards
* Recharge History
* Recharge Confirmation

---


# Member 2 — Team Leader

### Files


routes/homepage.py


templates/homepage.html



### Responsibilities

#### Project Leadership


* Navbar & Footer


#### Homepage Module

* Hero Section
* Features Section
* Announcements
* Landing Page UI
* Responsive Homepage


# Member 4 — Payment Module

### Files


routes/payment.py

templates/payment.html
templates/success.html


### Responsibilities

* Payment Page
* Card Payment UI
* QR Payment UI
* Transaction Summary
* Success Page
* Receipt Design

---

# Member 5 — User Dashboard

### Files


routes/dashboard.py

templates/dashboard.html


### Responsibilities

* Dashboard UI
* Current Balance
* Recent Transactions
* Electricity Status Cards
* Sidebar Navigation

---

# Member 6 — Analytics & Charts

### Files


routes/analyze.py

templates/analyze.html

static/js/chart.js



### Responsibilities

* Consumption Charts
* Monthly Reports
* Statistics Cards
* Chart.js Integration
* Energy Analysis

---

# Member 7 — Admin Panel

### Files


routes/admin.py

templates/admin.html
templates/manage_users.html


### Responsibilities

* Admin Dashboard
* User Management
* Room Management
* Search & Filters
* Transaction Monitoring

---

# Member 8 — Authentication + Responsive Optimization

### Files


routes/auth.py

templates/login.html
templates/register.html
templates/forgot_password.html


### Responsibilities

#### Authentication Pages

* Login Page
* Register Page
* Forgot Password Page

#### UI Finishing

* Mobile Responsiveness
* Tailwind Improvements
* Animations
* Consistent Design
* Final UI Polishing

---

# Member 9 — Documentation & Video

### Responsibilities

* Final Report
* Screenshots
* Contribution Table
* Project Video
* PPT Preparation
* Submission Organization

---

One more thing: looking at your current structure screenshot, you still have:


templates/forgot_passport.html


It should be renamed to:


templates/forgot_password.html


before everyone starts coding, otherwise the route names and template names will become inconsistent.
