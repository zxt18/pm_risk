

# Setup Instructions

## 1. Create and activate a virtual environment

```bash
# This project was coded using Python version 3.12.2, assuming you're using a unix machine, the commands are as below
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## MAKEFILE
### Key scripts for running the server, generating/running migrations, and producing sample data are defined in the Makefile.

Run the following in order:

```
make migrations (Create DB migrations)

make migrate (Run migrations)

make dummy-data (Generate sample data)

make runserver (Runs dev server)
```

Your website will be live at:

http://127.0.0.1:8000/

### To login 
1) Create a superuser using (python manage.py createsuperuser)
2) http://127.0.0.1:8000/admin (for admin page to configure Books and read/edit permissions)
