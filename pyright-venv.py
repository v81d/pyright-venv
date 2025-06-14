#!/usr/bin/env python3

import json
import os
import subprocess
import argparse
from pathlib import Path
import sys


def get_current_python_version():
    return f"{sys.version_info.major}.{sys.version_info.minor}"


def generate_pyright_config(project_dir, venv_name, python_version=None):
    project_dir = Path(project_dir).resolve()
    venv_path = project_dir / venv_name

    # Create venv if it does not exist
    if not venv_path.exists():
        if python_version is None:
            python_version = get_current_python_version()

        print(f"[+] Creating venv '{venv_name}' using Python {python_version}")
        try:
            subprocess.run(
                [f"python{python_version}", "-m", "venv", str(venv_path)], check=True
            )
        except FileNotFoundError:
            print(
                f"[-] Python {python_version} not found. Make sure it's installed and available."
            )
            return
        except subprocess.CalledProcessError as e:
            print(f"[-] Failed to create virtual environment: {e}")
            return
    else:
        print(f"[+] Found existing virtual environment at {venv_path}")

    config_path = project_dir / "pyrightconfig.json"
    config = {}

    # Load existing config if it exists
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print(
                f"[-] Existing pyrightconfig.json is invalid JSON. Overwriting."
            )

    # Update or append "venvPath" and "venv"
    config["venvPath"] = str(project_dir)
    config["venv"] = venv_name

    # Update the include key; append "."
    includes = config.get("include")
    if isinstance(includes, list):
        if "." not in includes:
            includes.append(".")
        config["include"] = includes
    else:
        config["include"] = ["."]

    # Write updated config
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"[+] Updated pyrightconfig.json in {project_dir}")
    print(f"venvPath: {project_dir}")
    print(f"venv: {venv_name}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate pyrightconfig.json and optionally create a virtual environment."
    )
    parser.add_argument(
        "venv_name", help="Name of the virtual environment directory (e.g. .venv)"
    )
    parser.add_argument(
        "--project",
        default=".",
        help="Path to the project directory (default: current)",
    )
    parser.add_argument(
        "--python",
        help="Python version to use when creating venv (default: current Python version)",
    )
    args = parser.parse_args()

    generate_pyright_config(args.project, args.venv_name, args.python)


if __name__ == "__main__":
    main()
