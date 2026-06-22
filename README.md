# Student Academic Portal

A desktop GUI application for managing student academic records, built for schools in Sierra Leone. Developed in Python using Tkinter, the portal digitizes record-keeping for teachers, principals, and administrators — and works fully offline.

## Overview

Many rural schools in Sierra Leone still rely on paper-based record-keeping, which is vulnerable to loss from rainy-season flooding, fire, insects, and human error. The Student Academic Portal replaces this with a local, offline-first system that supports the Free Quality School Education initiative and Sustainable Development Goal 4 (Quality Education).

## Features

- **Role-based access** — separate dashboards for Teachers, Principals, and Admins
- **Student registration** — unique student IDs in the format `SLE-DISTRICT-YEAR-NUMBER`
- **Custom subject entry** — add, edit, or remove subjects per student (supports vocational/specialized programs)
- **Automatic grade calculation** — averages and status classification:
  - 70%+ → Distinction
  - 50–69% → Pass
  - Below 50% → Needs Improvement
- **Statistics & reporting** — class averages, pass rates, gender breakdowns, and SDG 4 progress tracking
- **Report generation** — individual report cards, class lists, principal analytics, and admin audit logs
- **Data export** — CSV export (Excel-compatible) and print-to-clipboard support
- **Admin approval workflow** — new accounts require admin approval before access is granted
- **Security** — SHA-256 password hashing and role-based permissions
- **Offline-first** — no internet connection required; all data is stored locally

## Tech Stack

| Component | Details |
|---|---|
| Language | Python 3.7+ (developed/tested on 3.14.4) |
| GUI | Tkinter (standard library) |
| Storage | JSON (`users.json`, `pending.json`) |
| Security | SHA-256 password hashing |
| Optional libraries | `matplotlib` (charts), `reportlab` (PDF export), `openpyxl` (Excel compatibility) |

## Installation

1. Install Python 3.7 or higher.
2. Clone or download this repository.
3. (Optional) Install extra packages for charts/exports:
   ```bash
   pip install matplotlib reportlab openpyxl
   ```
4. Run the application:
   ```bash
   python student_portal.py
   ```
   No external packages are required to run the core application — Tkinter ships with Python.

## Usage

- **Teachers**: register students, enter subjects and grades, view statistics, generate report cards.
- **Principals**: monitor school-wide performance, compare classes, track SDG 4 indicators.
- **Admins**: approve or reject pending registrations, manage user accounts, review audit logs, back up data.

Default login credentials and detailed walkthroughs are available in the User Manual (see project documentation, Appendix C).

## Project Structure

```
student_portal.py      # Main application (LoginWindow, dashboards, report generation, etc.)
data/
  users.json            # Registered user accounts and student records
  pending.json          # Registrations awaiting admin approval
```

## Architecture

The application follows a three-tier structure:
1. **Login module** — authentication and role selection
2. **Registration module** — student/teacher/principal sign-up with admin approval
3. **Main dashboard** — role-specific views for record management and reporting

Core logic is organized into modular, user-defined functions (e.g., `calculate_average`, `determine_status`, `validate_grade`, `add_student`, `search_students`, `generate_statistics`), following structured programming principles.

## Roadmap

Planned future enhancements include:
- SMS notifications for parents
- Krio language support
- Companion mobile app for grade entry
- Integration with WAEC (WASSCE/BECE) result databases
- Multi-device data synchronization
- Charting and trend visualization with matplotlib

## Contributing

Contributions are welcome. Please open an issue or submit a pull request with a clear description of the change and, where relevant, test coverage.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Acknowledgements

Built in support of Sierra Leone's Free Quality School Education initiative and aligned with UN Sustainable Development Goal 4.
