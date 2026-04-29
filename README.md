#  KasaUp Marketplace 

KasaUp is a premium **full-stack service marketplace** designed to connect local service providers with customers through a sleek, modern, and high-performance interface.

---

## Features & Highlights

- **Advanced Authentication**: Secure JWT session management with **GitHub OAuth** integration.
- **Role-Based Portals**: Tailored experiences for Customers, Service Providers, and Administrators.

- **Map-Based Discovery**: Intuitive provider discovery using interactive maps and location services.
- **Built-in Chat**: Direct real-time communication between customers and providers.
- **Automated CI/CD Pipeline**: Streamlined and reliable deployments powered by **GitHub Actions**.


---

## 🛠️ Tech Stack

### **Frontend**
- **Framework**: [Vue 3](https://vuejs.org/) (Composition API)
- **Build Tool**: [Vite](https://vitejs.dev/)
- **Styling**: Vanilla CSS (Premium Glassmorphism Design)
- **State Management**: [Pinia](https://pinia.vuejs.org/)
- **Routing**: Vue Router

### **Backend**
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Security**: JWT tokens, bcrypt hashing, and HTTP-only cookies.

---

##  Project Structure

```bash
KasaUp/
├── frontend/          # Vue 3 + Vite application
│   ├── src/
│   │   ├── components/  # Reusable UI elements (Sidebar, etc.)
│   │   ├── views/       # Role-specific pages (Customer, Provider, Admin)
│   │   ├── stores/      # Pinia state management
│   │   └── hooks/       # Custom Vue composables (useScroll, etc.)
└── backend/           # FastAPI application
    ├── app/
    │   ├── routers/     # API Endpoints
    │   ├── services/    # Business logic (Auth, Bookings, OAuth)
    │   ├── models/      # SQLAlchemy DB models
    │   └── schemas/     # Pydantic validation models
```

---

##  Getting Started

### **1. Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt
# Configure your .env file
uvicorn app.main:app --reload
```

### **2. Frontend Setup**
```bash
cd frontend
npm install
# Configure your .env.local file
npm run dev
```



---

##  License

This project is currently under active development.
**Deployment Heartbeat**: Updated for 2026 Production Standards.
