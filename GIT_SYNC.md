# Git Sync Guide

Your local repository is now synced with GitHub: https://github.com/SumitAG008/aiBotc

## Current Status
- ✅ Git repository initialized
- ✅ Remote origin configured
- ✅ All files committed
- ✅ Pushed to GitHub (master branch)

## Future Sync Commands

### To push changes to GitHub:
```bash
cd C:\Users\sumit\Documents\AICBOT
git add .
git commit -m "Your commit message"
git push
```

### To pull changes from GitHub:
```bash
cd C:\Users\sumit\Documents\AICBOT
git pull
```

### To check status:
```bash
cd C:\Users\sumit\Documents\AICBOT
git status
```

### To see what branch you're on:
```bash
cd C:\Users\sumit\Documents\AICBOT
git branch
```

## Branch Information

Currently using `master` branch. If GitHub defaults to `main`, you can rename:
```bash
git branch -m master main
git push -u origin main
```

## Files Included

All project files are tracked:
- Backend (FastAPI)
- Frontend (React)
- Documentation
- Configuration files

## Excluded Files (.gitignore)

The following are NOT synced (for security):
- `.env` files (contains secrets)
- `node_modules/`
- `venv/`
- `*.db` (database files)
- `uploads/` and `repos/` directories

## Important Notes

1. **Never commit sensitive data**:
   - API keys
   - Passwords
   - `.env` files
   - Database files

2. **Always review changes** before committing:
   ```bash
   git status
   git diff
   ```

3. **Use meaningful commit messages**:
   ```bash
   git commit -m "Add feature: AI analysis improvements"
   ```

## Troubleshooting

### If push fails due to authentication:
- Use GitHub Personal Access Token instead of password
- Or set up SSH keys

### If you need to sync with a different branch:
```bash
git checkout -b new-branch-name
git push -u origin new-branch-name
```

### To see commit history:
```bash
git log --oneline
```

---

**Repository URL**: https://github.com/SumitAG008/aiBotc
