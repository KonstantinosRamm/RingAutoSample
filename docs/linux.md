## DEBIAN BASED DISTROS

# 1. Install Python 3
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
source venv/bin/activate
```

# 5. Install project dependencies
```bash
pip install -r requirements.txt
```

# 6. Run the project

```bash
source venv/bin/activate
flask run
```

