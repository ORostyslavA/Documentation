# Lab 2 OSMAK

This is a three-tier application with Data Access Layer (DAL), Business Logic Layer (BLL), and Presentation Layer.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Generate data: `python generator/generate_data.py`
3. Run the application: `python main.py`

## Architecture

- **DAL**: Uses SQLAlchemy ORM for database operations and CSV import.
- **BLL**: Business logic for importing data and managing models.
- **Presentation**: Interfaces for controllers (not implemented yet).
- **Generator**: Script to generate sample CSV data with 1000+ rows.
