#!/usr/bin/env python3
import os
import subprocess

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Successfully executed: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e}")

def main():
    # Update system and upgrade packages
    print("Updating system and upgrading packages...")
    run_command("sudo apt update && sudo apt upgrade -y")

    # Install pip and htop
    print("Installing pip and htop...")
    run_command("sudo apt install python3-pip htop -y")

    # Install Python 12 (using deadsnakes PPA)
    print("Installing Python 12...")
    run_command("sudo add-apt-repository ppa:deadsnakes/ppa -y")
    run_command("sudo apt update")
    run_command("sudo apt install python3.12 -y")

    # Remove Python 3.9
    print("Removing Python 3.9...")
    run_command("sudo apt remove python3.9 -y")
    run_command("sudo apt autoremove -y")

    # Install VS Code
    print("Installing VS Code...")
    run_command("sudo apt install software-properties-common apt-transport-https wget -y")
    run_command("wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -")
    run_command("sudo add-apt-repository \"deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main\"")
    run_command("sudo apt update")
    run_command("sudo apt install code -y")

    # Install grub-customizer
    print("Installing grub-customizer...")
    run_command("sudo add-apt-repository ppa:danielrichter2007/grub-customizer -y")
    run_command("sudo apt update")
    run_command("sudo apt install grub-customizer -y")

    # Configure keyboard layout switching
    print("Configuring keyboard layout switching...")
    run_command("gsettings set org.gnome.desktop.input-sources sources \"[('xkb', 'us'), ('xkb', 'ru')]\"")
    run_command("gsettings set org.gnome.desktop.input-sources xkb-options \"['grp:ctrl_shift_toggle']\"")

    # Install Stacer
    print("Installing Stacer...")
    run_command("sudo apt update")
    run_command("sudo apt install stacer -y")

    # Install Ulauncher
    print("Installing Ulauncher...")
    run_command("sudo add-apt-repository ppa:agornostal/ulauncher -y")
    run_command("sudo apt update")
    run_command("sudo apt install ulauncher -y")

    # Install Wine
    print("Installing Wine...")
    run_command("sudo dpkg --add-architecture i386")
    run_command("sudo apt update")
    run_command("sudo apt install wine64 wine32 -y")

    print("\nSetup completed! Please restart your system for all changes to take effect.")

if __name__ == "__main__":
    main()