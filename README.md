# Topic-Trek

A Django-based social media feed application that allows users to interact and share content.

## 👨🏻‍💻 Functionalities
# Super User Role 
|            | Enter the admin panel and edit/delete data | Follow/Unfollow other users, Like/Dislike their topics and leave comments  | Post topics, edit your own topics and comments | Edit your profile | 
|------------|--------------------------------------------|----------------------------------------------------------------------------|------------------------------------------------|-------------------|
|Super User  |                 [x]                        |                               [x]                                          |                [x]                             |         [x]       |
|Normal User |                 [ ]                        |                               [x]                                          |                [x]                             |         [x]       |

## 🚀 Getting Started
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/yourusername/social-media-feed.git
cd social-media-feed
```

### **2️⃣ Create a Virtual Environment (Recommended)**
```sh
python3 -m venv venv
source venv/bin/activate
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Run Database Migrations**
```sh 
python main.py makemigrations
python main.py migrate 
```

### **5️⃣ Create a Superuser (Admin Panel)**
```sh
python main.py createsuperuser
```
Open *http://127.0.0.1:8000/admin* in your browser when you run the server to enter the admin panel

### **6️⃣ Start the Development Server**
```sh
python main.py runserver
```
Visit *http://127.0.0.1:8000/* in your browser.

## 🧪 Running Tests
```sh
python3 main.py test
```

## 🛠 Technologies Used
* Django – Backend framework
* Bootstrap – Frontend styling
* SQLite – Default database (can be changed)