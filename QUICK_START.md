# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Edit .env with your settings

# Run the server
python main.py
```

Backend will run on `http://localhost:8000`

### Step 2: Frontend Setup

```bash
# Navigate to frontend (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:3000`

### Step 3: Access the Application

1. Open browser: `http://localhost:3000`
2. Login with your SuccessFactors credentials:
   - Company ID
   - Username
   - Password
   - Application

### Step 4: Upload Your First Workbook

1. Go to "Workbooks" page
2. Drag & drop an Excel (.xlsx) or CSV file
3. Wait for upload to complete
4. Click on the workbook to view details

### Step 5: Analyze & Implement

1. Click "Analyze Workbook" to get AI recommendations
2. Review the analysis and recommendations
3. Select a version
4. Click "Implement Configuration" to apply changes

## 📋 Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] SuccessFactors account with API access
- [ ] (Optional) OpenAI API key for AI features

## 🔧 Configuration

### Backend Configuration (.env)

```env
# Database
DATABASE_URL=sqlite:///./sfbot.db

# Security
SECRET_KEY=your-secret-key-here

# SuccessFactors
SF_BASE_URL=https://api.successfactors.com
SF_API_VERSION=v2

# AI (Optional)
OPENAI_API_KEY=your-openai-key
```

### SuccessFactors API Setup

1. Log in to SuccessFactors Admin Center
2. Navigate to "Manage OAuth2 Client Applications"
3. Create a new OAuth2 client
4. Note down Client ID and Client Secret
5. Configure API permissions

## 🐛 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in main.py or use:
uvicorn main:app --port 8001
```

**Database errors:**
```bash
# Delete existing database
rm sfbot.db
# Restart server (will create new DB)
```

### Frontend Issues

**Port already in use:**
```bash
# Change port in vite.config.js
```

**Module not found:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules
npm install
```

### SuccessFactors Connection Issues

- Verify Company ID format
- Check username includes domain if required
- Ensure API access is enabled in SF
- Verify OAuth2 client is properly configured

## 📚 Next Steps

1. Read [FEASIBILITY_ASSESSMENT.md](./FEASIBILITY_ASSESSMENT.md) for detailed analysis
2. Review [README.md](./README.md) for full documentation
3. Check API documentation at `http://localhost:8000/docs` (Swagger UI)

## 💡 Tips

- Start with a test workbook in a sandbox environment
- Review AI analysis before implementing
- Use version control to track changes
- Test with small configurations first

## 🆘 Need Help?

- Check the [FEASIBILITY_ASSESSMENT.md](./FEASIBILITY_ASSESSMENT.md)
- Review backend logs for errors
- Check browser console for frontend issues
- Verify SuccessFactors API connectivity
