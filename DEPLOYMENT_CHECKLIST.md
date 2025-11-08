# 📋 DEPLOYMENT CHECKLIST & COMMANDS

## ✅ PRE-DEPLOYMENT CHECKLIST

- [ ] Model trained (face_emotionModel.h5 exists)
- [ ] App tested locally (python app.py works)
- [ ] All files in FACE_DETECTION folder
- [ ] requirements.txt has all packages
- [ ] GitHub account created
- [ ] Render account created
- [ ] Git installed on computer

---

## 🔧 EXACT COMMANDS TO RUN (Copy & Paste)

### Step 1: Navigate to Project
```powershell
cd "C:\Users\DELL 7300\Documents\400LEVEL ALPHA\CSC 415 -AI\ai-assignment"
```

### Step 2: Initialize Git (One Time)
```powershell
git init
git add .
git commit -m "Initial facial emotion detection project"
```

### Step 3: Create GitHub Repo (Do Online)
1. Go to https://github.com/new
2. Repository name: `facial-emotion-detection`
3. Click "Create repository"
4. GitHub shows you commands to run...

### Step 4: Push to GitHub (Use GitHub's Commands)
```powershell
git remote add origin https://github.com/YOUR_USERNAME/facial-emotion-detection.git
git branch -M main
git push -u origin main
```

**Replace YOUR_USERNAME with your GitHub username!**

### Step 5: Deploy on Render (Do Online)
1. Go to https://render.com
2. Sign up with GitHub
3. Dashboard → "+ New" → "Web Service"
4. Connect GitHub repo
5. Fill settings:
   - Name: facial-emotion-detection
   - Root: FACE_DETECTION
   - Build: pip install -r requirements.txt
   - Start: python app.py
6. Add Environment Variable:
   - PORT = 10000
7. Click "Create Web Service"
8. Wait 5 minutes...

### Step 6: Save Your Live URL
```powershell
# Your URL will look like:
# https://facial-emotion-detection.onrender.com

# Edit this file with your URL:
cd FACE_DETECTION
notepad link_web_app.txt
```

### Step 7: Push URL to GitHub
```powershell
git add link_web_app.txt
git commit -m "Add deployment URL"
git push
```

---

## 📊 COMMAND QUICK REFERENCE

| Action | Command |
|--------|---------|
| Check git status | `git status` |
| Add all files | `git add .` |
| Commit | `git commit -m "message"` |
| Push to GitHub | `git push` |
| Check remote | `git remote -v` |
| View logs | `git log` |

---

## 🔍 VERIFY AT EACH STAGE

### After Git Init & Commit
```
Expected: Files staged and committed
Check: git log (should show your commit)
```

### After Push to GitHub
```
Expected: Files on github.com
Check: Go to github.com/username/repo and see all files
```

### After Render Deploy
```
Expected: Live URL accessible
Check: Click the URL and see the web form
```

### After Testing
```
Expected: Upload image, see emotion prediction
Check: Form loads, image uploads, results appear
```

---

## ⚠️ COMMON MISTAKES TO AVOID

❌ **DON'T:**
- Forget YOUR_USERNAME in git remote command
- Push code without committing first
- Leave Root Directory as default (must be FACE_DETECTION)
- Forget to add PORT environment variable
- Miss the face_emotionModel.h5 file in commit

✅ **DO:**
- Replace YOUR_USERNAME with your actual GitHub username
- Add all files before push: `git add .`
- Set Root Directory to: FACE_DETECTION
- Add environment variable: PORT = 10000
- Verify model file is in folder before git add

---

## 🚨 IF SOMETHING GOES WRONG

### "fatal: destination path already exists"
```
Solution: Delete .git folder and start over
Command: rm -r .git (or delete .git folder manually)
Then: Run git init again
```

### "fatal: could not read Username"
```
Solution: GitHub authentication issue
Fix: Use HTTPS with token or SSH key
Or: Try again with correct repository URL
```

### "Build failed" on Render
```
Check logs on Render dashboard
Common cause: Model file not included
Solution: Make sure face_emotionModel.h5 was pushed to GitHub
```

### "ModuleNotFoundError" on Render
```
Check: Is dependency in requirements.txt?
Fix: Add missing package to requirements.txt, push, redeploy
```

### "Model not found" on live app
```
Issue: face_emotionModel.h5 not in GitHub
Solution: 
git add face_emotionModel.h5
git commit -m "Add model"
git push
Then redeploy on Render
```

---

## 📱 TESTING YOUR LIVE APP

1. Go to: `https://your-app-name.onrender.com`
2. Enter your name
3. Upload a photo of your face
4. Click "Detect Emotion"
5. You should see:
   - ✅ Emotion detected
   - ✅ Confidence percentage
   - ✅ Feedback message
   - ✅ Appears in submissions list

---

## 🎯 SUCCESS INDICATORS

✅ GitHub repo shows all your files  
✅ Render service shows "deployed"  
✅ Live URL is accessible  
✅ Emotion detection works  
✅ Submissions are saved  
✅ No error messages  

---

## 📝 FINAL STEPS

- [ ] All code pushed to GitHub
- [ ] Render deployment complete
- [ ] Live app tested successfully
- [ ] Live URL saved to link_web_app.txt
- [ ] Updated link pushed to GitHub
- [ ] Ready for grading

---

## 🎉 YOUR LIVE DEPLOYMENT

Once complete, your app lives at:
```
https://facial-emotion-detection.onrender.com
```

**This is your submission link for grading!**

---

## 📞 RENDER DOCUMENTATION

If you need more help:
- Render Docs: https://render.com/docs
- Python Deployment: https://render.com/docs/deploy-python
- Troubleshooting: https://render.com/docs/troubleshooting

---

## ⏱️ TIMELINE

- Git setup: 2 min
- Push to GitHub: 1-2 min
- Render setup: 2 min
- Deployment (automated): 5 min
- Testing: 2 min
- **TOTAL: ~15 minutes**

---

## ✨ YOU DID IT!

Your facial emotion detection app is now:
- 🌍 On the internet
- 🔒 Backed up on GitHub
- 📊 Running in the cloud
- 🚀 Ready for grading

Congratulations! 🎉
