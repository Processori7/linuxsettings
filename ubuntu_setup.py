#!/usr/bin/env python3
import os
import subprocess

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Successfully executed: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e}")

def cleanup_ppa():
    print("Cleaning up unreachable PPA repositories and those without Release files...")
    # Get list of PPA repositories and check their availability
    run_command("""
        for f in /etc/apt/sources.list.d/*.list; do
            grep -o '^deb http://ppa.launchpad.net/[a-z0-9\-]\+/[a-z0-9\-]\+' "$f" | while read ENTRY; do
                PPA=${ENTRY#deb http://ppa.launchpad.net/}
                HOST="ppa.launchpad.net"
                if ! ping -c 1 "$HOST" >/dev/null 2>&1 || \
                   ! curl --output /dev/null --silent --head --fail "http://$HOST/$PPA/ubuntu/dists/$(lsb_release -cs)/Release"; then
                    echo "Removing unreachable PPA: $PPA"
                    sudo add-apt-repository -r "ppa:$PPA" -y
                fi
            done
        done
    """)

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
    run_command("wget -O code.deb 'https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64'")
    run_command("sudo apt install ./code.deb -y")
    run_command("rm code.deb")

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

    # Clean up PPA repositories without Release files
    cleanup_ppa()

    print("\nSetup completed! Please restart your system for all changes to take effect.")

if __name__ == "__main__":
    main()