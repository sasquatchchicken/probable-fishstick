## Introduction

This repository contains a Python script designed for simulating BLE (Bluetooth Low Energy) payload injection scenarios. The script interacts with BLE devices, discovers their characteristics, and demonstrates potential security vulnerabilities that could be exploited by malicious threat actors for payload injection.

The purpose of this repository is to provide security professionals, researchers, and enthusiasts with a tool to understand and simulate threats related to BLE security. By demonstrating various payload injection techniques, users can gain insights into potential attack vectors and strengthen their security posture.

## Features

    Spoofing MAC address to demonstrate stealthy reconnaissance techniques.
    Scanning for BLE devices and interacting with their characteristics.
    Demonstration of payload injection scenarios with selected BLE devices.
    User-friendly interface for device selection and interaction.

## Usage

    Setup Environment:
        Ensure Python 3.x is installed on your system.
        Install the required dependencies using pip install -r requirements.txt.

    Running the Script: 
        sudo python3 bluit.py
        Follow the on-screen instructions to perform BLE device discovery and interaction.

    Selecting Devices:
        Upon discovery of BLE devices, the script prompts the user to select a device for further interaction.
        Users can input the device number to connect or skip the selection.
        NOTE further interaction has been left out. Act accordingly and always in the bounds of the law.


## Threat Scenarios

This repository demonstrates four potential threat scenarios involving BLE payload injection:

    Insider Threat - Unauthorized Access:
        An insider threat leverages the script to gain unauthorized access to sensitive BLE devices within the organization's premises.
        Using spoofed MAC addresses, the insider performs stealthy reconnaissance and selects target devices for payload injection.

    Insider Threat - Data Exfiltration:
        Another insider threat utilizes payload injection techniques to exfiltrate sensitive data from BLE devices.
        By exploiting vulnerabilities in device characteristics, the insider extracts and exfiltrates data without detection.

    Nefarious Threat Actor - Malware Distribution:
        A nefarious threat actor deploys malware using BLE payload injection techniques.
        The actor identifies vulnerable BLE devices and injects malicious payloads, facilitating the distribution of malware within the target environment.

    Nefarious Threat Actor - Physical Security Bypass:
        In a physical security bypass scenario, a threat actor leverages BLE payload injection to bypass physical security controls.
        By injecting payloads into access control systems or security devices, the actor gains unauthorized access to restricted areas.

## Disclaimer

This repository and the associated script are intended for educational and research purposes only. Users are solely responsible for their actions and should use the tool in compliance with applicable laws and regulations. The authors do not condone or support any malicious activities.
