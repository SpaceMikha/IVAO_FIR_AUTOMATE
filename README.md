#  Aurora Sectorfile Git Automation

##  Overview
This script automates the process of committing and pushing **Aurora sectorfile updates** to GitHub. It allows you to:

 **Commit & push modified files**: Type filenames, search for them, copy them to the repo, add commit messages, and push them.  
 **Add new files**: Create a new file, commit it, and push it to GitHub.  
 **Use an `.env` file**: Easily configure paths for different users.  

---

##  How It Works
When you run the script, you'll see this prompt:

```
 Choose an option:
1️ Commit & push modified files
2️ Add a new file and push it to the repo

Enter 1 or 2:
```

- **Option 1:** The script will ask for the filenames you modified. It will search for them in the `SECTORFILE_PATH`, copy them to `REPO_PATH`, ask for commit messages, and push the changes.  
- **Option 2:** The script will ask for the name of a new file to add. It will create the file, ask for a commit message, and push it to GitHub.

---

##  Installation & Setup
### **1️ Install Python**
Ensure you have **Python 3.7+** installed. Check your version:
```sh
python --version
```

### **2️ Install Required Packages**
Run:
```sh
pip install python-dotenv colorama
```

### **3️ Clone the Repository**
If you haven't already cloned your repo:
```sh
git clone https://github.com/YOUR-ORG/YOUR-REPO.git
```

### **4️ Set Up Your `.env` File**
Inside the project folder, create a `.env` file:
```
SECTORFILE_PATH=M:/Aurora/SectorFiles/Include/SBRE
REPO_PATH=C:/Users/YOUR_USER/Documents/SBRE_Repo
```
Replace **`YOUR_USER`** with your Windows username.

---

##  Usage
### **Run the Script**
From the project directory, run:
```sh
python manual_git_push.py
```

### **Example Usage**
#### **1️ Committing Modified Files**
```
🔹 Enter the filenames you modified (one per line). Type 'done' when finished:
> sbfz.gts
 Copied: M:/Aurora/SectorFiles/Include/SBRE/sbfz.gts → C:/Users/YOUR_USER/Documents/SBRE_Repo/sbfz.gts

Enter commit message for 'sbfz.gts': Fixed taxiway errors
 Changes successfully pushed to GitHub!
```

#### **2️ Adding a New File**
```
 Enter the name of the new file you want to add: new_chart.txt
 Created new file: C:/Users/YOUR_USER/Documents/SBRE_Repo/new_chart.txt

 Enter commit message for 'new_chart.txt': Added new airport chart
 New file successfully pushed to GitHub!
```

---

##  Automating the Script (Optional)
To run the script **automatically**, use **Windows Task Scheduler**:

Open **Task Scheduler (`taskschd.msc`)**  
Click **"Create Basic Task"**  
Set a trigger (**on startup** or **every hour**)  
Set action **"Start a Program"**, and enter:
   ```
   python C:\path\to\main.py
   ```

---

##  Troubleshooting
### **1. ImportError: No module named 'dotenv'**
Run:
```sh
pip install python-dotenv
```

### **2. GitHub Authentication Issues**
Ensure you have:
- Set up **SSH keys** ([GitHub Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh))
- Or use **GitHub Personal Access Token (PAT)** instead of passwords.

### **3. Script Doesn't Detect My Files**
- Ensure the **`SECTORFILE_PATH`** in `.env` is correct.
- Try running:  
  ```sh
  python -c "import os; print(os.listdir('M:/Aurora/SectorFiles/Include/SBRE'))"
  ```
  If files are not listed, the path may be incorrect.

---

##  Contributing
If you have suggestions or improvements, feel free to open a **Pull Request**!
---

*This script was developed by:* **Mikhael da Silva**

