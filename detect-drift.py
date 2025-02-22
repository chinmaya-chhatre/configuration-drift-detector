import yaml  # For parsing YAML files
import json  # For JSON output
import argparse  # For handling CLI arguments
import sys  # For command-line arguments
import datetime  # For timestamps in logs
import smtplib  # For sending email notifications
import os  # For accessing environment variables
import shutil  # For backing up and restoring files
from email.mime.text import MIMEText  # For formatting email messages
from email.mime.multipart import MIMEMultipart  # For handling email body

def read_config(file_path):
    """Reads a YAML configuration file and returns its contents as a dictionary."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def detect_drift(baseline_file, current_file):
    """Compares two configuration files and detects differences (drift)."""
    baseline_config = read_config(baseline_file)
    current_config = read_config(current_file)

    drift = {}

    for key in baseline_config:
        if key in current_config:
            if baseline_config[key] != current_config[key]:  # Detect modified keys
                drift[key] = {
                    "expected": baseline_config[key],
                    "found": current_config[key]
                }
        else:
            drift[key] = {
                "expected": "NOT PRESENT in the baseline",
                "found": "MISSING"
            }

    for key in current_config:
        if key not in baseline_config:
            drift[key] = {
                "expected": "NOT PRESENT in baseline",
                "found": current_config[key]
            }

    return drift

def log_drift(drift_result, baseline_file, current_file, action_taken, output_format=None):
    """Logs the detected drift and restoration actions to a file (drift.log) with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("drift.log", "a") as log_file:
        log_file.write(f"\n[{timestamp}] Configuration Drift Detected!\n")
        log_file.write(f"Baseline: {baseline_file} | Current: {current_file}\n")

        if output_format == "json":
            log_file.write(json.dumps(drift_result, indent=4) + "\n")
        elif output_format == "yaml":
            log_file.write(yaml.dump(drift_result, default_flow_style=False) + "\n")
        else:
            for key, changes in drift_result.items():
                log_file.write(f"- {key}:\n")
                log_file.write(f"   Expected: {changes['expected']}\n")
                log_file.write(f"   Found:    {changes['found']}\n")
        
        log_file.write(f"Action Taken: {action_taken}\n")
        log_file.write("=" * 50 + "\n")

def send_email(drift_result, action_taken):
    """Sends an email notification if configuration drift is detected."""
    
    sender_email = os.getenv("EMAIL_SENDER")
    receiver_email = os.getenv("EMAIL_RECEIVER")
    email_password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    if not sender_email or not receiver_email or not email_password:
        print("❌ Email credentials not set. Skipping email notification.")
        return
    
    subject = "⚠️ Configuration Drift Detected & Auto-Reverted"
    body = "Configuration drift has been detected and auto-reverted:\n\n"
    
    for key, changes in drift_result.items():
        body += f"- {key}:\n"
        body += f"   🔹 Expected: {changes['expected']}\n"
        body += f"   🔸 Found: {changes['found']}\n\n"
    
    body += f"\n✅ Action Taken: {action_taken}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print(f"📩 Email sent to {receiver_email} about drift detection and auto-revert.")
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")

def auto_revert_config(baseline_file, current_file):
    """Automatically restores the baseline configuration by replacing the drifted file."""
    
    backup_file = f"{current_file}.backup"

    try:
        # Create a backup of the current (drifted) configuration
        shutil.copy(current_file, backup_file)
        print(f"🛠️ Backup created: {backup_file}")

        # Restore the baseline configuration
        shutil.copy(baseline_file, current_file)
        print(f"✅ Configuration auto-reverted: {current_file} restored from {baseline_file}")

        return f"Auto-reverted {current_file} from {baseline_file} (Backup saved as {backup_file})"

    except Exception as e:
        print(f"❌ Failed to auto-revert: {str(e)}")
        return "Failed to auto-revert configuration."

if __name__ == "__main__":
    # Parse command-line arguments with argparse
    parser = argparse.ArgumentParser(description="Detect and auto-revert configuration drift.")
    parser.add_argument("baseline_file", help="Path to the baseline configuration file.")
    parser.add_argument("current_file", help="Path to the current configuration file.")
    parser.add_argument("--output", choices=["json", "yaml"], help="Output format (json/yaml).")
    args = parser.parse_args()

    baseline_file = args.baseline_file
    current_file = args.current_file
    output_format = args.output

    drift_result = detect_drift(baseline_file, current_file)

    if drift_result:
        if output_format == "json":
            print(json.dumps(drift_result, indent=4))  # Print drift details in JSON format
        elif output_format == "yaml":
            print(yaml.dump(drift_result, default_flow_style=False))  # Print in YAML format
        else:
            print("\n⚠️  Configuration Drift Detected:\n")
            for key, changes in drift_result.items():
                print(f"- {key}:")
                print(f"   🔹 Expected: {changes['expected']}")
                print(f"   🔸 Found:    {changes['found']}\n")
        
        # Auto-revert the configuration
        action_taken = auto_revert_config(baseline_file, current_file)

        # Log drift details and actions
        log_drift(drift_result, baseline_file, current_file, action_taken, output_format)

        # Send email notification
        send_email(drift_result, action_taken)

        print("📝 Drift details logged to 'drift.log'.")
    else:
        print("✅ No configuration drift detected.")
