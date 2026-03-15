import tempfile
from pathlib import Path

import pytest

from create_ai_tooling_app.scaffold import ScaffoldError, scaffold_project

PROVIDERS = ["anthropic", "openai"]


@pytest.fixture
def tmp_target(tmp_path: Path) -> Path:
    return tmp_path / "my_project"


@pytest.mark.parametrize("provider", PROVIDERS)
def test_scaffold_creates_expected_files(tmp_target: Path, provider: str) -> None:
    scaffold_project(
        project_name="My Project",
        project_slug="my_project",
        provider=provider,
        target=tmp_target,
    )

    expected = [
        "README.md",
        "pyproject.toml",
        ".env.example",
        ".gitignore",
        "src/my_project/__init__.py",
        "src/my_project/main.py",
        "src/my_project/models/request.py",
        "src/my_project/models/response.py",
        "src/my_project/prompts/base.py",
        "src/my_project/llm/client.py",
        "src/my_project/routes/tool.py",
        "tests/test_tool.py",
    ]

    for path in expected:
        assert (tmp_target / path).exists(), f"Missing: {path}"


@pytest.mark.parametrize("provider", PROVIDERS)
def test_scaffold_uses_project_slug(tmp_target: Path, provider: str) -> None:
    scaffold_project(
        project_name="My Project",
        project_slug="my_project",
        provider=provider,
        target=tmp_target,
    )

    main_py = (tmp_target / "src/my_project/main.py").read_text()
    assert "My Project" in main_py

    pyproject = (tmp_target / "pyproject.toml").read_text()
    assert 'name = "my_project"' in pyproject


def test_scaffold_anthropic_uses_anthropic_sdk(tmp_target: Path) -> None:
    scaffold_project(
        project_name="My Project",
        project_slug="my_project",
        provider="anthropic",
        target=tmp_target,
    )

    client = (tmp_target / "src/my_project/llm/client.py").read_text()
    assert "import anthropic" in client
    assert "openai" not in client

    pyproject = (tmp_target / "pyproject.toml").read_text()
    assert "anthropic" in pyproject
    assert "openai" not in pyproject


def test_scaffold_openai_uses_openai_sdk(tmp_target: Path) -> None:
    scaffold_project(
        project_name="My Project",
        project_slug="my_project",
        provider="openai",
        target=tmp_target,
    )

    client = (tmp_target / "src/my_project/llm/client.py").read_text()
    assert "import openai" in client
    assert "anthropic" not in client

    pyproject = (tmp_target / "pyproject.toml").read_text()
    assert "openai" in pyproject
    assert "anthropic" not in pyproject


def test_scaffold_overwrites_existing_directory(tmp_target: Path) -> None:
    tmp_target.mkdir(parents=True)
    (tmp_target / "old_file.txt").write_text("should be gone")

    scaffold_project(
        project_name="My Project",
        project_slug="my_project",
        provider="anthropic",
        target=tmp_target,
    )

    assert not (tmp_target / "old_file.txt").exists()
    assert (tmp_target / "pyproject.toml").exists()


def test_scaffold_raises_on_unwritable_directory(tmp_path: Path) -> None:
    tmp_path.chmod(0o444)  # read-only

    try:
        with pytest.raises(ScaffoldError, match="Could not create project directory"):
            scaffold_project(
                project_name="My Project",
                project_slug="my_project",
                provider="anthropic",
                target=tmp_path / "my_project",
            )
    finally:
        tmp_path.chmod(0o755)  # restore so cleanup works
