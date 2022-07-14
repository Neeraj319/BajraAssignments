# Run the project 

```bash
git clone https://github.com/Neeraj319/BajraAssignments
```

```bash
cd BajraAssignments
```
```bash
cd Database
```

## Install dependencies 

### With poetry 
- Only if you have poetry installed on your system 

```bash
poetry lock 
```

```
poetry install 
```

```
poetry shell
```

### Without poetry 
Create a virtual environment

```bash
python -m venv env
```

```bash
source env/bin/activate
```
```bash
pip install -r requirements.txt
```
## create env vars
- Create .env file and add vars according to .env.example file
## Initialize the database 
Create a postgres database and add its url to .env file
- Run only once
```
python db_init.py initialize
```
```
python app.py
```

