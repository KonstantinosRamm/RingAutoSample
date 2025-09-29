## Getting Started

Follow these steps to set up the project locally.

```bash
# 1. Install Python 3 (Linux example)
sudo apt update
sudo apt install python3 python3-venv python3-pip -y

# 2. Verify installation
python3 --version
pip3 --version

# 3. Create a virtual environment
python3 -m venv venv

# 4. Activate the virtual environment
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\Activate.ps1  # Windows PowerShell
# OR
venv\Scripts\activate.bat  # Windows CMD

# 5. Install project dependencies
pip install -r requirements.txt

# 6. Run the project
python main.py


