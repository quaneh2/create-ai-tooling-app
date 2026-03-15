import shutil
from pathlib import Path

from jinja2 import Environment, PackageLoader

TEMPLATES_DIR = Path(__file__).parent / "templates"


def scaffold_project(
    project_name: str,
    project_slug: str,
    provider: str,
    target: Path,
) -> None:
    ctx = {
        "project_name": project_name,
        "project_slug": project_slug,
        "provider": provider,
    }

    env = Environment(
        loader=PackageLoader("create_ai_tooling_app", "templates"),
        keep_trailing_newline=True,
    )

    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    # Files rendered from Jinja2 templates
    template_files = [
        ("README.md.jinja", "README.md"),
        ("pyproject.toml.jinja", "pyproject.toml"),
        (".env.example.jinja", ".env.example"),
        (".gitignore.jinja", ".gitignore"),
        ("src/__init__.py.jinja", f"src/{project_slug}/__init__.py"),
        ("src/main.py.jinja", f"src/{project_slug}/main.py"),
        ("src/models/__init__.py.jinja", f"src/{project_slug}/models/__init__.py"),
        ("src/models/request.py.jinja", f"src/{project_slug}/models/request.py"),
        ("src/models/response.py.jinja", f"src/{project_slug}/models/response.py"),
        ("src/prompts/__init__.py.jinja", f"src/{project_slug}/prompts/__init__.py"),
        ("src/prompts/base.py.jinja", f"src/{project_slug}/prompts/base.py"),
        ("src/llm/__init__.py.jinja", f"src/{project_slug}/llm/__init__.py"),
        ("src/llm/client.py.jinja", f"src/{project_slug}/llm/client.py"),
        ("src/routes/__init__.py.jinja", f"src/{project_slug}/routes/__init__.py"),
        ("src/routes/tool.py.jinja", f"src/{project_slug}/routes/tool.py"),
        ("tests/__init__.py.jinja", "tests/__init__.py"),
        ("tests/test_tool.py.jinja", "tests/test_tool.py"),
    ]

    for template_path, output_path in template_files:
        template = env.get_template(template_path)
        rendered = template.render(**ctx)
        out = target / output_path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered)

