from create_ai_tooling_app.cli import to_slug, validate_project_name


class TestToSlug:
    def test_basic(self):
        assert to_slug("my project") == "my_project"

    def test_hyphens_become_underscores(self):
        assert to_slug("my-project") == "my_project"

    def test_mixed_case(self):
        assert to_slug("My Project") == "my_project"

    def test_leading_trailing_spaces(self):
        assert to_slug("  my project  ") == "my_project"

    def test_special_characters_stripped(self):
        assert to_slug("my!@#project") == "myproject"

    def test_multiple_spaces(self):
        assert to_slug("my   project") == "my_project"

    def test_numbers_preserved(self):
        assert to_slug("tool v2") == "tool_v2"

    def test_all_special_chars_returns_empty(self):
        assert to_slug("!!!") == ""

    def test_leading_trailing_underscores_stripped(self):
        assert to_slug("_my_project_") == "my_project"


class TestValidateProjectName:
    def test_valid_name(self):
        assert validate_project_name("my project") is True

    def test_empty_string(self):
        assert validate_project_name("") == "Project name cannot be empty."

    def test_whitespace_only(self):
        assert validate_project_name("   ") == "Project name cannot be empty."

    def test_special_chars_only(self):
        assert validate_project_name("!!!") == "Project name must contain at least one letter or number."

    def test_name_with_numbers(self):
        assert validate_project_name("tool 2") is True
