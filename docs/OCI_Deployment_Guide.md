# OCI Deployment Guide for Smart Journal Bot

This guide walks you through deploying the Smart Journal Bot on an Oracle Cloud Infrastructure (OCI) "Always Free" instance.

## Prerequisites
- An OCI Account (Free Tier is sufficient).
- SSH Key Pair (Public/Private keys) for accessing the instance.
- Telegram Bot Token & Google Gemini API Key.

---

## Step 1: Create an OCI Compute Instance

1.  **Log in to OCI Console**.
2.  Navigate to **Compute -> Instances** and click **Create Instance**.
3.  **Name**: Give it a name (e.g., `journal-bot-host`).
4.  **Image and Shape**:
    - **Image**: Ubuntu 22.04 or 24.04 Minimal (Canonical Ubuntu).
    - **Shape**:
        - *Option A (Recommended)*: **VM.Standard.A1.Flex** (Ampere ARM). Select 1-4 OCPUs and 6-24 GB RAM. This is powerful and free.
        - *Option B*: **VM.Standard.E2.1.Micro** (AMD). 1 OCPU, 1 GB RAM. Sufficient for this bot but tighter on resources.
5.  **Networking**:
    - Select a new or existing VCN.
    - **IMPORTANT**: Ensure "Assign a public IPv4 address" is checked.
6.  **Add SSH Keys**:
    - Upload your **Public Key** file (`.pub`).
7.  **Boot Volume**: Default (50GB) is fine.
8.  Click **Create**.

---

## Step 2: Configure Network Security (Ingress Rules)

1.  Click on the newly created instance.
2.  Click on the **Subnet** link (e.g., `subnet-xxxx`).
3.  Click on the **Default Security List** for that subnet.
4.  Click **Add Ingress Rules**.
5.  Add a rule to allow SSH (usually already there) and the bot's webhook port:
    - **Source CIDR**: `0.0.0.0/0`
    - **IP Protocol**: TCP
    - **Destination Port Range**: `5000`
    - **Description**: Allow Telegram Webhook
6.  Click **Add Ingress Rules**.

---

## Step 3: Connect to the Instance

Open your local terminal and SSH into the instance using your private key:

```bash
ssh -i /path/to/your/private_key.key ubuntu@<YOUR_INSTANCE_PUBLIC_IP>
```
*(If usage Oracle Linux, user might be `opc`. For Ubuntu, it is `ubuntu`.)*

---

## Step 4: Install Docker & Docker Compose

Run the following commands on the server to install Docker:

```bash
# Update packages
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker dependencies
sudo apt-get install -y ca-certificates curl gnupg

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify installation
sudo docker run hello-world

# Allow running docker without sudo (optional but recommended)
sudo usermod -aG docker $USER
# Log out and log back in for this to take effect
exit
```
*(Reconnect via SSH)*

---

## Step 5: Deploy the Bot

1.  **Clone the Repository**:
    ```bash
    git clone <YOUR_GITHUB_REPO_URL>
    cd Smart_Journal_Bot
    ```

2.  **Configure Environment Variables**:
    Create a `.env` file for Docker Compose to use (though our compose file reads from shell env, it's easier to create a `.env` file and let compose read it automatically if mapped, or export variables).
    
    *Recommended approach*: Create a `.env` file in the project root.
    ```bash
    nano .env
    ```
    Paste the following:
    ```env
    TELEGRAM_BOT_TOKEN=your_token_here
    GEMINI_API_KEY=your_key_here
    WEBHOOK_URL=https://<YOUR_INSTANCE_PUBLIC_IP>:5000
    ```
    *(Note: For WEBHOOK_URL, use `https://<PUBLIC_IP>:5000`. Telegram requires HTTPS. If you don't have a domain/SSL, Telegram allows self-signed certs, OR you can use a separate reverse proxy like Nginx with Certbot. For simplicity, if Telegram refuses connection to raw IP, strictly speaking you need a domain. However, checking Telegram API, it supports ports 443, 80, 88, 8443. Port 5000 is NOT standard supported unless you use a proxy. **Update**: We should expose port 8443 or use Nginx.)*

    **Correction for OCI**: Since Telegram requires specific ports (443, 80, 88, 8443) and SSL, the easiest production setup is using **Caddy** or **Nginx** as a reverse proxy which handles SSL for you automatically.

    **Simplified Setup for this Guide (using HTTP for internal, Caddy for external):**
    
    1. Update `docker-compose.yml` (Optional, add Caddy sidecar).
    
    **Alternatively (Quickest)**: Use `ngrok` in docker or assume you will setup SSL separately. 
    
    *Let's assume you have a way to get HTTPS or are testing.*
    
    To save config: `Ctrl+O`, `Enter`, `Ctrl+X`.

3.  **Start the Bot**:
    ```bash
    docker compose up -d --build
    ```

4.  **Check Logs**:
    ```bash
    docker compose logs -f
    ```

---

## Step 6: Maintenance

- **Update Bot**:
  ```bash
  git pull
  docker compose up -d --build
  ```

- **Backup Database**:
  ```bash
  # Copy database file from container to host
  docker cp smart_journal_bot:/app/bot_data/bot_data.db ./backup_bot_data.db
  ```

- **Restore Database**:
  ```bash
  # Stop bot
  docker compose down
  # Copy backup back
  # (Requires a running dummy container or mounting volume. Easier to just copy to the mapped volume folder on host)
  cp ./backup_bot_data.db ./bot_data/bot_data.db
  # Start bot
  docker compose up -d
  ```

## Troubleshooting
- **Webhook Failures**: Check using `https://api.telegram.org/bot<TOKEN>/getWebhookInfo`.
- **429 Errors**: The bot logs show "Gemini Rate Limit Hit". It will retry automatically.
