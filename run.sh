#!/bin/bash

# ATHEX-SPY Basic Installation Script
# Checks and installs required dependencies

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print banner
echo -e "${GREEN}"
echo '            █████████   ███████████ █████   █████ ██████████ █████ █████                   █████████  ███████████  █████ █████'
echo '           ███░░░░░███ ░█░░░███░░░█░░███   ░░███ ░░███░░░░░█░░███ ░░███                   ███░░░░░███░░███░░░░░███░░███ ░░███ '
echo '          ░███    ░███ ░   ░███  ░  ░███    ░███  ░███  █ ░  ░░███ ███                   ░███    ░░░  ░███    ░███ ░░███ ███  '
echo '          ░███████████     ░███     ░███████████  ░██████     ░░█████       ██████████   ░░█████████  ░██████████   ░░█████   '
echo '          ░███░░░░░███     ░███     ░███░░░░░███  ░███░░█      ███░███     ░░░░░░░░░░     ░░░░░░░░███ ░███░░░░░░     ░░███    '
echo '          ░███    ░███     ░███     ░███    ░███  ░███ ░   █  ███ ░░███                   ███    ░███ ░███            ░███    '
echo '          █████   █████    █████    █████   █████ ██████████ █████ █████                 ░░█████████  █████           █████   '
echo '          ░░░░░   ░░░░░    ░░░░░    ░░░░░   ░░░░░ ░░░░░░░░░░ ░░░░░ ░░░░░                   ░░░░░░░░░  ░░░░░           ░░░░░    '
echo -e "${CYAN}════════════════════════════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}                     ADVANCED EXPLOITATION SYSTEM${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════════════════════════════════════════${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install packages based on OS
install_package() {
    local package=$1
    echo -e "${YELLOW}Installing $package...${NC}"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command_exists apt-get; then
            sudo apt-get update && sudo apt-get install -y "$package"
        elif command_exists dnf; then
            sudo dnf install -y "$package"
        elif command_exists yum; then
            sudo yum install -y "$package"
        elif command_exists pacman; then
            sudo pacman -S --noconfirm "$package"
        else
            echo -e "${RED}Package manager not found. Please install $package manually.${NC}"
            return 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command_exists brew; then
            brew install "$package"
        else
            echo -e "${RED}Homebrew not found. Please install $package manually.${NC}"
            return 1
        fi
    else
        echo -e "${RED}Unsupported OS. Please install $package manually.${NC}"
        return 1
    fi
}

echo -e "${GREEN}[*] Checking installation requirements...${NC}\n"

# Check Python3
echo -ne "${GREEN}Checking Python3... ${NC}"
if command_exists python3; then
    python_version=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Found version $python_version${NC}"
else
    echo -e "${RED}✗ Not found${NC}"
    echo -e "${YELLOW}Please install Python 3.6 or higher${NC}"
    exit 1
fi

# Check pip3
echo -ne "${GREEN}Checking pip3... ${NC}"
if command_exists pip3; then
    echo -e "${GREEN}✓ Found${NC}"
else
    echo -e "${RED}✗ Not found${NC}"
    echo -e "${YELLOW}Installing pip3...${NC}"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install -y python3-pip
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        python3 -m ensurepip --upgrade
    fi
fi

echo ""

# Required packages
REQUIRED_PACKAGES=("adb" "scrcpy" "nmap")
MISSING_PACKAGES=()

# Check each required package
echo -e "${GREEN}[*] Checking system requirements:${NC}"
for pkg in "${REQUIRED_PACKAGES[@]}"; do
    echo -ne "  Checking $pkg... "
    if command_exists $pkg; then
        echo -e "${GREEN}✓ Installed${NC}"
    else
        echo -e "${RED}✗ Not found${NC}"
        MISSING_PACKAGES+=($pkg)
    fi
done

# Install missing packages
if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}[*] The following packages need to be installed:${NC}"
    for pkg in "${MISSING_PACKAGES[@]}"; do
        echo "  - $pkg"
    done
    
    echo ""
    read -p "Do you want to install them now? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        for pkg in "${MISSING_PACKAGES[@]}"; do
            install_package $pkg
        done
    else
        echo -e "${YELLOW}Please install the missing packages manually and run this script again.${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}[*] Checking Python requirements:${NC}"

# Python dependencies
PYTHON_REQUIREMENTS=(
    "colorama"
    "python-nmap"
    "requests"
    "cryptography"
)

# Check and install Python packages
for req in "${PYTHON_REQUIREMENTS[@]}"; do
    echo -ne "  Checking $req... "
    if python3 -c "import $req" 2>/dev/null; then
        echo -e "${GREEN}✓ Installed${NC}"
    else
        echo -e "${YELLOW}Installing...${NC}"
        pip3 install $req
    fi
done

# Install additional Python requirements from requirements.txt if exists
if [ -f "requirements.txt" ]; then
    echo ""
    echo -e "${GREEN}[*] Installing additional Python requirements...${NC}"
    pip3 install -r requirements.txt
fi

# Create Downloaded-Files directory if it doesn't exist
if [ ! -d "Downloaded-Files" ]; then
    echo ""
    echo -e "${GREEN}[*] Creating Downloaded-Files directory...${NC}"
    mkdir -p Downloaded-Files
fi

# Make the main script executable
if [ -f "ATHEX-SPY.py" ]; then
    chmod +x ATHEX-SPY.py
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}                    ✓ ATHEX-SPY installation completed successfully! ✓${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}To start ATHEX-SPY, run:${NC}"
echo -e "  ${GREEN}python3 ATHEX-SPY.py${NC}"
echo ""
echo -e "${YELLOW}Note: Make sure USB debugging is enabled on your Android device${NC}"
echo -e "${YELLOW}      and it's connected via USB or same network.${NC}"
echo ""

# Ask if user wants to run ATHEX-SPY now
read -p "Do you want to run ATHEX-SPY now? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "\n${GREEN}[*] Starting ATHEX-SPY...${NC}\n"
    python3 ATHEX-SPY.py
else
    echo -e "\n${GREEN}Installation complete! Run 'python3 ATHEX-SPY.py' when ready.${NC}"
fi