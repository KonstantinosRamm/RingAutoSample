## Getting Started

Follow these steps to set up the project locally.

# 1. Install Python 3 (Linux example)
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip -y
```

# 2. Verify installation
```bash
python3 --version
pip3 --version
```
# 3. Create a virtual environment
```bash
python3 -m venv venv
```
# 4. Activate the virtual environment
```bash
source venv/bin/activate  # Linux/macOS
```
# OR
```bash
venv\Scripts\Activate.ps1  # Windows PowerShell
```
# OR
```bash
venv\Scripts\activate.bat  # Windows CMD
```

# 5. Install project dependencies
```bash
pip install -r requirements.txt
```

# 6. Run the project
```bash
python main.py
```

