# Chat App – Real-Time Messaging Application

This is a simple real-time chat application built using Django and Django Channels.  
Users can register, log in, and chat with each other in real time using WebSockets.

The project follows Django's MVT (Model-View-Template) architecture and uses SQLite as the database.

---

## Technologies Used

- Python
- Django
- Django Channels
- SQLite
- HTML, CSS, JavaScript
- Bootstrap

---

## Setup Steps

1. Clone this repository:

   git clone https://github.com/Hanaaan19/chat-app.git

2. Go inside the project folder:

   cd chat-app

3. Create a virtual environment:

   For Windows:
   python -m venv env  
   env\Scripts\activate  

   For Mac/Linux:
   python3 -m venv env  
   source env/bin/activate  

4. Install the required packages:

   pip install -r requirements.txt

5. Create a `.env` file in the project root and add the following:

   SECRET_KEY=your_secret_key  
   DEBUG=True  
   ALLOWED_HOSTS=127.0.0.1,localhost  

6. Run database migrations:

   python manage.py migrate

---

## Installation Instructions

Make sure Python is installed on your system.  
Then create and activate a virtual environment before installing dependencies.

All required packages are listed in `requirements.txt`.  
Install them using:

   pip install -r requirements.txt

---

## How to Run the Project

Since this project uses Django Channels, it should be run using Daphne:

   daphne chat_app.asgi:application

After running the above command, open your browser and go to:

   http://127.0.0.1:8000

You can register a new user account and start chatting.

---

## Features

- User registration and login
- Email-based authentication
- Online / Offline status
- Last seen display
- Real-time chat using WebSockets
- Message read receipts (✓ / ✓✓)
- Typing indicator
- Unread message count
- Delete own messages

---

## Project Structure

- Models – Defines database tables (CustomUser, Message)
- Views – Handles HTTP requests
- Templates – UI rendering
- Consumers – WebSocket handling logic

Business logic is handled in views and consumers, not in templates.

---

## Author

Developed by Hanan.