from bluepy.btle import Scanner, UUID, Peripheral, DefaultDelegate
import uuid
import random
import subprocess

# Define the UUID for the Battery Level characteristic
battery_level_uuid = UUID(0x2A19)
devices = ""
def generate_random_mac_address():
    # Generate a random MAC address
    mac = [0x00, 0x16, 0x3e, random.randint(0x00, 0x7f), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def spoof_mac_address():
    # Spoof raspi4  MAC address
    interface_name = "eth0"  # Assuming the interface name is eth0
    new_mac = generate_random_mac_address()
    print("Spoofing MAC address of", interface_name, "to:", new_mac)
    
    
    # Bring the interface down
    subprocess.call(["sudo", "ifconfig", interface_name, "down"])
    # Bring the interface up
    subprocess.call(["sudo", "hciconfig", "hci0", "up"])
    # Set the new MAC address
    subprocess.call(["sudo", "ifconfig", interface_name, "hw", "ether", new_mac])
    # Set the scan mode
    subprocess.call(["sudo", "hciconfig", interface_name, "piscan"])
    #subprocess.call(["sudo", "ifconfig", "eth0", new_mac])
    # Change the local name (Optional)
    subprocess.call(["sudo", "ifconfig", interface_name, "up"])

def discover_and_interact_with_ble_devices():
    # Scan for BLE devices
    scanner = Scanner().withDelegate(DefaultDelegate())
    devices = scanner.scan(3.0)  # Scan for 3 seconds
    
    print("\nList of discovered devices:")
    for idx, device in enumerate(devices, start=1):
        print("{}. Device ({}), RSSI={} dB".format(idx, device.addr, device.rssi))
        for (adtype, desc, value) in device.getScanData():
            print("   {} = {}".format(desc, value))

        # Check if the battery level UUID is in the scan data
        if battery_level_uuid.getCommonName() in [desc for (_, desc, _) in device.getScanData()]:
            print("   Battery Level characteristic found on", device.addr)

            try:
                # Connect to the device
                peripheral = Peripheral(device)

                # Read Battery Level value
                battery_level_char = peripheral.getCharacteristics(uuid=battery_level_uuid)[0]
                battery_level = battery_level_char.read()
                print("   Battery Level: {}%".format(ord(battery_level)))

                # Interaction: Write data to a writable characteristic (example)
                # Find a writable characteristic (for demonstration purposes)
                writable_char = None
                for char in peripheral.getCharacteristics():
                    if char.supportsRead() and char.supportsWrite():
                        writable_char = char
                        break

                if writable_char:
                    # Example: Write a custom value (byte) to the characteristic
                    value_to_write = b'\x01'  # Example custom value (byte)
                    writable_char.write(value_to_write, withResponse=True)
                    print("   Data written to characteristic successfully.")

                peripheral.disconnect()
            except Exception as e:
                print("Error:", e)



def select_device(devices):

    #Prompt the user to select a device
    print("Select a device to connect:")
    for i, device in enumerate(devices):
       print(f"{i + 1}. Device ({device.addr}), Name={device.getValueText(9)}, RSSI={device.rssi} dB")
    
    while True:
        choice = input("Enter the device number to connect (or press Enter to skip): ")
        if choice.isdigit() and 0< int(choice) <= len(devices):
            return device[int(choice) -1]
        elif choice == "":
            print("Skipping device selection.")
            return None
        else:
            print("Invalid choice. Please enter a valid device number.")

'''
def select_device(devices):
    # Prompt the user to select a device
    print("Select a device to connect:")
    for i, device in enumerate(devices):
        print(f"{i + 1}. Device ({device.addr}), Name={device.getValueText(9)}, RSSI={device.rssi} dB")
    
    while True:
        choice = input("Enter the device number to connect (or press Enter to skip): ")
        if choice.isdigit():
            choice = int(choice)
            if 0 < choice <= len(devices):
                return devices[choice - 1]
            else:
                print("Invalid choice. Please enter a valid device number.")
        elif choice == "":
            print("Skipping device selection.")
            return None
        else:
            print("Invalid choice. Please enter a valid device number.")

def main():
    generate_random_mac_address()
    # Spoof the MAC address of the Raspberry Pi
    spoof_mac_address()

    # Scan for BLE devices and interact with Battery Level characteristic
    devices = discover_and_interact_with_ble_devices()

    select_device(devices)
    sekected_device = select_device()
    # Now you can use 'selected_device' to perform further actions, e.g., establish connection

    if selected_device:
        print("Selected device:", selected_device.addr)
    else:
        print("No device selected.")

if __name__ == "__main__":
    main()

'''
def main():
    generate_random_mac_address()
    # Spoof the MAC address of the Raspberry Pi
    spoof_mac_address()

    # Scan for BLE devices and interact with Battery Level characteristic
    discover_and_interact_with_ble_devices()

    selected_device = select_device(devices)

if __name__ == "__main__":
    main()
