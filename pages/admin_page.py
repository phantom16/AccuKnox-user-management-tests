from playwright.sync_api import Page, expect


class AdminPage:
    def __init__(self, page: Page):
        self.page = page
        self.admin_menu = page.locator("a[href='/web/index.php/admin/viewAdminModule']")
        self.add_button = page.locator("button:has-text('Add')")
        self.search_button = page.locator("button[type='submit']:has-text('Search')")
        self.reset_button = page.locator("button[type='reset']:has-text('Reset')")
        self.delete_selected_button = page.locator(
            ".orangehrm-header-container button:has(.oxd-icon.bi-trash)"
        )
        self.toast_message = page.locator(".oxd-toast")
        self.records_table = page.locator(".oxd-table-body")
        self.no_records_text = page.locator("span:has-text('No Records Found')")

    # --- Helper: find form field by label text ---
    def _get_field_group(self, label_text: str):
        """Return the .oxd-grid-item that contains the given label."""
        return self.page.locator(
            f".oxd-form .oxd-grid-item:has(.oxd-label:text-is('{label_text}'))"
        )

    def _select_dropdown(self, label_text: str, option_text: str):
        """Click a dropdown identified by its label and pick an option."""
        group = self._get_field_group(label_text)
        group.locator(".oxd-select-text").click()
        self.page.locator(
            f".oxd-select-dropdown .oxd-select-option:has-text('{option_text}')"
        ).click()

    def _fill_input(self, label_text: str, value: str):
        """Fill a text input identified by its label."""
        group = self._get_field_group(label_text)
        group.locator("input").fill(value)

    # --- Navigation ---
    def navigate_to_admin(self):
        self.admin_menu.click()
        self.page.wait_for_load_state("networkidle")
        expect(self.page.locator("h6", has_text="Admin")).to_be_visible(timeout=15000)

    def verify_admin_page_loaded(self):
        expect(self.page.locator("h5", has_text="System Users")).to_be_visible(timeout=10000)

    # --- Search filters ---
    def search_by_username(self, username: str):
        self._fill_input("Username", username)
        self.search_button.click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

    def search_by_role(self, role: str):
        self._select_dropdown("User Role", role)
        self.search_button.click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

    # --- Table helpers ---
    def get_table_rows(self):
        return self.page.locator(".oxd-table-body .oxd-table-row")

    def get_first_row_cells(self):
        return self.get_table_rows().first.locator(".oxd-table-cell")

    def get_record_count(self):
        return self.get_table_rows().count()

    # --- Add User ---
    def click_add(self):
        self.add_button.click()
        self.page.wait_for_load_state("networkidle")
        expect(self.page.locator("h6", has_text="Add User")).to_be_visible(timeout=10000)

    def select_user_role(self, role: str):
        self._select_dropdown("User Role", role)

    def select_status(self, status: str):
        self._select_dropdown("Status", status)

    def fill_employee_name(self, name: str):
        emp_input = self.page.locator("input[placeholder='Type for hints...']")
        emp_input.fill(name)
        self.page.wait_for_timeout(2000)
        autocomplete_option = self.page.locator(".oxd-autocomplete-option")
        expect(autocomplete_option.first).to_be_visible(timeout=10000)
        autocomplete_option.first.click()
        self.page.wait_for_timeout(500)

    def fill_username(self, username: str):
        self._fill_input("Username", username)

    def fill_password(self, password: str):
        password_inputs = self.page.locator("input[type='password']")
        password_inputs.nth(0).fill(password)
        password_inputs.nth(1).fill(password)

    def click_save(self):
        self.page.locator("button[type='submit']:has-text('Save')").click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

    def verify_success_toast(self, message: str = "Success"):
        expect(self.toast_message).to_be_visible(timeout=15000)
        expect(self.toast_message).to_contain_text(message, timeout=5000)
        self.page.wait_for_timeout(1000)

    # --- Edit User ---
    def click_first_row_edit(self):
        edit_button = self.get_table_rows().first.locator(
            "button:has(.oxd-icon.bi-pencil-fill)"
        )
        expect(edit_button).to_be_visible(timeout=10000)
        edit_button.click()
        self.page.wait_for_load_state("networkidle")
        expect(self.page.locator("h6", has_text="Edit User")).to_be_visible(timeout=10000)

    def toggle_change_password(self):
        self.page.locator("label:has-text('Yes')").click()
        self.page.wait_for_timeout(500)

    # --- Delete User ---
    def click_first_row_delete(self):
        """Click the trash/delete icon button on the first table row."""
        delete_button = self.get_table_rows().first.locator(
            "button:has(.oxd-icon.bi-trash)"
        )
        expect(delete_button).to_be_visible(timeout=10000)
        delete_button.click()
        self.page.wait_for_timeout(1000)

    def confirm_delete(self):
        confirm_btn = self.page.locator("button:has-text('Yes, Delete')")
        expect(confirm_btn).to_be_visible(timeout=5000)
        confirm_btn.click()
        self.page.wait_for_load_state("networkidle")

    def verify_no_records_found(self):
        no_records = self.page.locator("span.oxd-text:has-text('No Records Found')")
        expect(no_records).to_be_visible(timeout=10000)
