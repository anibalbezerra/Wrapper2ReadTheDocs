# Wrapper2ReadTheDocs
This is a basic Python wrapper that parses the structure of a github repository and creates the basic required folders, and files to allow for the use of the ReadTheDocs service.

After running the code, remember to remove ciclic references to project's modules from both `requirements.txt` and `setup.py`. This will avoid problems during the compiling of the "ReadTheDocs". Sometimes, basic packages from Python like `os`, `time`, and others are added to those files, based on the Python modules within the project. This would cause a crash during compiling of the website. Remove them acoordinly.

If the project's modules are object-oriented it is required to add, together with those modules folder, a simple `__init__.py` file, that can be empty. This will trigger, however, the generation of a corresponding `__init__.rst` file that will be added to the contents list of the generated website. You could simply keep it there or, if it bothers you, remove the file and update the repository.
