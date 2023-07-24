# ARKA bot


![flake8 test](https://github.com/Prrromanssss/ARKA-bot/actions/workflows/python-package.yml/badge.svg)


## Contens
* [Deployment instructions](#deployment-instructions)
  * [Cloning project](#1-cloning-project-from-github)
  * [Activation venv](#2-creation-and-activation-venv)
  * [Requirements](#3-installation-all-requirements)
  * [.Env](#4-generate-file-with-virtual-environment-variables-env)
  * [Running](#5-running-project)
  * [Deployment](#6-deployment)
* [Examples](#examples)



## Deployment instructions

### 1. Cloning project from GitHub

1.1 Run this command
```commandline
git clone https://github.com/Prrromanssss/ARKA-bot.git
```

### 2. Creation and activation venv

2.1 First of all, from root directory run this command
```commandline
python -m venv venv
```
2.2 Then run this command to activate venv
#### Mac OS / Linux
```commandline
source venv/bin/activate
```
#### Windows
```commandline
.\venv\Scripts\activate
```

### 3. Installation all requirements

3.3 Run this command 
```commandline
pip install -r requirements.txt
```

### 4. Generate file with virtual environment variables (.env)

4.1 Generate file '.env' in root directory with structure specified in the 'examples/env_example.txt' file


### 5. Running project

5.1 Run this command
```commandline
python main.py
```

### 6. Deployment

6.1 This bot was deployed to heroku, but from November 28, free heroku Dynos no longer available :(


## Examples

You can find some examples in the examples folder.
