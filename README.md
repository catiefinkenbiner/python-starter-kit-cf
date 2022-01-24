# Python Starter Kit
## Goals
- Standardize repository structure within Customer Success
- Encourage the use of virtual environments
- Enforce PEP-8 coding standards with as little burden as possible

## Features

### Environment setup
Scripts for quick virtual environment setup (`create-venv.py`) and python dependency installation (`install.py`) are provided. See the Instructions section below for details.

### Invoke functions
Useful development functions are defined in `tasks.py` and available using the `invoke` command.
- `invoke lint`: This command uses `flake8` to report linting errors in your code.
- `invoke format`: This command uses `black` to report any formatting issues in your code. 
   - `invoke format --diff`: This command will report any formatting issues in your code and include a diff between your current code and the recommended code.
   - `invoke format --fix`: This command will automatically fix formatting issues in your code.
- `invoke test`: This command uses `pytest` to run the tests you have written for your code. 

### Continuous Integration
Using this template will automatically add integration checks to pull requests against your repository. These are defined in the ".github" directory. By default, `invoke format` and `invoke lint` are run against every pull request.

### GitIgnore
In addition to ignoring common nuisance files types, all files within the "data" directory are ignored as GitHub should not manage data. Similarly, all files within the "conf" directory are ignored unless they end with ".template". Only configuration templates should be managed by GitHub. True configuration values should be stored in a copy of these files with ".template" removed from their name.  


## Instructions
1. Create a new repository using this template. Use the green "Use this template" button on GitHub.
   - Detailed instructions available here: https://help.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template
   - Note: Repositories for customer projects should follow the pattern "customer-<MY-CUSTOMER-NAME>"

2. Clone your newly created repository to your local machine
   - ```git clone git@github.com:Datatamer/<MY-REPO-NAME>.git```

3. Update the "README.md" file in your new repository
   - If you can still see this text in your repository, you should edit it to something specific about your project!

4. Create and enter a virtual environment
   - Create a new environment using ```python3 create-venv.py``` to use the default name or ```python3 create-venv.py my-venv-name``` to use a custom name. 
   - Enter the environment using ```source <venv-name>/bin/activate```. The default environment name is ```.venv-<MY-REPO-NAME>```.
   - When you want to exit the environment, use `deactivate`.

5. Install repository dependencies
   - ```python install.py```
   - This script installs the dependencies listed in `requirements.txt` and `dev-requirements.txt`. As you develop your repository, add any additional dependencies needed for your scripts to `requirements.txt` and any additional dependencies needed for your tests to `dev-requirements.txt`. Then re-run the install command to install your newly added dependencies.
   - You can also update the versions of tamr-client and tamr-toolbox to latest version available

6. Add your own code to the repository
   - Your main code should be placed in the "scripts" directory.
   - Tests for your code should be placed in the "tests" directory.
   - Configuration files on which your code depends should be placed in the "conf" directory.
   - Data files on which your code depends should be placed in the "data" directory.