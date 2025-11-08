# 🚀 RENDER DEPLOYMENT - COMPLETE GUIDE

## 📋 Prerequisites Check

Before deploying, verify you have:
- ✅ GitHub account (create one if you don't have it)
- ✅ Render account (free at render.com)
- ✅ Git installed on your computer
- ✅ All files in FACE_DETECTION folder
- ✅ Model trained (face_emotionModel.h5 created)

---

## 🎯 STEP-BY-STEP DEPLOYMENT

### PHASE 1: Prepare Your Code (GitHub)

#### Step 1: Initialize Git Repository
```powershell
# Navigate to your project root (parent of FACE_DETECTION)
cd "C:\Users\DELL 7300\Documents\400LEVEL ALPHA\CSC 415 -AI\ai-assignment"

# Initialize git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial facial emotion detection project"
```

**Expected Output:**
```
[master (root-commit) xxxxx] Initial facial emotion detection project
 15 files changed, ...
```

#### Step 2: Create GitHub Repository
1. Go to **github.com**
2. Click **"New repository"** (+ icon, top right)
3. **Repository name**: `facial-emotion-detection` (or any name)
4. **Description**: "Facial emotion recognition ML web app"
5. **Visibility**: Public (required for free Render deployment)
6. Click **"Create repository"**

**You'll see instructions like:**
```
git remote add origin https://github.com/YOUR_USERNAME/facial-emotion-detection.git
git branch -M main
git push -u origin main
```

#### Step 3: Connect & Push to GitHub
```powershell
# Add remote (replace with your URL from Step 2)
git remote add origin https://github.com/YOUR_USERNAME/facial-emotion-detection.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

**Expected Output:**
```
Enumerating objects: 25, done.
Counting objects: 100% (25/25), done.
...
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

**Verify**: Go to github.com/YOUR_USERNAME/facial-emotion-detection and you should see all files!

---

### PHASE 2: Deploy on Render

#### Step 1: Create Render Account
1. Go to **https://render.com**
2. Click **"Sign up"** (top right)
3. Use GitHub to sign up (easiest option)
4. Click **"Authorize render-com"**

#### Step 2: Connect GitHub Repository
1. After login, click **"Dashboard"** (top right)
2. Click **"+ New"** button
3. Select **"Web Service"** (for backend app)

#### Step 3: Configure Deployment Settings
You'll see a form. Fill it like this:

**1. Select Repository**
- Click **"Connect GitHub account"** if not done
- Search for your repository: `facial-emotion-detection`
- Click **"Connect"**

**2. Deployment Settings**
```
Name:                    facial-emotion-detection
Region:                  Singapore (or closest to you)
Branch:                  main
Root Directory:          FACE_DETECTION (IMPORTANT!)
Runtime:                 Python 3
Build Command:           pip install -r requirements.txt
Start Command:           python app.py
```

**3. Environment Variables**
Click **"+ Add Environment Variable"**:
- **Key**: PORT
- **Value**: 10000

Leave everything else as default.

**4. Instance Type**
- Select **"Free"** (if you want free tier)
- Or **"Starter"** ($7/month) for better performance

#### Step 4: Deploy!
1. Click **"Create Web Service"**
2. Render will start deploying (takes 3-5 minutes first time)
3. Watch the logs for progress

**You'll see:**
```
Build started...
npm or python version: Python 3.10.13
Installing dependencies...
...
Build succeeded
Deploying...
```

#### Step 5: Wait for Deployment
The deployment process:
- ⏳ Installs Python dependencies (2-3 min)
- ⏳ Starts your Flask app (1-2 min)
- ✅ App goes live on Render

**You'll see: "Your service is live!"** in green ✅

---

### PHASE 3: Get Your Live URL & Save It

#### Step 1: Find Your Deployment URL
On Render dashboard:
1. Your service should show a URL like:
   ```
   https://facial-emotion-detection.onrender.com
   ```
2. Click the URL to test your app

#### Step 2: Test Your Deployment
1. Open the URL in your browser
2. You should see the emotion detection form
3. Try uploading a photo
4. Test that emotion detection works
5. Verify submissions appear in database

#### Step 3: Save the URL
1. Go back to your local FACE_DETECTION folder
2. Open **link_web_app.txt**
3. Add your deployment URL:
   ```
   https://facial-emotion-detection.onrender.com
   ```
4. Save the file

#### Step 4: Push Updated File to GitHub
```powershell
# Add the updated file
git add link_web_app.txt

# Commit
git commit -m "Add deployment link"

# Push
git push
```

---

## ✅ VERIFICATION CHECKLIST

After deployment, verify everything works:

- [ ] App loads at your Render URL
- [ ] Form displays correctly
- [ ] Can enter name
- [ ] Can upload image
- [ ] Emotion detection works
- [ ] Feedback message appears
- [ ] Submissions list shows submissions
- [ ] Confidence bar displays
- [ ] Mobile view is responsive
- [ ] No error messages in browser console

---

## 🔍 MONITORING & DEBUGGING

### Check Logs
1. Go to your Render service dashboard
2. Click **"Logs"** tab
3. Watch for any errors
4. Look for "Running on..." message

### Common Issues During Deployment

#### Issue: "Build failed"
```
Solution: Check logs - usually missing dependency
- Verify requirements.txt has all packages
- Check for typos in file names
```

#### Issue: "App crashes after deploy"
```
Solution: Check logs for error messages
- May need to retrain model
- Check database permissions
```

#### Issue: "Model not found error"
```
Solution: Model file wasn't pushed to GitHub
- Commit face_emotionModel.h5 to GitHub
- Re-deploy
```

#### Issue: "Port error"
```
Solution: Render uses PORT environment variable
- Verify app.py reads: int(os.environ.get('PORT', 5000))
- Already configured in provided code ✅
```

---

## 📊 Expected Deployment Timeline

| Step | Time | Status |
|------|------|--------|
| GitHub setup | 2-5 min | Quick |
| Git push | 1-2 min | Quick |
| Render setup | 2-3 min | Quick |
| Dependency install | 2-3 min | Automated |
| App startup | 1-2 min | Automated |
| **Total** | **~10-15 min** | First time |

---

## 🎯 AFTER DEPLOYMENT

### What's Running on Render
- Your Flask app (24/7)
- Your database.db file (persists)
- Your model file (face_emotionModel.h5)
- All your code

### Database
- SQLite database persists between restarts
- Submissions from your app stay saved
- You can test with multiple users

### Important Notes
- Free tier: App sleeps after 15 min of inactivity (wakes up on request)
- Logs available: Check for any errors
- Can view/manage from Render dashboard

---

## 🚀 ADVANCED: Making Changes & Redeploying

If you need to update your code:

```powershell
# Make changes to your files
# Then:

git add .
git commit -m "Updated feature: ..."
git push

# Render automatically redeploys! ✅
# Just wait 2-3 minutes
```

---

## 💡 TIPS & BEST PRACTICES

✅ **DO:**
- Keep requirements.txt updated
- Test locally before pushing
- Monitor logs for errors
- Save deployment link immediately
- Commit your model file to GitHub

❌ **DON'T:**
- Hardcode absolute paths
- Use localhost/127.0.0.1 in production
- Forget to commit model file
- Change PORT handling code
- Use debug=True in production

---

## 📞 TROUBLESHOOTING

### "Repository not found"
```
Check: Did you push to GitHub successfully?
Fix: Run: git push -u origin main
```

### "Can't connect to GitHub"
```
Check: Are you logged into GitHub?
Fix: Create new personal access token on GitHub
```

### "Build succeeded but app won't start"
```
Check logs for Python errors
Common causes:
- Missing dependencies (check requirements.txt)
- Model file not found (push to GitHub)
- Database permission issue (check .gitignore)
```

### "Model takes too long to load"
```
Normal: First request loads model (~5 seconds)
Fine: Subsequent requests are faster
```

### "Submissions disappearing"
```
Check: Free tier restarts after 15 min
Note: Data persists, just app restarts
```

---

## 📋 DEPLOYMENT CHECKLIST

- [ ] GitHub account created
- [ ] Render account created
- [ ] Code pushed to GitHub
- [ ] Repository is PUBLIC
- [ ] face_emotionModel.h5 committed to GitHub
- [ ] Render service created
- [ ] Build command set correctly
- [ ] Start command set correctly
- [ ] Environment variable PORT=10000 added
- [ ] Root directory set to FACE_DETECTION
- [ ] Deployment completed successfully
- [ ] App is accessible at Render URL
- [ ] Tested emotion detection on live app
- [ ] URL saved to link_web_app.txt
- [ ] Updated file pushed to GitHub

---

## ✨ FINAL RESULT

After completing all steps:

✅ **Your app is live at**: `https://facial-emotion-detection.onrender.com`  
✅ **Anyone can access it** from anywhere  
✅ **Your model works** in the cloud  
✅ **Your database persists** across restarts  
✅ **Your code is on GitHub** for backup  

---

## 📝 QUICK REFERENCE

### Commands to Run (in order)
```powershell
# 1. Navigate to project root
cd "C:\Users\DELL 7300\Documents\400LEVEL ALPHA\CSC 415 -AI\ai-assignment"

# 2. Initialize git
git init
git add .
git commit -m "Initial commit"

# 3. Add GitHub remote
git remote add origin https://github.com/USERNAME/REPO.git
git branch -M main
git push -u origin main

# 4. After Render deployment, update link
# (edit link_web_app.txt with your URL)
git add link_web_app.txt
git commit -m "Add deployment link"
git push
```

### Key Render Settings
```
Root Directory: FACE_DETECTION
Build: pip install -r requirements.txt
Start: python app.py
Environment: PORT=10000
```

---

## 🎉 YOU'RE READY TO DEPLOY!

Everything in your FACE_DETECTION folder is already configured for Render deployment.

Just follow the steps above and your app will be live! 🚀

**Questions?** Check the logs on Render or review the EXECUTION_GUIDE.md file.

Good luck! 🌟
