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
    # First, get a list of all PPA files
    try:
        ppa_files = subprocess.run(["find", "/etc/apt/sources.list.d/", "-name", "*.list"], 
                                 capture_output=True, text=True, check=True)
        
        for ppa_file in ppa_files.stdout.splitlines():
            try:
                # Extract PPA URLs from the file
                grep_result = subprocess.run(["grep", "-o", "^deb http://ppa.launchpad.net/[a-z0-9-]\+/[a-z0-9-]\+", ppa_file],
                                           capture_output=True, text=True)
                
                for line in grep_result.stdout.splitlines():
                    # Extract PPA name
                    ppa = line.replace("deb http://ppa.launchpad.net/", "").strip()
                    if ppa:
                        # Check if PPA is reachable
                        try:
                            # Try to fetch the Release file
                            release_url = f"http://ppa.launchpad.net/{ppa}/ubuntu/dists/$(lsb_release -cs)/Release"
                            curl_result = subprocess.run(["curl", "--output", "/dev/null", "--silent", "--head", "--fail", release_url],
                                                       capture_output=True)
                            
                            if curl_result.returncode != 0:
                                print(f"PPA {ppa} is unreachable or has no Release file")
                                run_command(f"sudo add-apt-repository -r 'ppa:{ppa}' -y")
                        except subprocess.CalledProcessError:
                            print(f"Failed to check PPA: {ppa}")
            except subprocess.CalledProcessError:
                continue
    except subprocess.CalledProcessError as e:
        print(f"Error while cleaning up PPAs: {e}")

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
    print("\nChecking keyboard layout configuration...")
    desktop_env = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
    
    def print_current_settings():
        print("Current keyboard layout settings:")
        if 'gnome' in desktop_env:
            try:
                sources = subprocess.run(["gsettings", "get", "org.gnome.desktop.input-sources", "sources"], 
                                        capture_output=True, text=True).stdout.strip()
                options = subprocess.run(["gsettings", "get", "org.gnome.desktop.input-sources", "xkb-options"], 
                                        capture_output=True, text=True).stdout.strip()
                print(f"Layout sources: {sources}")
                print(f"Keyboard options: {options}")
            except Exception as e:
                print(f"Error reading GNOME settings: {e}")
        elif 'lxqt' in desktop_env:
            try:
                current_layout = subprocess.run(["setxkbmap", "-query"], capture_output=True, text=True).stdout
                print(current_layout)
            except Exception as e:
                print(f"Error reading LXQT settings: {e}")
    
    print_current_settings()
    print("\nConfiguring keyboard layout switching...")
    
    if 'gnome' in desktop_env:
        # GNOME desktop environment (Ubuntu)
        current_sources = subprocess.run(["gsettings", "get", "org.gnome.desktop.input-sources", "sources"], 
                                       capture_output=True, text=True).stdout.strip()
        current_options = subprocess.run(["gsettings", "get", "org.gnome.desktop.input-sources", "xkb-options"], 
                                       capture_output=True, text=True).stdout.strip()
        
        if "[('xkb', 'us'), ('xkb', 'ru')]" not in current_sources:
            run_command("gsettings set org.gnome.desktop.input-sources sources \"[('xkb', 'us'), ('xkb', 'ru')]\"")
            print("Updated keyboard layouts to US and RU")
        
        if "['grp:ctrl_shift_toggle']" not in current_options:
            run_command("gsettings set org.gnome.desktop.input-sources xkb-options \"['grp:ctrl_shift_toggle']\"")
            print("Updated keyboard switch shortcut to Ctrl+Shift")
        
        print("\nVerifying new settings:")
        print_current_settings()
        
    elif 'lxqt' in desktop_env:
        # LXQT desktop environment (Lubuntu)
        xkb_config_file = "/etc/X11/xorg.conf.d/00-keyboard.conf"
        xkb_config = """\
Section "InputClass"
        Identifier "system-keyboard"
        MatchIsKeyboard "on"
        Option "XkbLayout" "us,ru"
        Option "XkbModel" "pc105"
        Option "XkbOptions" "grp:ctrl_shift_toggle"
EndSection
"""
        
        # Check if config directory exists, create if not
        if not os.path.exists("/etc/X11/xorg.conf.d"):
            run_command("sudo mkdir -p /etc/X11/xorg.conf.d")
        
        # Check current keyboard settings
        current_settings = subprocess.run(["setxkbmap", "-query"], capture_output=True, text=True).stdout
        needs_update = False
        
        if "layout:     us,ru" not in current_settings or "option:     grp:ctrl_shift_toggle" not in current_settings:
            needs_update = True
        
        # Check if config file exists and has correct settings
        if os.path.exists(xkb_config_file):
            try:
                with open(xkb_config_file, 'r') as f:
                    current_config = f.read()
                    if 'XkbLayout "us,ru"' not in current_config or 'XkbOptions "grp:ctrl_shift_toggle"' not in current_config:
                        needs_update = True
            except Exception as e:
                print(f"Error reading keyboard config: {e}")
                needs_update = True
        else:
            needs_update = True
        
        if needs_update:
            print("Updating keyboard layout configuration...")
            # Create X11 config file
            run_command(f"echo '{xkb_config}' | sudo tee {xkb_config_file} > /dev/null")
            
            # Apply settings immediately
            run_command("setxkbmap -layout 'us,ru' -option 'grp:ctrl_shift_toggle'")
            
            # Update LXQT-specific settings
            run_command("mkdir -p ~/.config/lxqt")
            lxqt_config = """[Keyboard]
            model=pc105
            layout=us,ru
            variant=,
            option=grp:ctrl_shift_toggle
            """
            run_command(f"echo '{lxqt_config}' > ~/.config/lxqt/keyboard.conf")
            
            # Restart keyboard settings
            run_command("setxkbmap -layout 'us,ru' -option 'grp:ctrl_shift_toggle'")
            run_command("lxqt-config-input --reload")
            
            print("\nVerifying new settings:")
            print_current_settings()
        else:
            print("Keyboard layout configuration is correct and up to date")
    else:
        print("Unsupported desktop environment for automatic keyboard layout configuration")

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

    # Uninstall FireFox
    run_command("sudo apt purge firefox -y")
    run_command("sudo apt autoremove -y")

    # Install LibreWolf
    run_command("sudo apt install extrepo -y")
    run_command("sudo extrepo enable librewolf")
    run_command("sudo apt update && sudo apt install librewolf -y")

    # Clean up PPA repositories without Release files
    cleanup_ppa()

    print("\nSetup completed! Please restart your system for all changes to take effect.")

if __name__ == "__main__":
    main()