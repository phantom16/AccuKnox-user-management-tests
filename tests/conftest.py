import pytest
from playwright.sync_api import Page, BrowserType
from pages.login_page import LoginPage
from pages.admin_page import AdminPage

BASE_URL = "https://opensource-demo.orangehrmlive.com"
ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "admin123"


@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }


@pytest.fixture()
def logged_in_page(page: Page) -> Page:
    """Login and return page ready at dashboard."""
    login = LoginPage(page)
    login.navigate()
    login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
    login.verify_dashboard_visible()
    return page


@pytest.fixture()
def admin_page(logged_in_page: Page) -> AdminPage:
    """Navigate to Admin module and return AdminPage object."""
    admin = AdminPage(logged_in_page)
    admin.navigate_to_admin()
    return admin
