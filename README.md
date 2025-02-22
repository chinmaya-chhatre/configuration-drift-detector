# Configuration Drift Detector

This **Python-based Configuration Drift Detector** helps **monitor and auto-revert unintended changes** to critical configuration files.

---

## 🛠️ Features
✅ **Detects configuration drift** between a baseline and current config.  
✅ **Auto-reverts changes** when drift is found.  
✅ **Sends email notifications** to alert users.  
✅ **Logs drift details** in `drift.log`.  
✅ **Supports JSON/YAML output** for better integration.  
✅ **Backup System** – Keeps a copy of the modified config before reverting.  

---

## 📦 Installation

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/chinmaya-chhatre/configuration-drift-detector.git
cd configuration-drift-detector
```

### **2️⃣ Install Dependencies**
```bash
pip install pyyaml
```

### **3️⃣ Ensure Python Version**
```bash
python3 --version
```
> ✅ **Requires Python 3.6+**

---

## 🚀 How to Use

### **1️⃣ Set Up Email Notifications**
Before running, set your email credentials as environment variables:
```bash
export EMAIL_SENDER="your-email@gmail.com"
export EMAIL_RECEIVER="receiver-email@example.com"
export EMAIL_PASSWORD="your-app-password"
export SMTP_SERVER="smtp.gmail.com" [test]
export SMTP_PORT=587
```
> **For Gmail users:** Generate an **App Password** from [Google App Passwords](https://myaccount.google.com/apppasswords).

---

### **2️⃣ Run Drift Detection**
#### **Basic Usage (Human-Readable Output)**
```bash
python3 detect-drift.py config_baseline.yaml config_current.yaml
```

#### **Get JSON Output**
```bash
python3 detect-drift.py config_baseline.yaml config_current.yaml --output json
```

#### **Get YAML Output**
```bash
python3 detect-drift.py config_baseline.yaml config_current.yaml --output yaml
```

---

## 🛠️ How It Works
1. **Compares two YAML config files** (`baseline` vs `current`).
2. If drift is detected:
   - Logs drift details in `drift.log`.
   - Sends an email alert.
   - **Auto-reverts changes** by restoring the baseline file.
   - **Creates a backup** of the modified file before replacing it.

---

## 📜 Example Output

### **Console Output**
```bash
⚠️  Configuration Drift Detected:

- server:
   🔹 Expected: {'host': '127.0.0.1', 'port': 8080}
   🔸 Found:    {'host': '127.0.0.1', 'port': 9090}

🛠️ Backup created: config_current.yaml.backup
✅ Configuration auto-reverted: config_current.yaml restored from config_baseline.yaml
📩 Email sent to aws.notifications.receiver@gmail.com about drift detection and auto-revert.
📝 Drift details logged to 'drift.log'.
```

---

### **Log File (`drift.log`)**
```
[2025-02-21 14:35:12] Configuration Drift Detected!
Baseline: config_baseline.yaml | Current: config_current.yaml
- server:
   Expected: {'host': '127.0.0.1', 'port': 8080}
   Found:    {'host': '127.0.0.1', 'port': 9090}
Action Taken: Auto-reverted config_current.yaml from config_baseline.yaml (Backup saved as config_current.yaml.backup)
==================================================
```

---
## 🚀 Why This Project?
AWS Config already offers drift detection, but it has **limitations**:
- **AWS-Only:** Works only within AWS, while this tool is **cloud-agnostic**.
- **Limited Auto-Revert:** AWS Config detects drift but doesn’t always auto-fix it.
- **Customization:** This tool allows **email alerts, JSON/YAML output, and automatic rollback**.
- **Lightweight & Fast:** No extra AWS costs, no need for managed services.

---

## 🤝 Contributing
Want to improve this tool? Fork the repo, make changes, and submit a pull request!

---

## 📜 License
This project is licensed under the **MIT License**
