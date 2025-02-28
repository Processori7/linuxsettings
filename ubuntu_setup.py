#!/usr/bin/env python3
import os
import subprocess

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Successfully executed: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e}")

def check_package_installed(package_name):
    try:
        result = subprocess.run(["dpkg", "-l", package_name], capture_output=True, text=True)
        return "ii" in result.stdout
    except subprocess.CalledProcessError:
        return False

def check_ppa_exists(ppa_name):
    try:
        result = subprocess.run(["grep", "-r", f"^deb.*{ppa_name}", "/etc/apt/sources.list.d/"], capture_output=True, text=True)
        return bool(result.stdout.strip())
    except subprocess.CalledProcessError:
        return False

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
    print("Checking and installing pip and htop...")
    if not check_package_installed("python3-pip"):
        run_command("sudo apt install python3-pip -y")
    else:
        print("python3-pip is already installed")

    if not check_package_installed("htop"):
        run_command("sudo apt install htop -y")
    else:
        print("htop is already installed")

    # Install Python 12 (using deadsnakes PPA)
    print("Checking and installing Python 12...")
    if not check_ppa_exists("deadsnakes"):
        run_command("sudo add-apt-repository ppa:deadsnakes/ppa -y")
        run_command("sudo apt update")
    else:
        print("deadsnakes PPA is already added")

    if not check_package_installed("python3.12"):
        run_command("sudo apt install python3.12 -y")
    else:
        print("Python 3.12 is already installed")

    # Remove Python 3.9 if installed
    print("Checking and removing Python 3.9...")
    if check_package_installed("python3.9"):
        run_command("sudo apt remove python3.9 -y")
        run_command("sudo apt autoremove -y")
    else:
        print("Python 3.9 is not installed")

    # Install VS Code
    print("Checking and installing VS Code...")
    if not check_package_installed("code"):
        run_command("wget -O code.deb 'https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64'")
        run_command("sudo apt install ./code.deb -y")
        run_command("rm code.deb")
    else:
        print("VS Code is already installed")

    # Install grub-customizer
    print("Checking and installing grub-customizer...")
    if not check_package_installed("grub-customizer"):
        if not check_ppa_exists("danielrichter2007/grub-customizer"):
            run_command("sudo add-apt-repository ppa:danielrichter2007/grub-customizer -y")
            run_command("sudo apt update")
        run_command("sudo apt install grub-customizer -y")
    else:
        print("grub-customizer is already installed")

    # Configure keyboard layout switching
    print("Configuring keyboard layout switching...")
    run_command("gsettings set org.gnome.desktop.input-sources sources \"[('xkb', 'us'), ('xkb', 'ru')]\"")
    run_command("gsettings set org.gnome.desktop.input-sources xkb-options \"['grp:ctrl_shift_toggle']\"")

    # Install Stacer
    print("Checking and installing Stacer...")
    if not check_package_installed("stacer"):
        run_command("sudo apt update")
        run_command("sudo apt install stacer -y")
    else:
        print("Stacer is already installed")

    # Install Ulauncher
    print("Checking and installing Ulauncher...")
    if not check_package_installed("ulauncher"):
        if not check_ppa_exists("agornostal/ulauncher"):
            run_command("sudo add-apt-repository ppa:agornostal/ulauncher -y")
            run_command("sudo apt update")
        run_command("sudo apt install ulauncher -y")
    else:
        print("Ulauncher is already installed")

    # Install Wine
    print("Checking and installing Wine...")
    if not (check_package_installed("wine64") and check_package_installed("wine32")):
        run_command("sudo dpkg --add-architecture i386")
        run_command("sudo apt update")
        run_command("sudo apt install wine64 wine32 -y")
    else:
        print("Wine is already installed")

    # Clean up PPA repositories without Release files
    cleanup_ppa()

    print("\nSetup completed! Please restart your system for all changes to take effect.")

if __name__ == "__main__":
    main()