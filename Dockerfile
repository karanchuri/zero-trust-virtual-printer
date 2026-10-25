# Use a pinned, slim Debian-based Python image
FROM python:3.12-slim

# Install Ghostscript and clean up apt cache
RUN apt-get update && \
    apt-get install -y --no-install-recommends ghostscript && \
    rm -rf /var/lib/apt/lists/*

# --- BINARY DESERT ---
# Physically delete the package manager and network tools.
# A compromised process cannot download payloads even if it gets a shell.
RUN rm -rf /usr/bin/apt* /usr/bin/dpkg* /usr/bin/curl /usr/bin/wget

# Create a non-root user and group
RUN groupadd -r printergroup && useradd -r -g printergroup printeruser

WORKDIR /app
COPY printer.py .

# Create the output directory and assign ownership to our restricted user
RUN mkdir -p /app/print_jobs && chown -R printeruser:printergroup /app

# Switch to the restricted user to drop root privileges
USER printeruser

# Run the server (-u forces unbuffered output so logs show up instantly)
CMD ["python", "-u", "printer.py"]
