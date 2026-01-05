# OCI MANAGEMENT QUICK REFERENCE (Smart Journal Bot)

================================
OCI BOT MANAGEMENT COMMANDS
================================

This document provides a quick reference for common shell commands used to manage, update, and monitor the Smart Journal Bot on your OCI Docker instance.

------------------------
1. SERVER CONNECTION
------------------------
# Standard Ubuntu User
User: ubuntu
Public IP: 140.245.222.72
Key Path: C:\OCI\ssh-key-2025-11-22.key

# Connect via SSH (from PowerShell)
ssh -i "C:\OCI\ssh-key-2025-11-22.key" ubuntu@140.245.222.72

-----------------------------
2. BOT DEPLOYMENT & UPDATES
-----------------------------
# Navigate to the bot folder
cd ~/Smart_Journal_Bot

# Update the bot with latest code from GitHub
git pull

# Rebuild and restart the container
docker compose up -d --build

------------------------
3. SERVICE MANAGEMENT
------------------------
# Run these commands from: ~/Smart_Journal_Bot

# Check Status:
docker compose ps

# Start Bot:
docker compose up -d

# Stop Bot (Removes containers):
docker compose down

# Restart Bot:
docker compose restart

----------------------
4. LOG MONITORING
----------------------
# View Live Logs (Ctrl+C to exit):
docker compose logs -f

# View Last 100 lines:
docker compose logs --tail=100

-------------------------
5. MONITORING CPU & MEMORY
-------------------------
# Overall server health
htop

# Individual container usage
docker stats

# Disk Space
df -h

-------------------
6. FILE TRANSFER (SCP)
-------------------
# Download Database to Local Machine (run in local PowerShell)
scp -i "C:\OCI\ssh-key-2025-11-22.key" ubuntu@140.245.222.72:~/Smart_Journal_Bot/bot_data/bot_data.db .

-------------------------
7. DATABASE QUERY (LIVE)
-------------------------
# Open the database file on the server
cd ~/Smart_Journal_Bot/bot_data
sqlite3 bot_data.db

# --- Inside sqlite session ---
.mode column
.headers on
SELECT * FROM JournalEntries LIMIT 5;
.quit

------------------------
8. GITHUB INFO
------------------------
# Repo URL: https://github.com/AbhaySingh989/Smart_Journal_Bot
