# BreastCare Pro - Backend API

Backend API for breast cancer screening platform using FastAPI and machine learning.

## Features

- **Mammography Analysis**: AI-powered BI-RADS classification
- **Risk Assessment**: Personalized breast cancer risk calculation
- **Patient Management**: Complete patient record system
- **Professional Directory**: Healthcare provider management
- **Authentication**: JWT-based user authentication
- **File Upload**: Secure mammography image handling

## Tech Stack

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **PostgreSQL**: Primary database
- **TensorFlow**: Machine learning model inference
- **JWT**: Authentication tokens
- **Pydantic**: Data validation

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   python app/db/init_db.py
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/           # API routes and endpoints
│   ├── core/          # Core configuration and security
│   ├── db/            # Database configuration
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   └── ml/            # Machine learning models
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `GET /api/v1/auth/me` - Get current user

### Mammography Analysis
- `POST /api/v1/mammography/analyze` - Analyze mammography images
- `GET /api/v1/mammography/analysis/{id}` - Get analysis result
- `GET /api/v1/mammography/history/{patient_id}` - Get patient history

### Risk Assessment
- `POST /api/v1/risk/calculate` - Calculate breast cancer risk
- `GET /api/v1/risk/factors` - Get risk factors information

### Patient Management
- `POST /api/v1/patients/` - Create patient
- `GET /api/v1/patients/{id}` - Get patient
- `PUT /api/v1/patients/{id}` - Update patient
- `GET /api/v1/patients/` - List patients

### Healthcare Professionals
- `POST /api/v1/professionals/` - Create professional
- `GET /api/v1/professionals/{id}` - Get professional
- `GET /api/v1/professionals/nearby` - Find nearby professionals
- `GET /api/v1/professionals/` - List professionals

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
flake8 .
```

### Database Migrations
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## Deployment

### Docker
```bash
docker build -t breastcare-api .
docker run -p 8000:8000 breastcare-api
```

### Production
- Use PostgreSQL database
- Set secure SECRET_KEY
- Configure CORS origins
- Set up SSL certificates
- Use process manager (PM2, systemd)

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

This project is licensed under the MIT License.
