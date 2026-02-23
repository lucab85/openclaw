# Azure Deploy Guide (Ubuntu VM + Docker)

> Minimal, repeatable, safe-by-default.  
> Assumes: Ubuntu 22.04 LTS VM, SSH key auth, Docker.

---

## 0) Prerequisites

- Azure subscription
- SSH key pair (recommended) — avoid password auth
- Laptop terminal + SSH client

---

## 1) Create the VM (Azure Portal)

1. **Create a resource → Virtual Machine**
2. Basics:
   - Resource group: `rg-openclaw` (create new)
   - VM name: `vm-openclaw-01`
   - Region: pick nearest
   - Image: **Ubuntu Server 22.04 LTS**
   - Size: **Standard B2s** (2 vCPU, 4 GB)
   - Authentication: **SSH public key**
   - Username: `azureuser`
   - Inbound ports: **SSH (22) only**
3. Disks: Standard SSD
4. Networking: Public IP enabled, NSG basic, SSH only
5. **Review + Create → Create**

After deployment: copy the **Public IP** from VM → Overview.

---

## 2) SSH into the VM

```bash
ssh azureuser@<PUBLIC_IP>
# or with a specific key:
ssh -i ~/.ssh/<your_key> azureuser@<PUBLIC_IP>
```

---

## 3) Install Docker

### 3.1 Update packages

```bash
sudo apt-get update -y && sudo apt-get upgrade -y
```

### 3.2 Install Docker (official)

```bash
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 3.3 Allow docker without sudo

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### 3.4 Validate

```bash
docker --version
docker compose version
docker run --rm hello-world
```

---

## 4) Clone the repo and configure

```bash
sudo apt-get install -y git
git clone https://github.com/lucab85/openclaw.git
cd openclaw
```

### Create your `.env` from the example

```bash
cp .env.example .env
nano .env
```

Fill in your real API keys. **Never commit `.env`** — it's in `.gitignore`.

---

## 5) Run with Docker Compose

```bash
docker compose up -d
docker compose ps
docker compose logs -f --tail=100
```

To stop:

```bash
docker compose down
```

---

## 6) Open the Azure firewall for port 3000

1. Azure Portal → VM → **Networking**
2. **Add inbound port rule**:
   - Destination port: `3000`
   - Protocol: TCP
   - Source: **Your IP** (safest) or "Any" for quick demo
   - Name: `allow-openclaw-3000`

---

## 7) Verify

### From the VM

```bash
curl -I http://localhost:3000
```

### From your laptop

Open: `http://<PUBLIC_IP>:3000`

---

## 8) Troubleshooting (80/20)

| Check | Command |
|-------|---------|
| Container running? | `docker compose ps` |
| Port mapped? | `sudo ss -tulpn \| grep 3000` |
| Azure NSG open? | VM → Networking → check inbound rule |
| App binding? | Ensure app listens on `0.0.0.0`, not `127.0.0.1` |

---

## 9) Quick hardening (recommended)

### UFW firewall

```bash
sudo apt-get install -y ufw
sudo ufw allow 22/tcp
sudo ufw allow 3000/tcp
sudo ufw enable
sudo ufw status
```

### Disable password SSH

```bash
sudo nano /etc/ssh/sshd_config
```

Set:
- `PasswordAuthentication no`
- `PermitRootLogin no`

```bash
sudo systemctl restart ssh
```

---

## On-camera notes

- "We start with **SSH only** open. We open the app port **after** the service is running."
- "Goal is not 'it runs' — goal is **it runs predictably and safely**."
- "If it fails: check **ports → docker → env vars → firewall**, in that order."
