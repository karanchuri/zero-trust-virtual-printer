# 🖨️ Zero-Trust Virtual PDF Printer

A highly secure, zero-dependency (on the host) virtual printer that acts as a local network printer. It intercepts raw print jobs (like those bypassing native drivers), converts them to PDFs via Ghostscript, and saves them directly to your local machine.

Designed with **extreme "Defense in Depth" security** to safely sandbox Ghostscript and execute untrusted PostScript code.

## 🔒 Security Architecture: The "Bomb-Disposal Chamber"

PostScript is a Turing-complete programming language, and processing untrusted print jobs carries inherent security risks. This project isolates the rendering engine using a 6-layer security model:

1. **Ghostscript Sandbox:** Enforces the `-dSAFER` flag, preventing Ghostscript from executing OS commands or accessing arbitrary files.
2. **Read-Only Filesystem:** The entire container filesystem is `read_only`. An attacker cannot write scripts, modify the Python code, or gain persistence. (Ghostscript is given a temporary RAM disk `/tmp` to process files).
3. **Neutered Kernel:** Drops all Linux capabilities (`cap_drop: ALL`) preventing the container from altering system times, changing network routing, or escaping to the host.
4. **Non-Root Trapping:** Runs under a restricted, unprivileged user with `no-new-privileges:true` to permanently block `sudo` or privilege escalation.
5. **DNS Blackhole:** Container DNS is routed to a dead address (`127.0.0.0`). If a malicious script attempts to resolve a command-and-control server, it instantly fails.
6. **Binary Desert:** Package managers (`apt`) and network tools (`curl`, `wget`) are physically deleted during the image build. Even if an attacker gets a shell, they have no tools to download payloads.
7. **Resource Quotas:** Hard limits on CPU (`0.5` cores) and RAM (`256M`) prevent the container from being hijacked for crypto-mining or resource-exhaustion attacks.

## 🚀 Quick Start

### 1. Prerequisites
* [Docker](https://docs.docker.com/get-docker/) & Docker Compose installed.

### 2. Build and Run
Clone this repository and start the secure container:
```bash
git clone https://github.com/karanchuri/zero-trust-virtual-printer.git
cd zero-trust-virtual-printer

# Start the container in the background
docker compose up -d --build

# Printer setup
Use IP: 127.0.0.1 for setup
