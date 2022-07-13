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
## Initialize the database 
```bash
docker-compose up --build
```
- Run only once
```
python db_init.py initialize
```
```
python app.py
```

