# BLE Scanner

A simple Python script to scan for BLE devices advertising with the name "hublink".

## Setup

1. Create and activate a virtual environment:
    ```bash
    # On Windows
    python -m venv venv
    venv\Scripts\activate

    # On Linux/MacOS
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install requirements:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the scanner:

```bash
python ble_scanner.py
```

The script will:
- Continuously scan for BLE devices with "hublink" in their name (case insensitive)
- Display the following information for each matching device:
  - Device name
  - MAC address
  - RSSI (signal strength)
  - Additional advertisement details
- Press 'q' to quit the application

## Requirements

- Python 3.7 or higher
- Bluetooth adapter with BLE support
- Operating system permissions for Bluetooth access

## Notes

### Linux Users
- You may need to run with sudo:
  ```bash
  sudo python ble_scanner.py
  ```
- Alternatively, add your user to the bluetooth group:
  ```bash
  sudo usermod -a -G bluetooth $USER
  ```
  (Requires logout/login to take effect)

### General
- Ensure Bluetooth is enabled on your system
- Keep devices within reasonable range for detection
