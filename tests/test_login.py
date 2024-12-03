import pytest
from playwright.sync_api import Page, expect

class TestLogin:
    def test_something(self, page: Page):
        """Basic test that will fail as requested"""
        print('hello')
        expect(True).to_be_empty()