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
    global devices
    # Scan for BLE devices
    scanner = Scanner().withDelegate(DefaultDelegate())
    devices = scanner.scan(9.0)  # Scan for 9 seconds
    
    discovered_devices = list(devices)  # Convert dict_values to a list
    
    print("\nList of discovered devices:")
    for idx, device in enumerate(discovered_devices, start=1):
        print("{}. Device ({}), RSSI={} dB".format(idx, device.addr, device.rssi))
        
        # Extract and print the human-readable name if available
        name = device.getValueText(9)  # Assuming the device name is stored with AD type 9 (Complete Local Name)
        if name:
            print("   Name:", name)
        
        for (adtype, desc, value) in device.getScanData():
            print("   {} = {}".format(desc, value))

        # Check if the battery level UUID is in the scan data
        if battery_level_uuid.getCommonName() in [desc for (_, desc, _) in device.getScanData()]:
            print("   \nBattery Level characteristic found on", device.addr)

            try:
                # Connect to the device
                peripheral = Peripheral(device)

                # Read Battery Level value
                battery_level_char = peripheral.getCharacteristics(uuid=battery_level_uuid)[0]
                battery_level = battery_level_char.read()
                print("   \nBattery Level: {}%".format(ord(battery_level)))

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
                    print("   \nData written to characteristic successfully.")

                peripheral.disconnect()
            except Exception as e:
                print("Error:", e)
        
        # Print all scan data for debugging
        print("   \nAll Scan Data:")
        for (adtype, desc, value) in device.getScanData():
            print("      {} = {}".format(desc, value))
    
    return discovered_devices  # Return the list of devices

def select_device(devices):
    
    #Prompt the user to select a device
    print("Select a device to connect:")
    for i, device in enumerate(devices):
       #print(f"{i + 1}. Device ({device.addr}), Name={device.getValueText(9)}, RSSI={device.rssi} dB")
    
    #while True:
        choice = input("Enter the device number to connect (or press Enter to skip): ")
        if choice.isdigit() and 0< int(choice) <= len(devices):
            return devices[int(choice) -1] 
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
    discovered_devices = discover_and_interact_with_ble_devices()

    # Store the selected device
    selected_device = select_device(discovered_devices)
    
    # If a device is selected, you can do further operations with it
    if selected_device:
        # Do something with selected_device
        print("Selected device:", selected_device.addr)
    else:
        print("No device selected.")

if __name__ == "__main__":
    main()
