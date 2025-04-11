**Deployment Guide**

---

## **Method 1: Bare-Metal Deployment (Using Virtual Environment)**

### **1. Pre-Requisites Installation**
Before starting, ensure the following dependencies are installed on the server:

```sh
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git curl redis nginx awscli
```

#### **Expected Result:**
- Python 3, pip, virtual environment, Redis, and Nginx should be installed successfully.
- Running `python3 --version` should return a valid Python version.
- Running `redis-server --version` should return a valid Redis version.

### **PostgreSQL Installation**
```sh
sudo apt install -y postgresql postgresql-contrib
```

#### **Expected Result:**
- Running `psql --version` should return the installed version.

---

### **2. Clone the Repository**
Navigate to the deployment directory and clone the GitHub repository:

```sh
cd /home/administrator/
git clone https://github.com/neudeeptech/CameraHealth_backend.git CHBE
cd CHBE
```

#### **Expected Result:**
- The project should be cloned into `/home/administrator/CHBE`.
- Running `ls` inside `CHBE` should list the project files.

---

### **3. Setup Virtual Environment & Dependencies**
Run the deployment script to set up the virtual environment and install dependencies:

```sh
chmod +x scripts/start.sh  # Ensure the script is executable
bash scripts/start.sh
```

#### **Expected Result:**
- A new virtual environment should be created at `/home/administrator/CHBE/.venv`.
- Dependencies should be installed without errors.

---

### **4. Start Backend Services**
The start script will:
- Set up a virtual environment.
- Install dependencies.
- Stop any running Gunicorn, Celery, and WebSocket processes.
- Start Gunicorn, Celery, and WebSocket servers.

#### **Verify Running Services:**
```sh
ps aux | grep -E "gunicorn|celery|ip_sub.py|save_ai_rating.py|web_socket_server.py"
```

#### **Expected Result:**
- Gunicorn should be running on port **8000**.
- Celery worker, AI subscriber, and WebSocket server should be active.


# Activate the virtual environment
source /home/administrator/CHBE/.venv/bin/activate  

# Export environment variables (if required)
export $(grep -v '^#' .env | xargs)

# Navigate to the application directory
cd /home/administrator/CHBE/app  

# Run the Celery task
celery -A app call schedules.schedules_tasks.schedule_task_checker  


---


## **Method 2: Docker-Based Deployment**

### **1. Pre-Requisites Installation**
```sh
sudo apt update && sudo apt install -y git curl docker.io docker-compose
sudo systemctl enable docker --now
```

#### **Expected Result:**
- Running `docker --version` should return the installed version.
- Running `docker-compose --version` should return the installed version.

---

### **2. Clone the Repository**
```sh
cd /home/administrator/
git clone https://github.com/neudeeptech/CameraHealth_backend.git CHBE
cd CHBE
```

#### **Expected Result:**
- The project files should be available inside `/home/administrator/CHBE`.

---

### **3. Create `.env` File**
Copy the example `.env` file and modify it:
```sh
cp .env.example .env
nano .env
```

---

### **4. Build and Run the Docker Containers**
```sh
docker-compose up --build -d
```

# one time run below command 
docker exec -it neudeep_celery_app celery -A app call schedules.schedules_tasks.schedule_task_checker


#### **Verify Running Containers:**
```sh
docker ps
```

#### **Expected Result:**
- The application backend should be running inside a Docker container.
- Running `docker ps` should list Gunicorn, Celery, Redis, and WebSocket containers.
- The backend should be accessible via `http://yourdomain.com`.
- The React frontend should be accessible at `http://yourdomain.com`.
- Running `docker ps` should list the frontend container.

---

### **Final Checklist: Successful Deployment Confirmation**
✅ The backend should be accessible via `http://yourdomain.com/api/` (or configured endpoint).
✅ The frontend should be accessible via `http://yourdomain.com`.
✅ `docker ps` should list all running containers (if using Docker).
✅ `ps aux | grep gunicorn` should confirm Gunicorn is running (for bare-metal setup).
✅ `systemctl status nginx` should confirm that Nginx is running.

---

**Deployment Completed Successfully! 🎉**

-------------------- Extra ----------------------------------
First, create an admin user (superuser):
Run the following command to create a superuser:

clear && docker compose run --rm app sh -c "python manage.py createsuperuser"


Login to the admin panel and complete the following setup:

In the "Recording Policy Days" section, add a new entry for Recording Policy Days.

Then, go to the Device Types section and add the following:

nvr
hikvision


Import CSV files in the admin panel.
In the API Endpoints section, import the CSV file (Example, APIEndpoint-2025-04-10.csv).


