import string
from itertools import combinations
from unittest.mock import patch

from django.test import SimpleTestCase
from django.urls import reverse

from .views import get_character_pool, get_password_length, get_password_strength


class PasswordGeneratorViewTests(SimpleTestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create a strong password in seconds")

    def test_password_generator_page_loads(self):
        response = self.client.get(
            reverse("generate-password"),
            {
                "length": "14",
                "lowercase": "on",
                "uppercase": "on",
                "numbers": "on",
                "symbols": "on",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password generated successfully")
        self.assertContains(response, "Length: 14")
        self.assertContains(response, "Strong")

    def test_password_length_is_clamped(self):
        self.assertEqual(get_password_length("3"), 6)
        self.assertEqual(get_password_length("100"), 32)
        self.assertEqual(get_password_length("bad-value"), 16)
        self.assertEqual(get_password_length(None), 16)

    def test_character_pool_defaults_to_lowercase(self):
        self.assertEqual(get_character_pool({}), "abcdefghijklmnopqrstuvwxyz")

    def test_strength_uses_length_and_selected_options(self):
        options = {"lowercase": "on", "uppercase": "on", "numbers": "on"}

        self.assertEqual(get_password_strength(14, options), "Strong")
        self.assertEqual(get_password_strength(10, options), "Medium")
        self.assertEqual(get_password_strength(6, options), "Weak")

    def test_long_single_group_password_is_strong(self):
        self.assertEqual(get_password_strength(32, {}), "Strong")
        self.assertEqual(get_password_strength(16, {"numbers": "on"}), "Medium")

    def test_symbol_pool_has_no_duplicates(self):
        pool = get_character_pool({"symbols": "on"})
        self.assertEqual(len(pool), len(set(pool)))

    def test_every_combination_includes_all_selected_groups(self):
        groups = {
            "lowercase": string.ascii_lowercase,
            "uppercase": string.ascii_uppercase,
            "numbers": string.digits,
            "symbols": get_character_pool({"symbols": "on"}),
        }
        for count in range(1, 5):
            for names in combinations(groups, count):
                with self.subTest(names=names):
                    options = {name: "on" for name in names}
                    response = self.client.get(reverse("generate-password"), {"length": 6, **options})
                    password = response.context["password"]
                    self.assertEqual(len(password), 6)
                    self.assertTrue(set(password) <= set(get_character_pool(options)))
                    for name in names:
                        self.assertTrue(any(character in groups[name] for character in password))

    def test_missing_options_use_lowercase(self):
        response = self.client.get(reverse("generate-password"))
        self.assertEqual(len(response.context["password"]), 16)
        self.assertTrue(set(response.context["password"]) <= set(string.ascii_lowercase))

    def test_rejects_password_missing_selected_group(self):
        with patch("generator.views.secrets.choice", side_effect=list("aaaaaaabcdeA")):
            response = self.client.get(reverse("generate-password"), {
                "length": 6, "lowercase": "on", "uppercase": "on",
            })
        self.assertEqual(response.context["password"], "abcdeA")

    def test_generated_password_is_not_cached(self):
        response = self.client.get(reverse("generate-password"))
        self.assertIn("no-store", response["Cache-Control"])
        self.assertIn("private", response["Cache-Control"])
        self.assertEqual(response["Referrer-Policy"], "no-referrer")

    def test_unsupported_methods_are_rejected(self):
        for name in ("home", "generate-password"):
            self.assertEqual(self.client.post(reverse(name)).status_code, 405)

    def test_password_html_is_escaped(self):
        with patch("generator.views.secrets.choice", return_value="&"):
            response = self.client.get(reverse("generate-password"), {"length": 6, "symbols": "on"})
        self.assertContains(response, "&amp;" * 6)
