
#!/usr/bin/env python3
import argparse
import ast
import os
import sys
from typing import Set, Dict

# Probeer standaardlib set op te halen (Python 3.10+)
try:
    STDLIB = set(sys.stdlib_module_names)
except AttributeError:
    # Fallback voor oudere Python: minimale set; kan uitgebreid worden
    STDLIB = {
        'abc','argparse','array','ast','asyncio','base64','bz2','cmath','collections','concurrent','contextlib',
        'copy','csv','dataclasses','datetime','decimal','enum','functools','gc','getpass','glob','hashlib','heapq',
        'hmac','html','http','importlib','inspect','io','ipaddress','itertools','json','logging','math','multiprocessing',
        'numbers','operator','os','pathlib','pickle','pkgutil','platform','plistlib','queue','random','re','sched',
        'secrets','select','shutil','signal','site','socket','sqlite3','ssl','statistics','string','struct','subprocess',
        'sys','tempfile','textwrap','threading','time','types','typing','unittest','urllib','uuid','venv','warnings',
        'weakref','xml','zipfile','zoneinfo'
    }

# Mapping van importnaam naar PyPI pakketnaam
NAME_MAP: Dict[str, str] = {
    "bs4": "beautifulsoup4",
    "PIL": "Pillow",
    "sklearn": "scikit-learn",
    "skimage": "scikit-image",
    "cv2": "opencv-python",
    "yaml": "PyYAML",
    "Crypto": "pycryptodome",
    "tensorflow": "tensorflow",
    "torch": "torch",
    "torchvision": "torchvision",
    "torchaudio": "torchaudio",
    "pandas": "pandas",
    "numpy": "numpy",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "requests": "requests",
    "httpx": "httpx",
    "flask": "Flask",
    "fastapi": "fastapi",
    "django": "Django",
    "sqlalchemy": "SQLAlchemy",
    "pydantic": "pydantic",
    "tqdm": "tqdm",
    "pytest": "pytest",
    "notebook": "notebook",
    "jupyter": "jupyter",
    "scipy": "scipy",
    "xgboost": "xgboost",
    "lightgbm": "lightgbm",
    "spacy": "spacy",
    "langchain": "langchain",
    "dateutil": "python-dateutil"  # vaak geimporteerd als dateutil
}


def is_relative_or_local(name: str) -> bool:
    # Relatieve imports of pakket-onderdelen moeten niet als toplevel dependency worden gezien
    return name.startswith('.') or name == ''


def top_level_from_name(name: str) -> str:
    # 'pkg.sub.module' -> 'pkg'
    return name.split('.')[0] if name else name


def collect_imports_from_file(py_path: str) -> Set[str]:
    mods: Set[str] = set()
    try:
        with open(py_path, 'r', encoding='utf-8') as f:
            node = ast.parse(f.read(), filename=py_path)
    except Exception:
        return mods  # sla problematische files over

    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            for alias in n.names:
                name = top_level_from_name(alias.name)
                if not is_relative_or_local(name):
                    mods.add(name)
        elif isinstance(n, ast.ImportFrom):
            # from x.y import z
            if n.module:
                name = top_level_from_name(n.module)
                if not is_relative_or_local(name):
                    mods.add(name)
    return mods


def is_stdlib_module(mod: str) -> bool:
    # Snel checken: in STDLIB of 'xml', 'unittest', etc.
    if mod in STDLIB:
        return True
    # Heuristiek: modules met namen die duidelijk stdlib zijn
    builtin_prefixes = ('xml', 'unittest', 'email', 'http', 'importlib', 'asyncio', 'concurrent', 'sqlite3', 'distutils')
    return mod in STDLIB or mod.startswith(builtin_prefixes)


def map_to_pypi_name(module: str) -> str:
    return NAME_MAP.get(module, module)


def discover_py_files(root: str) -> Set[str]:
    files: Set[str] = set()
    for dirpath, dirnames, filenames in os.walk(root):
        # skip veelvoorkomende build/venv dirs
        skip = {'.git', '.hg', '.svn', '.venv', 'venv', 'env', 'build', 'dist', '__pycache__'}
        dirnames[:] = [d for d in dirnames if d not in skip]
        for fn in filenames:
            if fn.endswith('.py'):
                files.add(os.path.join(dirpath, fn))
    return files


def pin_versions(pkgs: Set[str]) -> Dict[str, str]:
    """
    Probeer versies te bepalen via importlib.metadata (Python 3.8+).
    Retourneert dict: pkg_name -> version of "" als onbekend.
    """
    versions: Dict[str, str] = {}
    try:
        from importlib.metadata import version, PackageNotFoundError
    except Exception:
        # geen pinning mogelijk
        return {p: "" for p in pkgs}

    for p in pkgs:
        # PyPI key kan hoofdletters hebben (Django, SQLAlchemy), probeer case-sensitief
        try:
            versions[p] = version(p)
        except PackageNotFoundError:
            # fallback: soms importnaam != PyPI naam; al gemapt, dus niets
            versions[p] = ""
        except Exception:
            versions[p] = ""
    return versions


def write_requirements(outfile: str, pkgs_with_versions: Dict[str, str]) -> None:
    lines = []
    for pkg, ver in sorted(pkgs_with_versions.items(), key=lambda kv: kv[0].lower()):
        if ver:
            lines.append(f"{pkg}=={ver}")
        else:
            lines.append(pkg)
    with open(outfile, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(
        description="Genereer requirements.txt uit Python-imports in een project."
    )
    parser.add_argument("project_root", help="Pad naar projectroot (directory).")
    parser.add_argument("--output", default="requirements-1.txt", help="Uitvoerbestand (default: requirements.txt).")
    parser.add_argument("--pin", action="store_true", help="Versies pinnen als geinstalleerd in huidige omgeving.")
    args = parser.parse_args()

    py_files = discover_py_files(args.project_root)
    if not py_files:
        print("Geen .py-bestanden gevonden.", file=sys.stderr)
        sys.exit(1)

    imports: Set[str] = set()
    for f in py_files:
        imports |= collect_imports_from_file(f)

    # Filter stdlib
    third_party = {m for m in imports if not is_stdlib_module(m)}

    # Map naar PyPI namen
    pypi_pkgs = {map_to_pypi_name(m) for m in third_party}

    if args.pin:
        versions = pin_versions(pypi_pkgs)
    else:
        versions = {p: "" for p in pypi_pkgs}

    write_requirements(args.output, versions)
    print(f"Gegenereerd: {args.output}")
    print("Pakketten:")
    for pkg, ver in sorted(versions.items(), key=lambda kv: kv[0].lower()):
        print(f" - {pkg}{'==' + ver if ver else ''}")


if __name__ == "__main__":
    main()
