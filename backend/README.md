# SuccessFactors Configuration Bot - Backend

## Overview
AI-powered backend service for automating SuccessFactors configuration management using workbook-based approach.

## Features
- SuccessFactors OAuth 2.0 authentication
- Workbook upload and version control
- AI-powered configuration analysis
- Automated implementation of configurations
- Version history and rollback capabilities

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run the server:
```bash
python main.py
# or
uvicorn main:app --reload
```

## API Endpoints

- `POST /api/auth/login` - Authenticate with SuccessFactors
- `GET /api/workbooks` - List all workbooks
- `POST /api/workbooks/upload` - Upload a workbook
- `POST /api/workbooks/{id}/implement` - Implement workbook configuration
- `GET /api/workbooks/{id}/versions` - Get workbook versions
- `POST /api/workbooks/{id}/analyze` - AI analysis of workbook

## SuccessFactors Integration

The service integrates with SuccessFactors APIs using:
- OAuth 2.0 for authentication
- REST API for configuration management
- Support for various SF modules (User, Position, Job, Compensation, etc.)
