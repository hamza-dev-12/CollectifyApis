# CollectifyApis ⚙️🧠 — Backend (Django + Gemini)

This is the backend of **Collectify** — a smart, AI-powered system that automates the collection of building maintenance fees and enables intelligent natural language queries through Google's Gemini model.

👉 **Frontend Live Demo:** [https://collectify-ui.vercel.app](https://collectify-ui.vercel.app)  
👉 **Frontend Repository:** [Collectify Frontend](https://github.com/hamza-dev-12/collectify-frontend)

---

## 🌐 Overview

CollectifyApis provides a powerful RESTful API built with Django and Django REST Framework, designed to:
- Manage buildings (groups), members, and payment statuses
- Enable secure user authentication and access control
- Power analytics and payment summaries
- Integrate with **Gemini** for natural language interactions via a smart chat interface

---

## 🌟 Key Features

- 🔐 **User Authentication & JWT Tokens**
- 🏢 **Group & Member Management**
- 💳 **Track Paid vs. Pending Status**
- 📊 **Payment Summaries & Analytics APIs**
- 🧠 **Smart Chat** — Natural language interface using **Gemini**
- 🌍 **CORS-enabled** for frontend integration
- 🗃️ **PostgreSQL** as primary database (compatible with local and cloud like NeonDB)

---

## 🤖 Gemini-Powered Smart Chat

A standout feature of this backend is its **Smart Chat interface**, allowing group admins to ask natural language questions like:

- "Who hasn’t paid this month?"
- "How much total payment is pending?"

This is achieved using **Google's Gemini API**, which processes the question, understands group context, and returns meaningful insights via structured responses.

---

## 🧠 Motivation

Manually managing building maintenance records is time-consuming and error-prone. With CollectifyApis, we automate the backend processes — allowing users to manage everything via intuitive APIs and even communicate with their data using natural language.

---

## 🛠️ Tech Stack

- **Framework:** Django, Django REST Framework
- **Authentication:** JWT (via djangorestframework-simplejwt)
- **Database:** PostgreSQL [Deployed on Neon]
- **AI Integration:** Google Gemini (via `google-genai`)
- **Deployment Ready:** Compatible with Docker and serverless architecture (e.g., AWS Lambda)
- **CORS & Middleware:** Enabled for cross-origin frontend integration

---

## 📂 Project Structure

```
CollectifyApis/
│
├── apis/
│   ├── routes/                 # DRF Routers organized by feature
│   │   ├── chat.py
│   │   ├── detail.py
│   │   ├── member.py
│   │   ├── payment.py
│   │   └── user.py
│   │
│   ├── views/                  # API views for each feature
│   │   ├── chat.py
│   │   ├── detail.py
│   │   ├── group.py
│   │   ├── member.py
│   │   ├── payment.py
│   │   └── users.py
│   │
│   ├── __init__.py
│
├── models.py                  # Data models: Group, Member, Payment, etc.
├── serializers.py             # DRF serializers
├── urls.py                    # Project-level URL configuration

```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/hamza-dev-12/CollectifyApis.git
cd CollectifyApis
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure `.env` for environment variables

```env
DATABASE_URL=your-postgres-db-url [Neon]
GOOGLE_API_KEY=your-gemini-api-key
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

---



## 🔗 Related Repositories

- **Frontend:** [Collectify (React + Vite)](https://github.com/hamza-dev-12/collectify-frontend)



---

## 🧠 Gemini Integration Notes

We're using `google-genai` to integrate Gemini. The model parses context + user questions to return intelligent answers about group data. You’ll need an API key from Google AI Studio to run this feature.

---

## 👤 Author

**Muhammad Hamza**  
GitHub: [@hamza-dev-12](https://github.com/hamza-dev-12)

---
