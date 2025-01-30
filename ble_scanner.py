import asyncio
from bleak import BleakScanner
import signal
import sys
import platform
from datetime import datetime

# Configuration
TARGET_DEVICE_NAME = "diagnostic"  # Change this to match your device name

# Flag to control the scanning loop
scanning = True

def signal_handler(sig, frame):
    global scanning
    print("\nExiting...")
    scanning = False

async def scan_for_devices():
    print(f"Scanning for BLE devices with name '{TARGET_DEVICE_NAME}'...")
    print("Press Ctrl+C to quit")
    
    global scanning
    while scanning:
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[{current_time}] Scanning...")
            
            devices = await BleakScanner.discover(timeout=5.0, return_adv=True)
            
            found_devices = False
            
            for device, adv_data in devices.items():
                try:
                    device_name = None
                    rssi = None
                    
                    # Handle macOS specific case where adv_data is a tuple
                    if isinstance(adv_data, tuple) and len(adv_data) == 2:
                        ble_device, advertisement = adv_data
                        device_name = advertisement.local_name
                        rssi = advertisement.rssi
                    else:
                        # Linux/other platforms
                        if hasattr(adv_data, 'local_name'):
                            device_name = adv_data.local_name
                        if hasattr(adv_data, 'rssi'):
                            rssi = adv_data.rssi
                    
                    # If we found a name and it matches our target
                    if device_name and TARGET_DEVICE_NAME.lower() in str(device_name).lower():
                        found_devices = True
                        print("\nFound matching device:")
                        print(f"Name: {device_name}")
                        print(f"Address: {device}")  # device is the address on macOS
                        if rssi is not None:
                            print(f"RSSI: {rssi} dBm")
                        print("-" * 50)
                
                except Exception as device_error:
                    print(f"Error processing device: {device_error}")
                    continue
            
            if not found_devices:
                print(f"No '{TARGET_DEVICE_NAME}' devices found in this scan")
                print("-" * 50)

        except Exception as e:
            print(f"Scan error: {e}")
            if "permission" in str(e).lower():
                if platform.system() == "Darwin":  # macOS
                    print("On macOS, ensure Bluetooth is enabled and the app has Bluetooth permissions")
                elif platform.system() == "Linux":
                    print("On Linux, try running with sudo or add your user to the bluetooth group:")
                    print("sudo usermod -a -G bluetooth $USER")
            continue

async def main():
    try:
        if platform.system() != "Windows":  # Unix-like systems (macOS, Linux)
            loop = asyncio.get_event_loop()
            loop.add_signal_handler(signal.SIGINT, signal_handler, signal.SIGINT, None)
            loop.add_signal_handler(signal.SIGTERM, signal_handler, signal.SIGTERM, None)
        
        await scan_for_devices()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if platform.system() != "Windows":
            loop = asyncio.get_event_loop()
            loop.remove_signal_handler(signal.SIGINT)
            loop.remove_signal_handler(signal.SIGTERM)

if __name__ == "__main__":
    asyncio.run(main()) 