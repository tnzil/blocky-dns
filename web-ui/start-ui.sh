#!/bin/bash
# Blocky DNS Web UI Startup Script

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is installed
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        log_success "Python 3 found: $(python3 --version)"
    elif command -v python &> /dev/null && python --version | grep -q "Python 3"; then
        PYTHON_CMD="python"
        log_success "Python 3 found: $(python --version)"
    else
        log_error "Python 3 is required but not found. Please install Python 3."
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
        log_success "pip3 found"
    elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
        log_success "pip found"
    else
        log_error "pip is required but not found. Please install pip."
        exit 1
    fi
}

# Install Python dependencies
install_dependencies() {
    log_info "Installing Python dependencies..."
    
    if [ -f "requirements.txt" ]; then
        $PIP_CMD install -r requirements.txt
        if [ $? -eq 0 ]; then
            log_success "Dependencies installed successfully"
        else
            log_error "Failed to install dependencies"
            exit 1
        fi
    else
        log_error "requirements.txt not found"
        exit 1
    fi
}

# Start the web UI
start_ui() {
    log_info "Starting Blocky DNS Web UI..."
    echo -e "${GREEN}"
    echo "=================================="
    echo "  Blocky DNS Management Web UI"
    echo "=================================="
    echo -e "${NC}"
    echo "Access the web interface at:"
    echo "  - Local:   http://localhost:8080"
    echo "  - Network: http://$(hostname -I | awk '{print $1}'):8080"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    $PYTHON_CMD app.py
}

# Main execution
main() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════╗"
    echo "║     Blocky DNS Web UI Launcher       ║"
    echo "╚══════════════════════════════════════╝"
    echo -e "${NC}"
    
    log_info "Checking system requirements..."
    check_python
    check_pip
    
    # Check if running as root (needed for some system operations)
    if [ "$EUID" -ne 0 ]; then
        log_warning "Not running as root. Some features may be limited."
        log_warning "For full functionality, run: sudo $0"
    fi
    
    # Install dependencies if needed
    if [ "$1" = "--install-deps" ] || [ ! -d "venv" ]; then
        install_dependencies
    fi
    
    start_ui
}

# Parse command line arguments
case "$1" in
    --help|-h)
        echo "Blocky DNS Web UI Launcher"
        echo ""
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --install-deps    Force install/update dependencies"
        echo "  --help, -h        Show this help message"
        echo ""
        echo "The web interface will be available at http://localhost:8080"
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac