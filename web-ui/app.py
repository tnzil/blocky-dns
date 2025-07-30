#!/usr/bin/env python3
"""
Blocky DNS Web UI
A web-based interface for managing Blocky DNS installation and configuration
"""

import os
import subprocess
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import yaml

app = Flask(__name__)
app.secret_key = 'blocky-dns-ui-secret-key'

# Custom template filters
@app.template_filter('to_nice_yaml')
def to_nice_yaml(value):
    """Convert a Python object to nicely formatted YAML"""
    return yaml.dump(value, default_flow_style=False, sort_keys=False, indent=2)

# Configuration
BLOCKY_PATH = '/opt/blocky'
INSTALL_SCRIPT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'install.sh')
UTILS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils')

class BlockyManager:
    """Manages Blocky DNS installation and configuration"""
    
    def __init__(self):
        self.blocky_path = BLOCKY_PATH
        self.install_script = INSTALL_SCRIPT
        
    def get_installation_status(self):
        """Check if Blocky is installed and running"""
        status = {
            'installed': False,
            'running': False,
            'service_exists': False,
            'config_exists': False,
            'binary_exists': False
        }
        
        # Check if directory exists
        if os.path.exists(self.blocky_path):
            status['installed'] = True
            
        # Check if binary exists
        binary_path = os.path.join(self.blocky_path, 'blocky')
        if os.path.exists(binary_path):
            status['binary_exists'] = True
            
        # Check if config exists
        config_path = os.path.join(self.blocky_path, 'config.yml')
        if os.path.exists(config_path):
            status['config_exists'] = True
            
        # Check if service exists and is running
        try:
            result = subprocess.run(['systemctl', 'is-active', 'blocky'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                status['running'] = True
                status['service_exists'] = True
        except FileNotFoundError:
            pass
            
        try:
            subprocess.run(['systemctl', 'cat', 'blocky'], 
                          capture_output=True, text=True, check=True)
            status['service_exists'] = True
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass
            
        return status
    
    def get_system_info(self):
        """Get system information"""
        info = {
            'hostname': 'Unknown',
            'os': 'Unknown',
            'uptime': 'Unknown',
            'memory': 'Unknown'
        }
        
        try:
            info['hostname'] = subprocess.check_output(['hostname']).decode().strip()
        except subprocess.CalledProcessError:
            pass
            
        try:
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('PRETTY_NAME='):
                        info['os'] = line.split('=')[1].strip().strip('"')
                        break
        except FileNotFoundError:
            pass
            
        try:
            uptime = subprocess.check_output(['uptime', '-p']).decode().strip()
            info['uptime'] = uptime
        except subprocess.CalledProcessError:
            pass
            
        return info
    
    def get_config(self):
        """Load Blocky configuration"""
        config_path = os.path.join(self.blocky_path, 'config.yml')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                return {'error': str(e)}
        return None
    
    def save_config(self, config_data):
        """Save Blocky configuration"""
        config_path = os.path.join(self.blocky_path, 'config.yml')
        try:
            with open(config_path, 'w') as f:
                yaml.dump(config_data, f, default_flow_style=False)
            return True
        except Exception as e:
            return str(e)
    
    def install_blocky(self, auto=False):
        """Install Blocky using the install script"""
        try:
            cmd = ['bash', self.install_script]
            if auto:
                cmd.append('-a')
            
            # Run installation script
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'output': '',
                'error': 'Installation timed out'
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e)
            }
    
    def restart_service(self):
        """Restart Blocky service"""
        try:
            result = subprocess.run(['sudo', 'systemctl', 'restart', 'blocky'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def get_logs(self, lines=50):
        """Get Blocky service logs"""
        try:
            result = subprocess.run(['journalctl', '-u', 'blocky', '-n', str(lines), '--no-pager'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            return "No logs available"
        except Exception:
            return "Error retrieving logs"

# Initialize manager
blocky_manager = BlockyManager()

@app.route('/')
def index():
    """Main dashboard"""
    status = blocky_manager.get_installation_status()
    system_info = blocky_manager.get_system_info()
    return render_template('index.html', status=status, system_info=system_info)

@app.route('/install')
def install():
    """Installation page"""
    status = blocky_manager.get_installation_status()
    return render_template('install.html', status=status)

@app.route('/api/install', methods=['POST'])
def api_install():
    """API endpoint for installation"""
    auto_install = request.json.get('auto', False)
    result = blocky_manager.install_blocky(auto=auto_install)
    return jsonify(result)

@app.route('/config')
def config():
    """Configuration management page"""
    status = blocky_manager.get_installation_status()
    if not status['config_exists']:
        flash('Blocky configuration not found. Please install Blocky first.', 'warning')
        return redirect(url_for('install'))
    
    config_data = blocky_manager.get_config()
    return render_template('config.html', config=config_data, status=status)

@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """API endpoint for configuration management"""
    if request.method == 'GET':
        config_data = blocky_manager.get_config()
        return jsonify(config_data)
    
    elif request.method == 'POST':
        config_data = request.json
        result = blocky_manager.save_config(config_data)
        if result is True:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': result})

@app.route('/logs')
def logs():
    """Logs viewer page"""
    status = blocky_manager.get_installation_status()
    logs_data = blocky_manager.get_logs() if status['service_exists'] else "Service not installed"
    return render_template('logs.html', logs=logs_data, status=status)

@app.route('/api/restart', methods=['POST'])
def api_restart():
    """API endpoint to restart Blocky service"""
    success = blocky_manager.restart_service()
    return jsonify({'success': success})

@app.route('/api/status')
def api_status():
    """API endpoint for status information"""
    status = blocky_manager.get_installation_status()
    system_info = blocky_manager.get_system_info()
    return jsonify({
        'status': status,
        'system_info': system_info
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)