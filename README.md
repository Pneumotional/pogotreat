
# Vendor Management System

This Vendor Management System allows businesses to efficiently manage vendor applications, sales, and commissions. It provides a seamless interaction between vendors and administrators, ensuring transparency and control over transactions.

## Key Features

### Vendor Dashboard:
- **Vendor Application**: Vendors can apply for approval to sell products or services on the platform.
- **Sales Submission**: Vendors can submit details of their sales, which await admin approval.
- **Commission Withdrawal Requests**: Vendors can request to withdraw earned commissions, pending admin approval.
- **Sales Summary**: Vendors can view a detailed summary of:
  - Total sales made
  - Total commissions earned
  - Number of items sold

### Admin Dashboard:
- **Vendor Approval**: Admins can view and approve vendor applications.
- **Sales Approval**: Admins can review and approve sales submitted by vendors.
- **Commission Withdrawal Approval**: Admins manage and approve commission withdrawal requests.
- **Vendor Management Overview**:
  - Number of active vendors
  - Total sales made across all vendors
  - Total items sold across all vendors
- **Pending Requests**: Quick view of pending sales and commission withdrawal requests.
- **Commission & Sale Rate Management**: Admins can set the commission rate and item sale rate for vendors.

### Authentication:
- **Role-based Access Control**: Both vendors and admins have separate authentication mechanisms to ensure secure access.

This system offers an intuitive interface for both vendors and admins, providing detailed control over sales tracking and commission management.



Sure! Here's a guide for running your Django project using Docker.

---

# How to Run the Project Using Docker

### Prerequisites:
- Docker installed on your machine
- Docker Compose installed on your machine

### Step 1: Clone the Project Repository

```bash
git clone https://github.com/Pneumotional/python-django-vendor_management_system.git
cd python-django-vendor_management_system
```


### Step 2: Build Docker Containers

In the root directory of the project, there should be a `docker-compose.yml` file that defines how the Docker containers are set up. To build and start the containers, run:

```bash
docker-compose up --build
```

This will:
- Build the Docker image based on the Dockerfile.
- Set up all necessary services (e.g., the web service for Django and any other services you may have).
- Start the Django development server.

If you want to run the containers in the background (detached mode), use:

```bash
docker-compose up --build -d
```

### Step 3: Apply Database Migrations

Once the containers are up, you need to apply Django's migrations to set up the database schema:

```bash
docker-compose exec web python manage.py migrate
```

### Step 4: Create a Superuser (Optional)

To create a Django superuser for accessing the Django admin interface, run the following command:

```bash
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts to enter your superuser details.


### Step 5: Access the Application

Now, your Django app should be running. Open your browser and go to:

```
http://localhost:8000
```

### Step 8: Stopping the Application

To stop the running containers, press `CTRL+C` in the terminal if you are running them in the foreground, or if running in detached mode, use:

```bash
docker-compose down
```

This command will stop and remove the containers.

---

### Additional Docker Commands

- **Check Logs:**

  To see logs from the `web` container, run:

  ```bash
  docker-compose logs web
  ```

- **Rebuild Containers:**

  If you make changes to the `Dockerfile` or `docker-compose.yml`, rebuild the containers with:

  ```bash
  docker-compose up --build
  ```

---
