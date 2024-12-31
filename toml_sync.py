import subprocess
import tomli
import tomli_w
from pathlib import Path


def get_packages():
    src = Path("src")
    return [
        d.name
        for d in src.iterdir()
        if src.exists() and d.is_dir() and not d.name.startswith(".")
    ]


def sync_dependencies():
    try:
        # Generate and read requirements
        with open("requirements.txt", "w") as req_file:
            subprocess.run(["pip", "freeze"], stdout=req_file, check=True)

        with open("requirements.txt") as f:
            deps = {
                name.lower(): version
                for line in f
                if "==" in line
                for name, version in [line.strip().split("==")]
            }

        # Exclude management packages
        excluded_packages = {"pip", "setuptools", "wheel", "tomli", "tomli-w"}
        filtered_deps = {
            name: version
            for name, version in deps.items()
            if name not in excluded_packages
        }

        # Update pyproject.toml
        pyproject_path = Path("pyproject.toml")
        if pyproject_path.exists():
            with pyproject_path.open("rb") as f:
                pyproject = tomli.load(f)

            if "project" in pyproject:
                pyproject["project"]["dependencies"] = [
                    f"{name}=={version}" for name, version in filtered_deps.items()
                ]

            pyproject.setdefault("tool", {})
            pyproject["tool"].setdefault("setuptools", {})
            pyproject["tool"]["setuptools"]["packages"] = get_packages()

            with pyproject_path.open("wb") as f:
                tomli_w.dump(pyproject, f)

        return True
    except (IOError, subprocess.CalledProcessError) as e:
        print(f"Error: {str(e)}")
        return False


if __name__ == "__main__":
    sync_dependencies()
