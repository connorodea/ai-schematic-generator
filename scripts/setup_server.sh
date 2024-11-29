#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Setting up AI Schematics server...${NC}"

# Install dependencies
apt-get update
apt-get install -y python3-pip nginx

# Create application directory
mkdir -p /opt/aischematics
cd /opt/aischematics

# Clone repository
git clone https://github.com/connorodea/ai-schematic-generator.git .

# Install Python dependencies
pip install -e .

# Create systemd service
cat > /etc/systemd/system/aischematics.service << 'SERVICE'
[Unit]
Description=AI Schematics Web Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/aischematics
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Environment="ANTHROPIC_API_KEY=your_api_key_here"
ExecStart=/usr/local/bin/gunicorn --workers 4 --bind unix:aischematics.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
SERVICE

# Configure Nginx
cat > /etc/nginx/sites-available/aischematics << 'NGINX'
server {
    listen 80;
    server_name aischematics.connorodea.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/opt/aischematics/aischematics.sock\;
    }
}
NGINX

# Enable site
ln -s /etc/nginx/sites-available/aischematics /etc/nginx/sites-enabled/

# Start services
systemctl daemon-reload
systemctl start aischematics
systemctl enable aischematics
systemctl restart nginx

echo -e "${GREEN}Setup complete!${NC}"
