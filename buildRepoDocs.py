import os
import subprocess
import shutil
import ast

# Configuration
repo_url = "https://github.com/anibalbezerra/<repo>r.git"
repo_name = "<repo>"
projectname = "<repo name>"
author = "<author>"
year = "<year>"
docs_folder = "docs"
src_folder = "src"

# Clone the repository
def clone_repo():
    if os.path.exists(repo_name):
        print(f"Repository {repo_name} already exists. Skipping clone.")
    else:
        subprocess.run(["git", "clone", repo_url])
        print(f"Cloned repository: {repo_name}")

# Convert README.md to README.rst
def convert_readme_to_rst():
    readme_md_path = "README.md"
    readme_rst_path = os.path.join(docs_folder, "README.rst")
    if os.path.exists(readme_md_path):
        subprocess.run(["pandoc", readme_md_path, "-o", readme_rst_path])
        print(f"Converted README.md to README.rst: {readme_rst_path}")
    else:
        print("README.md not found. Skipping conversion.")

# Inspect the repository and create documentation structure
def create_docs_structure():
    if not os.path.exists(repo_name):
        print(f"Repository {repo_name} not found. Please clone the repository first.")
        return

    os.chdir(repo_name)

    # Create the docs folder if it doesn't exist
    if not os.path.exists(docs_folder):
        os.makedirs(docs_folder)
        print(f"Created {docs_folder} folder.")

    # Convert README.md to README.rst
    convert_readme_to_rst()

    # Create the source folder structure
    if os.path.exists(src_folder):
        for root, dirs, files in os.walk(src_folder):
            for file in files:
                if file.endswith(".py"):
                    module_path = os.path.join(root, file)
                    module_name = os.path.splitext(file)[0]
                    module_doc_path = os.path.join(docs_folder, module_name + ".rst")

                    # Create a .rst file for each module
                    with open(module_doc_path, "w") as f:
                        f.write(f".. _{module_name}:\n\n")
                        f.write(f"{module_name}\n")
                        f.write("=" * len(module_name) + "\n\n")
                        f.write(f".. automodule:: {os.path.relpath(module_path, src_folder)}\n")
                        f.write("   :members:\n")
                        f.write("   :undoc-members:\n")
                        f.write("   :show-inheritance:\n\n")

                        # Add autoclass directives for each class in the module
                        with open(module_path, "r") as py_file:
                            for line in py_file:
                                if line.startswith("class "):
                                    class_name = line.split()[1].split("(")[0]
                                    f.write(f".. autoclass:: {os.path.relpath(module_path, src_folder)}.{class_name}\n")
                                    f.write("   :members:\n")
                                    f.write("   :undoc-members:\n")
                                    f.write("   :show-inheritance:\n\n")

                    print(f"Created documentation file: {module_doc_path}")

    # Create the index.rst file
    index_path = os.path.join(docs_folder, "index.rst")
    with open(index_path, "w") as f:
        f.write(f"{projectname}\n")
        f.write("============================\n\n")
        #f.write(f"Welcome to the Documentation\n")
        #f.write("============================\n\n")
        f.write(".. toctree::\n")
        f.write("   :maxdepth: 2\n")
        f.write("   :caption: Contents:\n\n")

        # Include README.rst as the initial page
        f.write("   README\n\n")

        if os.path.exists(src_folder):
            for root, dirs, files in os.walk(src_folder):
                for file in files:
                    if file.endswith(".py"):
                        module_name = os.path.splitext(file)[0]
                        f.write(f"   {module_name}\n")

        f.write("\nIndices and tables\n")
        f.write("==================\n\n")
        f.write("* :ref:`genindex`\n")
        f.write("* :ref:`modindex`\n")
        f.write("* :ref:`search`\n")

    print(f"Created index file: {index_path}")

    # Create the conf.py file
    conf_path = os.path.join(docs_folder, "conf.py")
    with open(conf_path, "w") as f:
        f.write("import os\n")
        f.write("import sys\n")
        f.write(f"sys.path.insert(0, os.path.abspath('{os.path.relpath(src_folder, docs_folder)}'))\n\n")
        f.write(f"project = '{projectname}'\n")
        f.write(f"copyright = '{year}, {author}'\n")
        f.write(f"author = '{author}'\n\n")
        f.write("extensions = [\n")
        f.write("    'sphinx.ext.autodoc',\n")
        f.write("    'sphinx.ext.napoleon',\n")
        f.write("    'sphinx.ext.viewcode',\n")
        f.write("    'sphinx.ext.autosummary',\n")
        f.write("]\n\n")
        f.write("napoleon_google_docstring = True\n")
        f.write("napoleon_numpy_docstring = True\n")
        f.write("napoleon_include_init_with_doc = False\n")
        f.write("napoleon_include_private_with_doc = False\n")
        f.write("napoleon_include_special_with_doc = True\n")
        f.write("napoleon_use_admonition_for_examples = False\n")
        f.write("napoleon_use_admonition_for_notes = False\n")
        f.write("napoleon_use_admonition_for_references = False\n")
        f.write("napoleon_use_ivar = False\n")
        f.write("napoleon_use_param = True\n")
        f.write("napoleon_use_rtype = True\n\n")
        f.write("html_theme = 'sphinx_pdj_theme'\n\n")
        f.write("html_static_path = ['_static']\n")

    print(f"Created conf.py file: {conf_path}")

    # Create the Makefile and make.bat files
    makefile_path = os.path.join(docs_folder, "Makefile")
    with open(makefile_path, "w") as f:
        f.write("html:\n")
        f.write("\tsphinx-build -b html $(SOURCEDIR) $(BUILDDIR)/html\n")
        f.write("\n")
        f.write("clean:\n")
        f.write("\trm -rf $(BUILDDIR)\n")

    print(f"Created Makefile: {makefile_path}")

    makebat_path = os.path.join(docs_folder, "make.bat")
    with open(makebat_path, "w") as f:
        f.write("@echo off\n")
        f.write("if \"%1\" == \"\" (\n")
        f.write("  echo Usage: make.bat [target]\n")
        f.write("  exit /b 1\n")
        f.write(")\n\n")
        f.write("set SOURCEDIR=.\n")
        f.write("set BUILDDIR=_build\n\n")
        f.write("if \"%1\" == \"html\" (\n")
        f.write("  sphinx-build -b html %SOURCEDIR% %BUILDDIR%/html\n")
        f.write("  exit /b 0\n")
        f.write(")\n\n")
        f.write("if \"%1\" == \"clean\" (\n")
        f.write("  if exist %BUILDDIR% rmdir /s /q %BUILDDIR%\n")
        f.write("  exit /b 0\n")
        f.write(")\n\n")
        f.write("echo Unknown target: %1\n")
        f.write("exit /b 1\n")

    print(f"Created make.bat: {makebat_path}")

    # Create the .readthedocs.yaml file
    readthedocs_path = ".readthedocs.yaml"
    with open(readthedocs_path, "w") as f:
        f.write("version: 2\n\n")
        f.write("build:\n")
        f.write("  os: ubuntu-22.04\n")
        f.write("  tools:\n")
        f.write("    python: \"3.9\"\n\n")
        f.write("python:\n")
        f.write("  install:\n")
        f.write("    - method: pip\n")
        f.write("      path: .\n")
        f.write("    - requirements: docs/requirements.txt\n\n")
        f.write("sphinx:\n")
        f.write("  configuration: docs/conf.py\n\n")
        f.write("formats:\n")
        f.write("  - pdf\n")
        f.write("  - epub\n")

    print(f"Created .readthedocs.yaml file: {readthedocs_path}")

    # Create the setup.py file
    setup_path = "setup.py"
    install_requires = get_install_requires()
    with open(setup_path, "w") as f:
        f.write("from setuptools import setup, find_packages\n\n")
        f.write("setup(\n")
        f.write(f"    name='{repo_name}',\n")
        f.write("    version='0.1',\n")
        f.write("    packages=find_packages(),\n")
        f.write("    install_requires=[\n")
        for req in install_requires:
            f.write(f"        '{req}',\n")
        f.write("    ],\n")
        f.write("    entry_points={\n")
        f.write("        'console_scripts': [\n")
        f.write("            # Define any console scripts here\n")
        f.write("        ],\n")
        f.write("    },\n")
        f.write(")\n")

    print(f"Created setup.py file: {setup_path}")

    # Create the requirements.txt file
    requirements_path = os.path.join(docs_folder, "requirements.txt")
    with open(requirements_path, "w") as f:
        f.write("sphinx\n")
        f.write("sphinx-pdj-theme\n")
        for req in install_requires:
            f.write(f"{req}\n")

    print(f"Created requirements.txt file: {requirements_path}")

    # Return to the original directory
    os.chdir("..")

def get_install_requires():
    """
    Extracts the required packages from the import statements in the Python files.

    Returns:
        set: A set of required packages.
    """
    install_requires = set()
    if os.path.exists(src_folder):
        for root, dirs, files in os.walk(src_folder):
            for file in files:
                if file.endswith(".py"):
                    with open(os.path.join(root, file), "r") as f:
                        print(os.path.join(root, file))
                        tree = ast.parse(f.read())
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for n in node.names:
                                    install_requires.add(n.name.split('.')[0])
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    install_requires.add(node.module.split('.')[0])
    # Remove standard library packages
    standard_libs = {'os', 'sys', 'math', 're', 'multiprocessing', 'logging', 'time'}
    install_requires -= standard_libs
    return install_requires

def remove_py_extension(rst_file_path):
    with open(rst_file_path, 'r') as file:
        content = file.read()

    # Replace occurrences of '.py' with an empty string
    modified_content = content.replace('.py', '')

    with open(rst_file_path, 'w') as file:
        file.write(modified_content)

def process_rst_files():
    doc_folder = os.path.join(repo_name, docs_folder)

    if not os.path.exists(doc_folder):
        print(f"The directory {doc_folder} does not exist.")
        return

    for root, dirs, files in os.walk(doc_folder):
        for file in files:
            if file.endswith('.rst'):
                rst_file_path = os.path.join(root, file)
                remove_py_extension(rst_file_path)
                print(f"Processed {rst_file_path}")

# Main function
def main():
    clone_repo()
    create_docs_structure()
    process_rst_files()

if __name__ == "__main__":
    main()
