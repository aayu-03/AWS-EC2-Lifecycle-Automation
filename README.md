# AWS EC2 Lifecycle Automation 🚀

## Overview
This project automates the **provisioning, monitoring, and cleanup** of AWS EC2 instances using **Terraform, Python (Boto3), and Jenkins**.  
It demonstrates **infrastructure as code (IaC)**, **cloud cost optimization**, and **CI/CD governance**.

---

## Features
- ✅ Provision EC2 instances with Terraform
- ✅ Monitor EC2 status with Python + Boto3
- ✅ Automatically stop idle instances (<5% CPU utilization)
- ✅ Cleanup unused volumes, snapshots, and Elastic IPs
- ✅ Jenkins pipeline for CI/CD with approvals and rollback

---

## Tech Stack
- **Terraform** – Infrastructure provisioning
- **Python (Boto3)** – AWS automation scripts
- **Jenkins** – CI/CD pipeline orchestration
- **AWS CloudWatch** – Monitoring & metrics

---

## Project Structure

```text
aws-ec2-lifecycle-automation/
├── terraform/        # Terraform IaC
├── scripts/          # Python automation scripts
├── Jenkinsfile       # CI/CD pipeline
├── requirements.txt  # Python dependencies
└── README.md         # Documentation
```
---

## How to Run

### 1. Clone the repo
```bash
git clone https://github.com/your-username/aws-ec2-lifecycle-automation.git
cd aws-ec2-lifecycle-automation
```
### 2. Provision EC2 with Terraform

cd terraform
terraform init
terraform apply

### 3. Install dependencies
pip3 install -r requirements.txt

### 4. Run monitoring
python3 scripts/ec2_status.py

### 5. Run cleanup
python3 scripts/cleanup.py


## CI/CD with Jenkins
- **Pipeline stages**: Checkout → Terraform Plan → Approval → Apply → Python Scripts → Cleanup
- **Credentials** stored securely in Jenkins
- **Approval** step ensures governance
- **Logs and notifications** for audit
