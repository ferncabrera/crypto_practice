# About
Crypto practice is a solution for those who are wanting to track and maximize profits while minigating loss by focusing on tracking _specific, individual_ crypto currency trades. All the wallets online are overbuilt and a huge amount of external calculation is required to simply see if you are profiting or losing on a trade as they merge your coin holdings into one large pot and it becomes impossible to differentiate purchases made during different times spans. Crypto Practice simplifies this all by calculating exact loss or gain made per trade all while tracking your total history in a customizable wallet.

<br />

Enjoy tracking!

# Preview
## Homepage
Non-protected route
![image](https://user-images.githubusercontent.com/73137447/155801709-91177fd1-22b3-4fde-b7e8-2c8078ecc170.png)
## Search feature
Will return a match if any instance of the search string is found within the currency name (case-insensitive)
![image](https://user-images.githubusercontent.com/73137447/155802940-e23aeae7-ac06-4a31-96de-047122e899e0.png)
## Clicking on coins
![image](https://user-images.githubusercontent.com/73137447/155803039-a96d74d5-e174-4b7f-bad9-679bcf4c3519.png)
If signed in, will take you directly to your wallet and add a query parameter to the URL used to pre-populate the form used to purchase coins with the name of the coin you selected! (Otherwise, it will redirect you to the login page, as is common behaviour with all protected routes)
![image](https://user-images.githubusercontent.com/73137447/155803059-fa235a8d-5f09-4d2e-8085-95db08d95f9a.png)
## Alerts 
Will alert you when coins are not found or purchases do not go through
![image](https://user-images.githubusercontent.com/73137447/155803156-109ab527-e756-418b-bc61-cf19d63dfcd0.png)
![image](https://user-images.githubusercontent.com/73137447/155803177-b039bee1-98ef-4880-83e2-095f1149fc37.png)
## Buying coins
If a correct name is provided (case-insensitive), any positive integer amount of this coin can be purchased.
![image](https://user-images.githubusercontent.com/73137447/155803725-a2f35b4a-82ae-4f49-beb4-2482ce3f659e.png)
![image](https://user-images.githubusercontent.com/73137447/155803763-ada04872-44a4-4ae0-aefd-3d2f6202bd34.png)
## Selling coins
All your purchases can be sold, and from the UI you can see how much you have made/lost per purchase along with other calculated data.
The current prices all come from the public CoinGecko API, thanks to them! <3 <br />
https://www.coingecko.com/en/api
<br />
Your wallet will keep track of the total net gain/loss that you have made since trading on the account. Pictured is a wallet that has been in use for a lot of time.
![image](https://user-images.githubusercontent.com/73137447/155804702-3a1c3fd8-75f9-4b82-80e6-38ffa262a114.png)
After selling this bitcoin purchase, you can see that it is directly reflected in the wallet total.
![image](https://user-images.githubusercontent.com/73137447/155804722-81690e5f-d4d4-44b3-b782-9b96013d47a6.png)
## Wallet features
The wallet also includes a search feature for convienece, that functions exactly like it does on the landing page
![image](https://user-images.githubusercontent.com/73137447/155804953-34b76e69-d45e-4df2-8098-f6b2a08d62a7.png)
After click: <br />
![image](https://user-images.githubusercontent.com/73137447/155804978-81b09461-5996-4a81-94d4-a0a7cd43246b.png)
<br />
All similar coin purchases are ordered by groups for convienence, with varying statistics regarding your purchases.
![image](https://user-images.githubusercontent.com/73137447/155805085-e136fa09-75e1-4944-9e21-12a89b38f1e1.png)
## User functionality
Logout, login, and registration work as expected!
![image](https://user-images.githubusercontent.com/73137447/155805162-5274ee1c-3d9f-43a1-b82d-2268ebaf2f7c.png)
Register a new wallet
![image](https://user-images.githubusercontent.com/73137447/155805200-aff98631-c41d-4684-82b5-9edafdaf881f.png)
Cannot re-use emails or usernames
![image](https://user-images.githubusercontent.com/73137447/155805269-092ab7ce-d04a-43d5-9b42-c127a650a9ed.png)
 

# Steps to run on local
This project was created using Anaconda as the primary package manager, thus the requirements.txt file is formatted to be read by an Anaconda interpreter and the steps will assume that you are also running Anaconda on your machine. Pip was used to install seperate packages within the environment accidentally for this project (This was build in 2 days 0.0), will manually transfer all packages to those available through the conda in the future.
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
