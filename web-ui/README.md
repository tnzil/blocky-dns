# Blocky DNS Web UI

A modern, web-based management interface for the Blocky DNS installer and configuration.

## Features

### 📊 Dashboard
- **Real-time Status Monitoring**: View installation status, service health, and system information
- **Quick Actions**: Easy access to common tasks like installation, configuration, and log viewing
- **Service Overview**: Visual indicators for DNS protection, ad blocking, and service status

### 🚀 Installation Management
- **Interactive Installation**: Step-by-step installer with progress tracking
- **Auto-Install Mode**: One-click installation with default settings
- **Update Support**: Update existing installations to the latest version
- **System Requirements Check**: Verify compatibility before installation

### ⚙️ Configuration Management
- **Visual Config Editor**: User-friendly interface for editing Blocky settings
- **Blocklist Management**: Add, remove, and manage DNS blocklists
- **Allowlist Management**: Configure domains that should never be blocked
- **Upstream DNS Settings**: Configure DNS servers and bootstrap settings
- **Raw YAML Editor**: Advanced editing with syntax validation

### 📋 Log Monitoring
- **Real-time Logs**: View Blocky service logs with auto-refresh
- **Log Filtering**: Search and filter logs by keywords
- **Log Statistics**: Count of info, warning, and error messages
- **Export Functionality**: Download logs for analysis

### 🔧 System Management
- **Service Control**: Start, stop, and restart Blocky service
- **Configuration Validation**: Check configuration syntax before applying
- **Backup & Restore**: Manage configuration backups
- **System Information**: Display server details and status

## Screenshots

![Dashboard](screenshots/dashboard.png)
*Main dashboard showing service status and quick actions*

![Installation](screenshots/installation.png)
*Installation wizard with progress tracking*

![Configuration](screenshots/configuration.png)
*Configuration editor with tabbed interface*

![Logs](screenshots/logs.png)
*Log viewer with filtering and statistics*

## Installation & Usage

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)
- Root access (for full functionality)

### Quick Start

1. **Navigate to the web-ui directory:**
   ```bash
   cd web-ui
   ```

2. **Run the startup script:**
   ```bash
   ./start-ui.sh
   ```

3. **Access the web interface:**
   - Open your browser and go to `http://localhost:8080`
   - Or access from network: `http://YOUR_SERVER_IP:8080`

### Manual Installation

1. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Start the application:**
   ```bash
   python3 app.py
   ```

### Running as a Service

To run the web UI as a systemd service:

1. **Create service file:**
   ```bash
   sudo nano /etc/systemd/system/blocky-ui.service
   ```

2. **Add service configuration:**
   ```ini
   [Unit]
   Description=Blocky DNS Web UI
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/path/to/blocky-dns/web-ui
   ExecStart=/usr/bin/python3 app.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and start service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable blocky-ui
   sudo systemctl start blocky-ui
   ```

## Configuration

### Environment Variables
- `BLOCKY_PATH`: Path to Blocky installation (default: `/opt/blocky`)
- `FLASK_HOST`: Host to bind to (default: `0.0.0.0`)
- `FLASK_PORT`: Port to listen on (default: `8080`)
- `FLASK_DEBUG`: Enable debug mode (default: `False`)

### Security Considerations
- The web UI requires root access for system operations
- Consider using a reverse proxy (nginx/apache) for production
- Implement authentication for network access
- Use HTTPS in production environments

## API Endpoints

The web UI provides a REST API for integration:

### Status API
- `GET /api/status` - Get installation and service status
- `POST /api/restart` - Restart Blocky service

### Installation API
- `POST /api/install` - Install or update Blocky
  ```json
  {
    "auto": true  // Enable auto-install mode
  }
  ```

### Configuration API
- `GET /api/config` - Get current configuration
- `POST /api/config` - Update configuration
  ```json
  {
    "upstream": {
      "default": ["1.1.1.1", "8.8.8.8"]
    },
    "blocking": {
      "denylists": {
        "ads": ["https://example.com/blocklist.txt"]
      }
    }
  }
  ```

## Browser Compatibility

The web UI is compatible with:
- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Icons**: Font Awesome 6
- **Configuration**: PyYAML
- **Styling**: Custom CSS with Bootstrap theming

## Development

### Project Structure
```
web-ui/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── start-ui.sh           # Startup script
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Dashboard
│   ├── install.html      # Installation page
│   ├── config.html       # Configuration editor
│   └── logs.html         # Log viewer
└── static/               # Static assets
    ├── css/
    │   └── custom.css    # Custom styles
    └── js/
        └── app.js        # JavaScript functionality
```

### Adding New Features

1. **Backend**: Add routes and logic to `app.py`
2. **Frontend**: Create templates in `templates/`
3. **Styling**: Add styles to `static/css/custom.css`
4. **JavaScript**: Add functionality to `static/js/app.js`

### Testing

Run the application in debug mode:
```bash
export FLASK_DEBUG=1
python3 app.py
```

## Troubleshooting

### Common Issues

1. **Permission Denied**: Run with sudo for system operations
2. **Port Already in Use**: Change port with `FLASK_PORT` environment variable
3. **Python Dependencies**: Install with `pip3 install -r requirements.txt`
4. **Service Not Found**: Ensure Blocky is installed first

### Debug Mode

Enable debug mode for detailed error information:
```bash
export FLASK_DEBUG=1
./start-ui.sh
```

### Logs

Check application logs:
```bash
# If running as service
sudo journalctl -u blocky-ui -f

# If running manually
# Check console output
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This web UI is part of the Blocky DNS installer project and follows the same license terms.

## Support

For issues and support:
1. Check the troubleshooting section
2. Review the main project documentation
3. Open an issue on GitHub