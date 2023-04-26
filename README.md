# LibraryPractice
Library API is a powerful API for managing library. It provides borrowing, customers and payment management, and notifications in Telegram.

## Installing / Getting started

### Since Celery has many constraints with Windows, we are using dockerization

`Python3 must be already installed`
```
git clone https://github.com/AndereLion/LibraryPractice.git
python -m venv venv
source venv/bin/activate  # On macOS
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

Inside base location and library_bot location provide your env values to .env file accordingly to env.sample.

```
python manage.py migrate
python manage.py runserver
docker-compose up
docker ps
docker exec -it bash
python manage.py createsuperuser

endpoints overview are available via localhost/app/swagger/doc
```

## Features

Check out our features!

**Books Service:**

Managing books amount (CRUD for Books).

API:
```
POST:        books/        - add new book
GET:         books/        - get a list of books
GET:         books/<id>/   - get book's detail info 
PUT/PATCH:   books/<id>/   - update book (also manage inventory)
DELETE:      books/<id>/   - delete book
```

**Users Service:**

Managing authentication & user registration.

API:
```
POST:        users/                 - register a new user 
POST:        users/token/           - get JWT tokens 
POST:        users/token/refresh/   - refresh JWT token 
GET:         users/me/              - get my profile info 
PUT/PATCH:   users/me/              - update profile info
```


**Borrowings Service:**

Managing users borrowings of books.

API:
```
POST:   borrowings/                            - add new borrowing 
GET:    borrowings/?user_id=...&is_active=...  - get borrowings by user id and whether is borrowing still active or not.
GET:    borrowings/<id>/                       - get specific borrowing 
POST:   borrowings/<id>/return/                - set actual return date
```


**Notifications Service (Telegram):**

Send notifications to users in Telegram. It includes notifications about new borrowing, borrowing overdue or/and successful payment.


**Payments Service (Stripe):**

Perform payments for book borrowings through the platform.

API:
```
GET:   success/   - check successful stripe payment
GET:   cancel/    - return payment paused message 
```
### Telegram bot

Check out Telegram bot: [Library bot](https://t.me/LibraryNotificationBot)

**How to use bot:**
1. Add bot to your Telegram channel
2. Make bot admin of your channel
3. Provide channel id to .env file in library_bot location
