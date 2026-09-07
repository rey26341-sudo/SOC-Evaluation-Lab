# Environment Access Validation

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Shell](https://img.shields.io/badge/Shell-Bash-green?logo=gnubash&logoColor=white)
![AWS CloudShell](https://img.shields.io/badge/AWS-CloudShell-orange?logo=amazonaws&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI/CD-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)
![Status](https://img.shields.io/badge/Checks-4%20Passing-brightgreen)

A DevOps practice project that simulates and automates the **pre-deployment environment validation** process using a real Linux environment on AWS CloudShell.

<img width="1440" height="1440" alt="image" src="https://github.com/user-attachments/assets/caaa977d-31fc-4869-bb8d-8ba141622e39" />

> Built and executed entirely in **AWS CloudShell (ap-south-1, Mumbai)** — a real cloud-hosted Linux terminal on Amazon's infrastructure.

---

## What Problem Does This Solve?

In real DevOps work, before deploying any application, an engineer must verify:

| Question | Type of Check |
|---|---|
| Can I access the server? | SSH / Shell check |
| Is the code repository ready? | Repo structure check |
| Is the pipeline running? | CI/CD pipeline check |
| Can I monitor the application? | Log access check |

Doing this manually every time is slow and error-prone. This project **automates all 4 checks** and generates a timestamped report.

---

## Architecture

```
Developer (Rey)
      │
      │ types commands in browser
      ▼
┌─────────────────────────────────────────────┐
│         AWS CloudShell (ap-south-1)         │
│   Real Linux environment on AWS servers     │
│                                             │
│  ┌──────────────┐   ┌──────────────────┐   │
│  │   Check 1    │   │    Check 2       │   │
│  │ SSH / Shell  │   │ Repo structure   │   │
│  │ whoami       │   │ app.py           │   │
│  │ uname -n     │   │ config.yml       │   │
│  │ uptime       │   │                  │   │
│  └──────────────┘   └──────────────────┘   │
│  ┌──────────────┐   ┌──────────────────┐   │
│  │   Check 3    │   │    Check 4       │   │
│  │ Pipeline     │   │ Log directory    │   │
│  │ build_status │   │ logs/app.log     │   │
│  │ .txt         │   │                  │   │
│  └──────────────┘   └──────────────────┘   │
│              │                             │
│              ▼                             │
│   access_checklist_report.txt              │
│   (auto-generated report)                  │
└─────────────────────────────────────────────┘
      │
      │ git add → git commit → git push
      │ (SSH key auth via ed25519)
      ▼
┌─────────────────────────────────────────────┐
│              GitHub Repository              │
│         rey26341-sudo/ENVIRONMENT-          │
│           ACCESS-VALIDATION                 │
│                                             │
│  Files pushed:                              │
│  ├── validate_environment.py                │
│  ├── access_checklist_report.txt            │
│  ├── logs/app.log                           │
│  ├── pipeline_simulation/build_status.txt   │
│  ├── repo_simulation/app.py                 │
│  ├── repo_simulation/config.yml             │
│  └── .github/workflows/validate.yml        │
│              │                              │
│              ▼                              │
│       GitHub Actions CI/CD                  │
│   Runs automatically on every push          │
│   Lint → Validate → Archive report          │
└─────────────────────────────────────────────┘
```

---

## Project Structure

```
ENVIRONMENT-ACCESS-VALIDATION/
│
├── validate_environment.py           ← Main Python validation script
├── access_checklist_report.txt       ← Auto-generated report
│
├── repo_simulation/
│   ├── app.py                        ← Simulated application
│   └── config.yml                    ← App configuration
│
├── pipeline_simulation/
│   └── build_status.txt              ← Simulated pipeline status
│
├── logs/
│   └── app.log                       ← Application log file
│
├── .github/workflows/
│   └── validate.yml                  ← GitHub Actions CI pipeline
│
└── pipeline_flow_documentation_v1.md ← Full pipeline documentation
```

---

## The 4 Checks

| # | Check | Commands Used | Result |
|---|---|---|---|
| 1 | SSH / Shell Access | `whoami` `uname -n` `uptime` | ✅ SUCCESS |
| 2 | Repository Structure | `ls -R` `ls -l` | ✅ SUCCESS |
| 3 | Pipeline Status | `cat build_status.txt` | ✅ SUCCESS |
| 4 | Log Directory Access | `cat app.log` | ✅ SUCCESS |

---

## How To Run

```bash
# Clone the repo
git clone https://github.com/rey26341-sudo/ENVIRONMENT-ACCESS-VALIDATION.git
cd ENVIRONMENT-ACCESS-VALIDATION

# Run the validation script
python validate_environment.py
```

### Output

```
==================================================
  ENVIRONMENT ACCESS VALIDATION
  2026-03-03 09:50:39
==================================================

CHECK 1: SSH / Shell Environment
  whoami   → cloudshell-user
  hostname → (not found — used uname -n)
  uname -n → ip-10-131-17-245.ap-south-1.compute.internal
  uptime   → 09:50:39 up 25 min, 0 users, load average: 0.02
  [✔] SSH / Shell Access: SUCCESS

CHECK 2: Repository Structure
  ✔ Found: repo_simulation/app.py
  ✔ Found: repo_simulation/config.yml
  [✔] Repository Structure: SUCCESS

CHECK 3: Pipeline Simulation
  ✔ pipeline: SUCCESS
  ✔ build #101 completed
  [✔] Pipeline Simulation: SUCCESS

CHECK 4: Log Directory Access
  ✔ application started successfully
  ✔ no errors detected
  [✔] Log Directory Access: SUCCESS

  Report written → access_checklist_report.txt
==================================================
  OVERALL: ALL CHECKS PASSED ✔
==================================================
```

---

## Real Issues Faced & How I Solved Them

These are actual errors hit while building this in AWS CloudShell:

| Issue | Error Message | Resolution |
|---|---|---|
| `hostname` not available | `bash: hostname: command not found` | Used `uname -n` as fallback |
| Git had no identity set | `fatal: empty ident name not allowed` | Ran `git config --global user.email` and `user.name` |
| SSH key permission too open | `WARNING: UNPROTECTED PRIVATE KEY FILE!` | Used correct private key file path |
| Space in folder name | `bash: cd: too many arguments` | Used underscore: `repo_simulation` |

---

## CI/CD Pipeline

GitHub Actions workflow runs automatically on every push to `main`:

```
Push to main → Setup Python 3.10 → Lint (flake8)
     → Run validate_environment.py
     → Archive access_checklist_report.txt (30 days)
```

---

## What I Actually Did — Step by Step

1. Opened **AWS CloudShell** in browser (ap-south-1, Mumbai region)
2. Created project folder: `mkdir env_acc_val && cd env_acc_val`

   <img width="1920" height="1020" alt="2026-03-03 (5)" src="https://github.com/user-attachments/assets/83a46c1b-459e-4191-8e00-74a06d9741b4" />

4. Created all files using Linux commands (`echo`, `mkdir`, `nano`)
5. Ran real validation checks: `whoami`, `uname -n`, `uptime`, `ls -R`

   <img width="1920" height="1020" alt="2026-03-03 (16)" src="https://github.com/user-attachments/assets/4e36d030-b2e4-47f7-bc7b-2015275e94e7" />

   <img width="1920" height="1020" alt="2026-03-03 (17)" src="https://github.com/user-attachments/assets/0eb07b79-0b7c-475a-9d6a-43bc81c751ed" />
   
6.Wrote the checklist report using `nano`

   <img width="1920" height="1020" alt="2026-03-03 (19)" src="https://github.com/user-attachments/assets/6e0cbfac-5fb0-4402-822b-15f76a61ce4b" />
   
   <img width="1920" height="1020" alt="2026-03-03 (21)" src="https://github.com/user-attachments/assets/174cf6ee-eb95-4054-8ac4-54ec1b58d5c9" />

8. Initialized Git: `git init` → `git add .` → `git commit`

   <img width="1920" height="1020" alt="2026-03-03 (25)" src="https://github.com/user-attachments/assets/d67b070e-fbfe-42ab-892a-cd57a6431daa" />

   <img width="1920" height="1020" alt="2026-03-03 (26)" src="https://github.com/user-attachments/assets/7c31d73a-6f8c-447b-8faa-68627879a292" />

   <img width="1920" height="1020" alt="2026-03-03 (29)" src="https://github.com/user-attachments/assets/66a1545e-d813-47d8-bb30-532f361ad9ac" />

10. Fixed Git identity error with `git config --global`
11. Generated SSH key pair: `ssh-keygen -t ed25519`

<img width="1920" height="1020" alt="2026-03-03 (28)" src="https://github.com/user-attachments/assets/bade8a7b-9007-408f-acda-7fefeeacdd84" />

11. Connected repo to GitHub: `git remote set-url origin`
12. Pushed all files to GitHub

---

## What I Learned

- How a real Linux cloud environment (AWS CloudShell) works
- Linux commands: `mkdir`, `echo`, `cat`, `ls`, `nano`, `cd`, `pwd`, `whoami`, `uname`, `uptime`
- Setting up Git from scratch in a new environment
- Configuring SSH key authentication for GitHub
- What pre-deployment checks actually are and why they matter
- Writing a CI/CD pipeline with GitHub Actions
- Documenting real issues and their resolutions

---

## Tools & Technologies

- **AWS CloudShell** — real Linux terminal on AWS (ap-south-1, Mumbai)
- **Python 3** — scripting and automation
- **Bash / Linux** — all file creation done via terminal commands
- **Git** — version control initialized from scratch
- **GitHub Actions** — CI/CD pipeline automation
- **SSH (ed25519)** — secure key authentication to GitHub
- **nano** — terminal text editor

---

## Project Status

This is a **learning and practice project** built to understand DevOps pre-deployment validation concepts.
Executed in a real cloud environment (AWS CloudShell) but does not connect to a live production server.

---

## Author

**Rey** — Aspiring DevOps Engineer
Self-taught | DevOps Course Certified | Hands-on Practice
[GitHub Profile](https://github.com/rey26341-sudo)
