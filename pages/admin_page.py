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

    def navigate_to_admin(self):
        self.admin_menu.click()
        self.page.wait_for_load_state("networkidle")
        expect(self.page.locator("h6", has_text="Admin")).to_be_visible(timeout=10000)

    def verify_admin_page_loaded(self):
        expect(self.page.locator("h5", has_text="System Users")).to_be_visible(timeout=10000)

    # --- Search filters ---
    def get_username_search_input(self):
        return self.page.locator(
            ".oxd-form .oxd-grid-item:nth-child(1) input"
        )

    def get_user_role_dropdown(self):
        return self.page.locator(
            ".oxd-form .oxd-grid-item:nth-child(2) .oxd-select-text"
        )

    def get_status_dropdown(self):
        return self.page.locator(
            ".oxd-form .oxd-grid-item:nth-child(4) .oxd-select-text"
        )

    def search_by_username(self, username: str):
        search_input = self.get_username_search_input()
        search_input.fill(username)
        self.search_button.click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

    def search_by_role(self, role: str):
        dropdown = self.get_user_role_dropdown()
        dropdown.click()
        self.page.locator(f".oxd-select-dropdown .oxd-select-option:has-text('{role}')").click()
        self.search_button.click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

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

    def select_user_role(self, role: str):
        dropdown = self.page.locator(
            ".oxd-form .oxd-grid-item:nth-child(1) .oxd-select-text"
        )
        dropdown.click()
        self.page.locator(
            f".oxd-select-dropdown .oxd-select-option:has-text('{role}')"
        ).click()

    def select_status(self, status: str):
        dropdown = self.page.locator(
            ".oxd-form .oxd-grid-item:nth-child(3) .oxd-select-text"
        )
        dropdown.click()
        self.page.locator(
            f".oxd-select-dropdown .oxd-select-option:has-text('{status}')"
        ).click()

    def fill_employee_name(self, name: str):
        emp_input = self.page.locator("input[placeholder='Type for hints...']")
        emp_input.fill(name)
        self.page.wait_for_timeout(1500)
        autocomplete_option = self.page.locator(".oxd-autocomplete-option").first
        autocomplete_option.click()

    def fill_username(self, username: str):
        self.page.locator(
            ".oxd-form .oxd-grid-item:nth-child(4) input"
        ).fill(username)

    def fill_password(self, password: str):
        password_inputs = self.page.locator("input[type='password']")
        password_inputs.nth(0).fill(password)
        password_inputs.nth(1).fill(password)

    def click_save(self):
        self.page.locator("button[type='submit']:has-text('Save')").click()
        self.page.wait_for_load_state("networkidle")

    def verify_success_toast(self, message: str = "Success"):
        expect(self.toast_message).to_be_visible(timeout=10000)
        expect(self.toast_message).to_contain_text(message, timeout=5000)

    # --- Edit User ---
    def click_first_row_edit(self):
        self.get_table_rows().first.locator(
            "button:has(.oxd-icon.bi-pencil-fill)"
        ).click()
        self.page.wait_for_load_state("networkidle")

    def toggle_change_password(self):
        self.page.locator("label:has-text('Yes')").click()

    # --- Delete User ---
    def select_first_row_checkbox(self):
        self.get_table_rows().first.locator(".oxd-checkbox-input label").click()

    def click_delete_selected(self):
        self.delete_selected_button.click()
        self.page.wait_for_timeout(500)

    def confirm_delete(self):
        self.page.locator("button:has-text('Yes, Delete')").click()
        self.page.wait_for_load_state("networkidle")

    def verify_no_records_found(self):
        expect(self.no_records_text).to_be_visible(timeout=10000)
