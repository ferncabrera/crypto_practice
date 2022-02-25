# Steps to run on local
This project was created using Anaconda as the primary package manager, thus the requirements.txt file is formatted to be read by an Anaconda interpreter and the steps will assume that you are also running Anaconda on your machine. Pip was used to install seperate packages within the environment accidentally for this project, will manually transfer all packages to those available through the conda in the future.
## What you need installed
### Anaconda
You can download it here: <br />
https://www.anaconda.com/products/individual
### Windows Subsystem for Linux (For Windows Users)
You may find that here <br />
https://docs.microsoft.com/en-us/windows/wsl/install
### SQLite & OPTIONALLY DB Browser for SQLite
SQLite: https://www.sqlitetutorial.net/download-install-sqlite/
<br/>
DB Browser for SQLite: https://sqlitebrowser.org/

## How to run
### Step 1: Clone repo
Clone this repository into a local directory on your machine. <br />
https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
<br />
### Step 2: Create python environment and install dependencies
Optionally, but highly recommnded, create an Anaconda environment for this project. <br/>
```
conda create --name your_env_name_here --file requirements.txt
```
Activate your environment:
```
conda activatr you_env_name_here
```
Then install all the pip packages into your Anaconda env from the pip.txt file. <br />
```
pip install -r pip.txt
```
Congrats, you have all the required packages inside your environments!
### Step 3: Set-up db
While in the root of the directory where you cloned the repo, run
```
alembic init alembic
```
This will create your alembic migration environment. You then need to change two pieces of code within some of these files.
<br />
Within /alembic/env.py add this import to the top of the file:
```
from models import Base
```
And change line 21 from:
```
target_metadata = None
```
to:
```
target_metadata = Base.metadata
```
Then, in alembic.ini, change line 51 from:
```
sqlalchemy.url = sqlite://sqlite.com
```
to:
```
sqlalchemy.url = sqlite:///./cryp_practice.db

```
Congrats, your db should not be set-up!
### Step 4: Run the program!
While in the root of the directory where the repo was cloned, run 
```
uvicorn main:app --reload
```
Enjoy!
