# CustomerChurnPredictor - Predictive Customer Analytics Engine

CustomerChurnPredictor is an enterprise-grade predictive analytics platform designed to help businesses identify customers likely to churn. It provides business analysts, marketing teams, and customer success managers with actionable risk insights and real-time dashboard monitoring.

## Features
- **Machine Learning**: Custom PyTorch neural network predicting customer churn probability.
- **Data Pipeline**: Automated data ingestion, cleaning, scaling, and one-hot encoding.
- **Dashboard**: Real-time KPI metrics, risk distributions, and historical charts.
- **Customer Directory**: Searchable, paginated, and filterable high-risk customer tables.
- **Predictions API**: Single customer and batch CSV predictions.
- **MySQL Integration**: Persistent storage of customers, predictions, and model metadata.
- **Synthetic Data Generation**: Option to scale the dataset for load-testing and demonstration purposes beyond the base IBM dataset.

## Technology Stack
- **Frontend**: React (Vite), TypeScript, Tailwind CSS, Recharts
- **Backend**: FastAPI, Python, SQLAlchemy
- **Machine Learning**: PyTorch, Pandas, NumPy
- **Database**: MySQL (with SQLite fallback for rapid local testing)
- **Containerization**: Docker, Docker Compose

## Dataset Source
The system uses the fictional **IBM Telco Customer Churn Sample Dataset**.
It contains ~7,043 real sample records.
*Official Source:* [IBM Telco Customer Churn](https://github.com/IBM/telco-customer-churn-on-icp4d)

*Note on Data Volume:* While the PRD mentions processing 10,000+ records, the original IBM dataset has ~7,043 rows. To meet larger volume tests, a synthetic data generator (`scripts/generate_synthetic_data.py`) is included to append strictly labeled synthetic data.

## Project Architecture
```text
customer-churn-predictor/
├── backend/            # FastAPI application
├── data/               # Raw and synthetic data files
├── docker/             # Dockerfiles
├── frontend/           # React dashboard UI
├── ml/                 # PyTorch model definition and ML utilities
├── models/             # Trained model state and preprocessor weights
└── scripts/            # Setup, training, and database seeding scripts
```

## Setup & Installation

### Option 1: Docker Compose (Recommended)
1. Ensure Docker and Docker Compose are installed.
2. Build and start the containers:
```bash
docker-compose up --build
```
3. Access the application:
   - Frontend: `http://localhost:3000`
   - Backend API Docs: `http://localhost:8000/docs`

### Option 2: Local Development (Without Docker)

#### 1. Setup Database
- Ensure MySQL is running on port 3306.
- Copy `.env.example` to `.env` and configure your credentials:
```bash
cp .env.example .env
```
*(For local testing without MySQL, `.env` can be configured to use SQLite: `DATABASE_URL=sqlite:///./customer_churn_db.sqlite`)*

#### 2. Install Backend & ML Dependencies
```bash
python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Data Download & Preparation
```bash
python scripts/download_data.py
python scripts/generate_synthetic_data.py --rows 3000
```

#### 4. Train Model
```bash
python scripts/train_model.py
```

#### 5. Seed Database
```bash
python scripts/seed_database.py
```

#### 6. Start Backend Server
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 7. Start Frontend Server (In a new terminal)
```bash
cd frontend
npm install
npm run dev
```

## Testing
Run tests using Pytest (if implemented):
```bash
pytest backend/tests/
```

## Important Notes & Limitations
1. **Fictitious Data**: The IBM dataset is fictional telecommunications data.
2. **Not Causal**: Churn prediction highlights associative risk factors, not causal relationships.
3. **Model Performance**: Current targets aim for ~80-88% accuracy depending on the train-test split and data volume.
4. **Synthetic Data**: Any generated synthetic rows are strictly for demonstration and marked with `data_source=synthetic`.
5. **Production Warning**: A real production deployment would require continuous monitoring, concept-drift detection, and secure credential management.
