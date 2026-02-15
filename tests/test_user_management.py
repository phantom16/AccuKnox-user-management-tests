"""
End-to-End tests for User Management in OrangeHRM Admin module.

Covers: Navigate, Add, Search, Edit, Validate, Delete user flows.
"""
import pytest
import random
import string
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.admin_page import AdminPage

# Unique username to avoid collisions on the shared demo instance
TEST_USERNAME = "TestUsr_" + "".join(random.choices(string.digits, k=5))
TEST_PASSWORD = "Test@1234"
NEW_PASSWORD = "NewPass@5678"


# ---------- TC_001: Navigate to Admin Module ----------
class TestNavigateToAdmin:
    def test_navigate_to_admin_module(self, logged_in_page: Page):
        """Verify user can navigate to Admin > System Users page."""
        admin = AdminPage(logged_in_page)
        admin.navigate_to_admin()
        admin.verify_admin_page_loaded()
        assert "/admin/viewSystemUsers" in logged_in_page.url


# ---------- TC_002: Add a New User ----------
class TestAddUser:
    def test_add_new_user(self, admin_page: AdminPage):
        """Add a new system user and verify success toast."""
        admin_page.click_add()
        admin_page.select_user_role("Admin")
        admin_page.select_status("Enabled")
        admin_page.fill_employee_name("a")  # type partial name to trigger autocomplete
        admin_page.fill_username(TEST_USERNAME)
        admin_page.fill_password(TEST_PASSWORD)
        admin_page.click_save()
        admin_page.verify_success_toast("Successfully Saved")


# ---------- TC_003: Search the Newly Created User ----------
class TestSearchUser:
    def test_search_user_by_username(self, admin_page: AdminPage):
        """Search for the newly created user by username."""
        admin_page.search_by_username(TEST_USERNAME)
        rows = admin_page.get_table_rows()
        expect(rows.first).to_be_visible(timeout=10000)
        first_cells = admin_page.get_first_row_cells()
        expect(first_cells.nth(1)).to_contain_text(TEST_USERNAME)


# ---------- TC_004: Search User by Role Filter ----------
class TestSearchByRole:
    def test_search_user_by_role(self, admin_page: AdminPage):
        """Filter users by Admin role and verify results."""
        admin_page.search_by_role("Admin")
        rows = admin_page.get_table_rows()
        count = rows.count()
        assert count >= 1, "Expected at least one Admin user"
        # Verify first row shows Admin role
        first_cells = admin_page.get_first_row_cells()
        expect(first_cells.nth(2)).to_contain_text("Admin")


# ---------- TC_005: Edit User – Change Role ----------
class TestEditUserRole:
    def test_edit_user_role(self, admin_page: AdminPage):
        """Change user role from Admin to ESS."""
        admin_page.search_by_username(TEST_USERNAME)
        admin_page.click_first_row_edit()
        admin_page.select_user_role("ESS")
        admin_page.click_save()
        admin_page.verify_success_toast("Successfully Updated")


# ---------- TC_006: Edit User – Change Status ----------
class TestEditUserStatus:
    def test_edit_user_status(self, admin_page: AdminPage):
        """Change user status to Disabled."""
        admin_page.search_by_username(TEST_USERNAME)
        admin_page.click_first_row_edit()
        admin_page.select_status("Disabled")
        admin_page.click_save()
        admin_page.verify_success_toast("Successfully Updated")


# ---------- TC_007: Edit User – Change Password ----------
class TestEditUserPassword:
    def test_edit_user_password(self, admin_page: AdminPage):
        """Change user password."""
        admin_page.search_by_username(TEST_USERNAME)
        admin_page.click_first_row_edit()
        admin_page.toggle_change_password()
        admin_page.fill_password(NEW_PASSWORD)
        admin_page.click_save()
        admin_page.verify_success_toast("Successfully Updated")


# ---------- TC_008: Validate Updated Details ----------
class TestValidateUpdatedDetails:
    def test_validate_updated_user_details(self, admin_page: AdminPage):
        """Verify previously edited fields are persisted."""
        admin_page.search_by_username(TEST_USERNAME)
        first_cells = admin_page.get_first_row_cells()
        # After edits: role should be ESS, status Disabled
        expect(first_cells.nth(2)).to_contain_text("ESS")
        expect(first_cells.nth(3)).to_contain_text("Disabled")


# ---------- TC_009: Delete the User ----------
class TestDeleteUser:
    def test_delete_user(self, admin_page: AdminPage):
        """Delete the test user and verify success toast."""
        admin_page.search_by_username(TEST_USERNAME)
        admin_page.select_first_row_checkbox()
        admin_page.click_delete_selected()
        admin_page.confirm_delete()
        admin_page.verify_success_toast("Successfully Deleted")


# ---------- TC_010: Verify Deleted User Cannot Be Found ----------
class TestVerifyDeletion:
    def test_verify_deleted_user_not_found(self, admin_page: AdminPage):
        """Search for deleted user and confirm no records found."""
        admin_page.search_by_username(TEST_USERNAME)
        admin_page.verify_no_records_found()
