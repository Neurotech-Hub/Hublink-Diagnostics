import asyncio
from bleak import BleakScanner
import signal
import sys
import platform

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
            devices = await BleakScanner.discover(timeout=5.0)
            
            found_devices = False
            for device in devices:
                if device.name and TARGET_DEVICE_NAME.lower() in device.name.lower():
                    found_devices = True
                    print("\nFound matching device:")
                    print(f"Name: {device.name}")
                    print(f"Address: {device.address}")
                    print(f"RSSI: {device.rssi} dBm")
                    print(f"Details: {device.details}")
                    print("-" * 50)
            
            if not found_devices:
                print(f"\nNo '{TARGET_DEVICE_NAME}' devices found in this scan")
                print("-" * 50)

        except Exception as e:
            print(f"Scan error: {e}")
            # If we get a permission error, provide platform-specific guidance
            if "permission" in str(e).lower():
                if platform.system() == "Darwin":  # macOS
                    print("On macOS, ensure Bluetooth is enabled and the app has Bluetooth permissions")
                elif platform.system() == "Linux":
                    print("On Linux, try running with sudo or add your user to the bluetooth group:")
                    print("sudo usermod -a -G bluetooth $USER")
            continue

async def main():
    try:
        # Set up signal handlers for graceful exit
        if platform.system() != "Windows":  # Unix-like systems (macOS, Linux)
            loop = asyncio.get_event_loop()
            loop.add_signal_handler(signal.SIGINT, signal_handler, signal.SIGINT, None)
            loop.add_signal_handler(signal.SIGTERM, signal_handler, signal.SIGTERM, None)
        
        await scan_for_devices()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Ensure clean shutdown
        if platform.system() != "Windows":
            loop = asyncio.get_event_loop()
            loop.remove_signal_handler(signal.SIGINT)
            loop.remove_signal_handler(signal.SIGTERM)

if __name__ == "__main__":
    asyncio.run(main()) 