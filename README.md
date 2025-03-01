# Project Setup Guide

Made By - BOLOGO ([Bionluk Profile](https://bionluk.com/bologo))

Follow these steps to set up the project:

1. **Create a virtual environment**  
   First, create a virtual environment to isolate your project's dependencies. Command:
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**  
   Activate the virtual environment that you created earlier.
   ```bash
   .venv\Scripts\activate
   ```

2. **Install requirements**  
   Download and install the required packages by running the following command:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**  
   Run the following command to apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. **Collect static files**  
   Use the following command to collect static files:
   ```bash
   python manage.py collectstatic
   ```

6. **Seed the database**  
   Seed the database with initial data by running:
   ```bash
   python manage.py seed_data
   ```

7. **Start the development server**  
   Run the server with the following command:
   ```bash
   python manage.py runserver
   ```

8. **Setting env file**  
   Copy the .env-example file and rename it .env. Configure the information in it according to your own settings

9. **Access the admin panel**  
   Open your browser and navigate to:
   ```plaintext
   http://127.0.0.1:8000/admin/
   ```

10. **Login credentials**  
   Default username: `admin`  
   Default password: `1`

11. **Change the default password**  
    Don’t forget to change the default password after logging in for security purposes.

12. **Default Tour Urls**  
   Default Two Hour Tour URL: `http://127.0.0.1:8000/tours/twohour/en/`  
   Default Three Hour Tour URL: `http://127.0.0.1:8000/tours/threehour/en/`
   Admin Panel URL: `http://127.0.0.1:8000/admin/`

---

Feel free to adjust anything based on your project!#   g u i d e  
 