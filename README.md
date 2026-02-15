# AccuKnox User Management Tests

End-to-end manual and automated test cases for the **User Management** module in [OrangeHRM](https://opensource-demo.orangehrmlive.com).

---

## Project Structure

```
AccuKnox-user-management-tests/
├── pages/                  # Page Object Model classes
│   ├── login_page.py       # Login page actions & selectors
│   └── admin_page.py       # Admin/User Management page actions & selectors
├── tests/                  # Playwright test cases
│   ├── conftest.py         # Fixtures (login, navigation)
│   └── test_user_management.py  # 10 E2E test cases
├── test-cases/             # Manual test case documentation
│   └── manual_test_cases.csv
├── scripts/                # Problem Statement 2 scripts
│   ├── system_health_monitor.py  # System health monitoring
│   └── app_health_checker.py     # Application health checker
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Project Setup

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/AccuKnox-user-management-tests.git
cd AccuKnox-user-management-tests

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

---

## How to Run the Test Cases

### Run all Playwright tests (headed mode with slow motion)

```bash
pytest
```

### Run in headless mode

```bash
pytest --headless
```

### Run a specific test class

```bash
pytest tests/test_user_management.py::TestAddUser -v
```

### Run with HTML report

```bash
pip install pytest-html
pytest --html=report.html --self-contained-html
```

---

## Playwright Version

- **Playwright**: 1.58.0
- **pytest-playwright**: 0.7.2

---

## Problem Statement 2 Scripts

### System Health Monitor

Monitors CPU, memory, disk space, and top processes. Alerts when thresholds are exceeded.

```bash
python scripts/system_health_monitor.py
```

### Application Health Checker

Checks if web applications are up or down by verifying HTTP status codes.

```bash
# Check default URLs
python scripts/app_health_checker.py

# Check custom URLs
python scripts/app_health_checker.py https://example.com https://google.com
```

---

## Test Scenarios Covered

| # | Test Case | Description |
|---|-----------|-------------|
| 1 | Navigate to Admin Module | Login and open Admin > System Users |
| 2 | Add a New User | Create user with all required fields |
| 3 | Search by Username | Find the newly created user |
| 4 | Search by Role Filter | Filter users by Admin role |
| 5 | Edit User Role | Change role from Admin to ESS |
| 6 | Edit User Status | Change status to Disabled |
| 7 | Edit User Password | Update user password |
| 8 | Validate Updated Details | Verify edits are persisted |
| 9 | Delete the User | Remove user via delete action |
| 10 | Verify Deletion | Confirm deleted user is not found |

---

## Application Under Test

- **URL**: https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
- **Credentials**: Admin / admin123
