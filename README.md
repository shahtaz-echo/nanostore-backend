# Nanostore

E-commerce Backend with Python and Django

## Getting Started

Follow these steps to set up and run the project on your local machine.

### 1. Set Up a Virtual Environment

1. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

### 2. Configure Visual Studio Code

1. **Install the Python extension:** Make sure to install the Python extension in VS Code for better development experience.

2. **Set up the Python debugger:**
   - Open the VS Code terminal.
   - Configure the Python debugger to work with your virtual environment.

### 3. Set Up the Database

1. **Apply the initial migrations:**

   ```bash
   python manage.py migrate
   ```

2. **Create migrations for the `store` app and apply them:**
   ```bash
   python manage.py makemigrations store
   python manage.py migrate store
   ```

### 4. Create a Superuser

1. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

2. **Provide the required information:**

   - Use your email as the username.
   - Set a password.

3. **Access the Django admin panel:**
   - Go to `http://localhost:8000/admin`
   - Log in with your superuser credentials.

### 5. Run the Server Locally

1. **Start the development server:**

   ```bash
   python manage.py runserver
   ```

2. **Access the application:**
   - Open your browser and go to `http://localhost:8000`

---

This version is more structured and concise, making it easy for someone to follow the setup process.
