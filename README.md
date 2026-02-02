# Playto Feed - Community Feed Prototype

This is a "Community Feed" prototype built for the Playto Engineering Challenge.  
Users can create posts, comment, reply in threads, like posts/comments, and earn Karma.  
A dynamic leaderboard shows the top 5 users in the last 24 hours.

---

## Features

- **Feed:** Display posts with author and like count.
- **Threaded Comments:** Nested comments and replies.
- **Likes & Karma:**
  - 1 Like on a post = 5 Karma points.
  - 1 Like on a comment = 1 Karma point.
- **Leaderboard:** Top 5 users by Karma in the last 24 hours.
- **Double-like Prevention:** Users cannot like a post/comment twice.
- **Atomic Like Logic:** Race conditions handled using database transactions.

---

## Tech Stack

- **Backend:** Django & Django REST Framework (DRF)
- **Frontend:** Django templates
- **Database:** SQLite (default)  
- **Python Version:** 3.13+

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone <your_repo_url>
cd playto
Create virtual environment & activate

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
Install dependencies

pip install -r requirements.txt
Run migrations

python manage.py migrate
Create a superuser (for testing/admin purposes)

python manage.py createsuperuser
Start the development server

python manage.py runserver
Visit http://127.0.0.1:8000/ in your browser.
