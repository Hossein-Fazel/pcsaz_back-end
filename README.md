# pcsaz_back-end

## How To Run
1. Open a terminal and clone the repository.
2. Navigate to the `pcsaz_back-end` directory.
3. Run the following command to install all dependencies:
```bash
pip install -r requirements.txt
```
4. Make a copy of `config_example.json` in the current directory and name it `config.json`.
5. Edit the `config.json` and replace your own database settings.
6. use this command to run server:
```bash
python manage.py runserver
```
This command runs your server on the address 127.0.0.1 and port 8000. If you want to change it, you can use the command below (replace the address and port with the ones you want):
```bash
python manage.py runserver address:port
```