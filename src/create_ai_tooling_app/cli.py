import re
import sys
from pathlib import Path

import questionary
import typer
from rich.console import Console
from rich.panel import Panel

from .scaffold import ScaffoldError, scaffold_project

app = typer.Typer(add_completion=False)
console = Console()


def to_slug(name: str) -> str:
    slug = name.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s-]+", "_", slug)
    slug = slug.strip("_")
    return slug


def validate_project_name(name: str) -> bool | str:
    if not name.strip():
        return "Project name cannot be empty."
    if not to_slug(name):
        return "Project name must contain at least one letter or number."
    return True


@app.command()
def main(
    output_dir: Path = typer.Argument(
        default=None,
        help="Directory to create the project in. Defaults to current directory.",
    ),
) -> None:
    console.print(
        Panel(
            "[bold cyan]create-ai-tooling-app[/bold cyan]\n"
            "[dim]Scaffold a Python AI tooling API project[/dim]",
            expand=False,
        )
    )

    project_name: str = questionary.text(
        "Project name:",
        validate=validate_project_name,
    ).ask()

    if project_name is None:
        sys.exit(0)

    project_slug = to_slug(project_name)

    provider: str = questionary.select(
        "LLM provider:",
        choices=[
            questionary.Choice("Anthropic (Claude)", value="anthropic"),
            questionary.Choice("OpenAI", value="openai"),
        ],
    ).ask()

    if provider is None:
        sys.exit(0)

    target = (output_dir or Path.cwd()) / project_slug

    if target.exists():
        overwrite = questionary.confirm(
            f"Directory '{target}' already exists. Overwrite?", default=False
        ).ask()
        if not overwrite:
            console.print("[yellow]Aborted.[/yellow]")
            sys.exit(0)

    console.print(f"\n[dim]Scaffolding [bold]{project_name}[/bold] in {target}...[/dim]")

    try:
        scaffold_project(
            project_name=project_name,
            project_slug=project_slug,
            provider=provider,
            target=target,
        )
    except ScaffoldError as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        sys.exit(1)

    api_key_var = "ANTHROPIC_API_KEY" if provider == "anthropic" else "OPENAI_API_KEY"

    console.print(
        Panel(
            f"[bold green]Done![/bold green] Your project is ready.\n\n"
            f"  [bold]cd {project_slug}[/bold]\n"
            f"  [bold]cp .env.example .env[/bold]   # add your {api_key_var}\n"
            f"  [bold]uv sync[/bold]\n"
            f"  [bold]uv run fastapi dev src/{project_slug}/main.py[/bold]",
            title="Next steps",
            expand=False,
        )
    )
