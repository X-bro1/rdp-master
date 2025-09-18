# RDP Master Cracker Ultimate

![Banner](https://img.shields.io/badge/Tool-RDP%20Cracker-red)
![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey)

A professional RDP penetration testing tool that displays every combination attempt in real-time with advanced visual feedback.

## ⚠️ LEGAL DISCLAIMER
**This tool is designed for AUTHORIZED PENETRATION TESTING ONLY.**
- Use only on systems you have explicit permission to test
- Unauthorized access to computer systems is illegal and punishable by law
- The developers are not responsible for any misuse of this tool
- Ensure you have written authorization before using this tool

## 🚀 Features

- Real-time display of every combination attempt with colored output
- Multi-threaded architecture for high-performance testing
- Dynamic thread management with configurable thread count
- Support for both user lists and fixed username modes
- Batch processing optimized for large wordlists
- Success logging to output file with immediate saving
- Professional terminal banner with rich formatting (optional)
- ETA calculation and progress monitoring
- Connection timeout configuration
- Comprehensive error handling and dependency checking

## 📦 Installation

### Prerequisites

- Python 3.6+
- FreeRDP2 (xfreerdp client)
- Linux environment (recommended)

### System Dependencies
```bash
# Install FreeRDP on Debian/Ubuntu
sudo apt update
sudo apt install freerdp2-x11

# Install FreeRDP on CentOS/RHEL
sudo yum install freerdp

# Install FreeRDP on Arch Linux
sudo pacman -S freerdp
``````
### Usage
```bash
python3 rdp_master.py -U Administrator -p passwords.txt -i ips.txt

python3 rdp_master.py -u users.txt -p passwords.txt -i ips.txt -t 50 -o results.txt
``````


🤝 For Support and more private tools:

🔗 Ko-fi: https://ko-fi.com/xbro1
🔗 https://buymeacoffee.com/xbro
🔗 https://www.paypal.me/AmineBouzama
📧 Telegram: https://t.me/+Djn6L6DK1jcyNjg8


🙏 Acknowledgments
- FreeRDP team for the excellent RDP client
- Python community for amazing libraries
- Cybersecurity professionals for continuous testing and feedback



