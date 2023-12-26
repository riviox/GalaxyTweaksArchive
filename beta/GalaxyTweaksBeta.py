import os
import requests
import ctypes
import sys
import subprocess
from colorama import Fore, init
import eel
import json

init(autoreset=True)
local = "3.8.2 BETA"

print(Fore.GREEN + "Loading...")
print(Fore.YELLOW + "This is GalaxyTweaks Output, do not close it!")

def get_html_from_github(file_url):
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

embedded_menu_html = get_html_from_github("https://raw.githubusercontent.com/RivioxGaming/GalaxyFPS/main/beta/gui/menu.html")

if not embedded_menu_html:
    print("Error: Failed to fetch HTML content from GitHub.")
    print("Exiting...")
username = os.getenv("username")
menu_folder = f"C:\\GalaxyTweaks"
menu = os.path.join(menu_folder, "menu.html")

if not os.path.exists(menu_folder):
    os.makedirs(menu_folder)

with open(menu, 'w', encoding='utf-8') as html_file:
    html_file.write(embedded_menu_html)

if not embedded_menu_html:
    print("Error: Failed to fetch HTML content from GitHub.")
    print("Exiting...")
    exit()

def run_as_admin():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            return

        script = os.path.abspath(sys.argv[0])
        params = ' '.join(sys.argv[1:])
        subprocess.run(['powershell', f'Start-Process -Verb RunAs "{sys.executable}" -ArgumentList "{script} {params}"'])
        sys.exit()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit()
run_as_admin()

temp_folder = os.environ['TEMP']
temp_version_file = os.path.join(temp_folder, "bgversion.txt")
versionurl = "https://raw.githubusercontent.com/RivioxGaming/GalaxyFPS/main/beta/version"

if os.path.exists(temp_version_file):
    os.remove(temp_version_file)

response = requests.get(versionurl)
if response.status_code == 200:
    with open(temp_version_file, 'wb') as file:
        file.write(response.content)

@eel.expose
def check_for_update():
    update_url = "https://raw.githubusercontent.com/RivioxGaming/GalaxyFPS/main/beta/GalaxyTweaksBeta.py"
    response = requests.get(update_url)

    if response.status_code == 200:
        new_version = local
        script_lines = response.text.splitlines()
        for line in script_lines:
            if line.startswith('local ='):
                new_version = line.split('=')[1].strip().replace('"', '')
                break

        if local != new_version:
            print(f"Your Version: {local}")
            print(f"New version: {new_version}")
            print("Note: You don't have to install pre-releases.")
            choice = input("Do you want to update? (y/n): ")
            if choice.lower() == 'y':
                with open(__file__, 'wb') as file:
                    file.write(response.content)

                menu_html_url = "https://raw.githubusercontent.com/RivioxGaming/GalaxyFPS/main/beta/gui/menu.html"
                menu_html_response = requests.get(menu_html_url)
                
                if menu_html_response.status_code == 200:
                    menu_html_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gui", "menu.html")
                    with open(menu_html_file_path, 'wb') as menu_html_file:
                        menu_html_file.write(menu_html_response.content)

                python = sys.executable
                os.execl(python, python, *sys.argv)
                exit()

@eel.expose
def perform_update():
    update_url = "https://raw.githubusercontent.com/RivioxGaming/GalaxyFPS/main/beta/GalaxyTweaksBeta.py"
    response = requests.get(update_url)

    if response.status_code == 200:
        with open(__file__, 'wb') as file:
            file.write(response.content)

        python = sys.executable
        os.execl(python, python, *sys.argv)
        exit()
        
@eel.expose
def mtw():
    print(Fore.YELLOW + "Applying Main Tweaks...")
    os.system(r'''
    Reg.exe add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v "SystemPages" /t REG_SZ /d "0" /f
    Reg.exe add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v "PoolUsageMaximum" /t REG_SZ /d "00000060" /f
    Reg.exe add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\GameDVR" /v "AppCaptureEnabled" /t REG_SZ /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "DisableExceptionChainValidation" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "DpcWatchdogProfileOffset" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "DpcWatchdogPeriod" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "KernelSEHOPEnabled" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "SerializeTimerExpiration" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "InterruptSteeringDisabled" /t REG_DWORD /d "1" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\SettingSync" /v "SyncPolicy" /t REG_DWORD /d "5" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\SettingSync\Groups\BrowserSettings" /v "Enabled" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\SettingSync\Groups\Credentials" /v "Enabled" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\SettingSync\Groups\Accessibility" /v "Enabled" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\SettingSync\Groups\Windows" /v "Enabled" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v "EnableTransparency" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers" /v "HwSchMode" /t REG_DWORD /d "2" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\DirectX\UserGpuPreferences" /v "DirectXUserGlobalSettings" /t REG_SZ /d "VRROptimizeEnable=0;" /f
    Reg.exe add "HKCU\Control Panel\Accessibility\MouseKeys" /v "Flags" /t REG_SZ /d "0" /f
    Reg.exe add "HKCU\Control Panel\Accessibility\StickyKeys" /v "Flags" /t REG_SZ /d "0" /f
    Reg.exe add "HKCU\Control Panel\Accessibility\Keyboard Response" /v "Flags" /t REG_SZ /d "0" /f
    Reg.exe add "HKCU\Control Panel\Accessibility\ToggleKeys" /v "Flags" /t REG_SZ /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo" /v "Enabled" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\Control Panel\International\User Profile" /v "HttpAcceptLanguageOptOut" /t REG_DWORD /d "1" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "Start_TrackProgs" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "SubscribedContent-338393Enabled" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "SubscribedContent-353696Enabled" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Speech_OneCore\Settings\OnlineSpeechPrivacy" /v "HasAccepted" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Personalization\Settings" /v "AcceptedPrivacyPolicy" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\InputPersonalization" /v "RestrictImplicitInkCollection" /t REG_DWORD /d "1" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\InputPersonalization" /v "RestrictImplicitTextCollection" /t REG_DWORD /d "1" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\InputPersonalization\TrainedDataStore" /v "HarvestContacts" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Diagnostics\DiagTrack" /v "ShowedToastAtLevel" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v "AllowTelemetry" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Privacy" /v "TailoredExperiencesWithDiagnosticDataEnabled" /t REG_DWORD /d "0" /f
    Reg.exe add "Powercfg" -h off
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Siuf\Rules" /v "NumberOfSIUFInPeriod" /t REG_DWORD /d "0" /f
    Reg.exe delete "HKCU\SOFTWARE\Microsoft\Siuf\Rules" /v "PeriodInNanoSeconds" /f
    Reg.exe add "HKLM\SOFTWARE\Policies\Microsoft\Windows\System" /v "PublishUserActivities" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SOFTWARE\Policies\Microsoft\Windows\System" /v "UploadUserActivities" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\userNotificationListener" /v "Value" /t REG_SZ /d "Deny" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location" /v "Value" /t REG_SZ /d "Deny" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\appDiagnostics" /v "Value" /t REG_SZ /d "Deny" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\userAccountInformation" /v "Value" /t REG_SZ /d "Deny" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications" /v "GlobalUserDisabled" /t REG_DWORD /d "1" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Search" /v "BackgroundAppGlobalToggle" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\Control Panel\Desktop\WindowMetrics" /v "MinAnimate" /t REG_SZ /d "0" /f
    Reg.exe add "HKCU\Control Panel\Desktop\WindowMetrics" /v "MaxAnimate" /t REG_SZ /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "ExtendedUIHoverTime" /t REG_DWORD /d "196608" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "DontPrettyPath" /t REG_DWORD /d "1" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "ListviewShadow" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "TaskbarAnimations" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\Software\Microsoft\Windows\DWM" /v "EnableAeroPeek" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DWM" /v "DWMWA_TRANSITIONS_FORCEDISABLED" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DWM" /v "DisallowAnimations" /t REG_DWORD /d "1" /f
    Reg.exe add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v "NoLowDiskSpaceChecks" /t REG_DWORD /d "1" /f
    Reg.exe add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v "LinkResolveIgnoreLinkInfo" /t REG_DWORD /d "1" /f
    Reg.exe add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v "NoResolveSearch" /t REG_DWORD /d "1" /f
    Reg.exe add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v "NoResolveTrack" /t REG_DWORD /d "1" /f
    Reg.exe add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v "NoInternetOpenWith" /t REG_DWORD /d "1" /f
    Reg.exe add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v "NoInstrumentation" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\EnergyEstimation\TaggedEnergy" /v "EnergyEstimationEnabled" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\Control Panel\Desktop" /v "FontSmoothing" /t REG_SZ /d "2" /f
    Reg.exe add "HKCU\Control Panel\Desktop" /v "FontSmoothingType" /t REG_DWORD /d "2" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MultitaskingView\AllUpView" /v "AllUpView" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MultitaskingView\AllUpView" /v "Remove TaskView" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl" /v "ConvertibleSlateMode" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl" /v "Win32PrioritySeparation" /t REG_DWORD /d "38" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Services\usbxhci\Parameters" /v "ThreadPriority" /t REG_DWORD /d "31" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Services\USBHUB3\Parameters" /v "ThreadPriority" /t REG_DWORD /d "31" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Services\nvlddmkm\Parameters" /v "ThreadPriority" /t REG_DWORD /d "31" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Services\NDIS\Parameters" /v "ThreadPriority" /t REG_DWORD /d "31" /f
    Reg.exe add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "DisallowShaking" /t REG_DWORD /d "1" /f
    Reg.exe add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "EnableBalloonTips" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Serialize" /v "StartupDelayInMSec" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Policies\Microsoft\Windows\CurrentVersion\PushNotifications" /v "NoTileApplicationNotification" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v "AllowTelemetry" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v "AllowDeviceNameInTelemetry" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "Affinity" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "Background Only" /t REG_SZ /d "False" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "Clock Rate" /t REG_DWORD /d "10000" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "GPU Priority" /t REG_DWORD /d "8" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "Priority" /t REG_DWORD /d "6" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "Scheduling Category" /t REG_SZ /d "High" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "SFIO Priority" /t REG_SZ /d "High" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "BackgroundPriority" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "Latency Sensitive" /t REG_SZ /d "True" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Power" /v "CoalescingTimerInterval" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\\54533251-82be-4824-96c1-47b60b740d00\\75b0ae3f-bce0-45a7-8c89-c9611c25e100" /v "Attributes" /t REG_DWORD /d "2" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\\54533251-82be-4824-96c1-47b60b740d00\\75b0ae3f-bce0-45a7-8c89-c9611c25e100" /v "Affinity" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\\54533251-82be-4824-96c1-47b60b740d00\\75b0ae3f-bce0-45a7-8c89-c9611c25e100" /v "Background Only" /t REG_SZ /d "False" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\\54533251-82be-4824-96c1-47b60b740d00\\75b0ae3f-bce0-45a7-8c89-c9611c25e100" /v "Clock Rate" /t REG_DWORD /d "10000" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\\54533251-82be-4824-96c1-47b60b740d00\\75b0ae3f-bce0-45a7-8c89-c9611c25e100" /v "GPU Priority" /t REG_DWORD /d "8" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\\54533251-82be-4824-96c1-47b60b740d00\\75b0ae3f-bce0-45a7-8c89-c9611c25e100" /v "Priority" /t REG_DWORD /d "6" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\\54533251-82be-4824-96c1-47b60b740d00\\75b0ae3f-bce0-45a7-8c89-c9611c25e100" /v "Scheduling Category" /t REG_SZ /d "High" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\\54533251-82be-4824-96c1-47b60b740d00\\75b0ae3f-bce0-45a7-8c89-c9611c25e100" /v "SFIO Priority" /t REG_SZ /d "High" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\\54533251-82be-4824-96c1-47b60b740d00\\75b0ae3f-bce0-45a7-8c89-c9611c25e100" /v "BackgroundPriority" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\\54533251-82be-4824-96c1-47b60b740d00\\75b0ae3f-bce0-45a7-8c89-c9611c25e100" /v "Latency Sensitive" /t REG_SZ /d "True" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\EnergyEstimation\TaggedEnergy" /v "DisableTaggedEnergyLogging" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\EnergyEstimation\TaggedEnergy" /v "TelemetryMaxApplication" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\EnergyEstimation\TaggedEnergy" /v "TelemetryMaxTagPerApplication" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Processor" /v "Cstates" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Processor" /v "Capabilities" /t REG_DWORD /d "516198" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v "HighPerformance" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v "HighestPerformance" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v "MinimumThrottlePercent" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v "MaximumThrottlePercent" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v "MaximumPerformancePercent" /t REG_DWORD /d "100" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v "Class1InitialUnparkCount" /t REG_DWORD /d "100" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v "InitialUnparkCount" /t REG_DWORD /d "100" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v "MaximumPerformancePercent" /t REG_DWORD /d "100" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerThrottling" /v "PowerThrottlingOff" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WcmSvc\GroupPolicy" /v "fDisablePowerManagement" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\PDC\Activators\Default\VetoPolicy" /v "EA:EnergySaverEngaged" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\PDC\Activators\28\VetoPolicy" /v "EA:PowerStateDischarging" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\Policy\Settings\Misc" /v "DeviceIdlePolicy" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\Policy\Settings\Processor" /v "PerfEnergyPreference" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\Policy\Settings\Processor" /v "PerfEnergyPreference" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\Policy\Settings\Processor" /v "CPMinCores" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\Policy\Settings\Processor" /v "CPMaxCores" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\Policy\Settings\Processor" /v "CPMinCores1" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\Policy\Settings\Processor" /v "CPMaxCores1" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\Policy\Settings\Processor" /v "CpLatencyHintUnpark1" /t REG_DWORD /d "100" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\Policy\Settings\Processor" /v "CPDistribution" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\Policy\Settings\Processor" /v "CpLatencyHintUnpark" /t REG_DWORD /d "100" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\Policy\Settings\Processor" /v "MaxPerformance1" /t REG_DWORD /d "100" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\Policy\Settings\Processor" /v "MaxPerformance" /t REG_DWORD /d "100" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\Policy\Settings\Processor" /v "CPDistribution1" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\Policy\Settings\Processor" /v "CPHEADROOM" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\Policy\Settings\Processor" /v "CPCONCUR
    Reg.exe add "HKCU\Control Panel\PowerCfg\GlobalPowerPolicy" /v "Policies" /t REG_BINARY /d "01000000020000000100000000000000020000000000000000000000000000002c0100003232030304000000040000000000000000000000840300002c01000000000000840300000001646464640000" /f
    Reg.exe add "HKCU\Control Panel\PowerCfg\GlobalPowerPolicy" /v "Policies" /t REG_BINARY /d "01000000020000000100000000000000020000000000000000000000000000002c0100003232030304000000040000000000000000000000840300002c01000000000000840300000001646464640000" /f
    Reg.exe add "HKCU\Control Panel\Desktop" /v "AutoEndTasks" /t REG_SZ /d "1" /f
    Reg.exe add "HKCU\Control Panel\Desktop" /v "HungAppTimeout" /t REG_SZ /d "1000" /f
    Reg.exe add "HKCU\Control Panel\Desktop" /v "WaitToKillAppTimeout" /t REG_SZ /d "2000" /f
    Reg.exe add "HKCU\Control Panel\Desktop" /v "LowLevelHooksTimeout" /t REG_SZ /d "1000" /f  
    Reg.exe add "HKCU\Control Panel\Desktop" /v "MenuShowDelay" /t REG_SZ /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control" /v "WaitToKillServiceTimeout" /t REG_SZ /d "2000" /f
    taskkill /f /im explorer.exe
    start explorer.exe
    ''')
    print(Fore.GREEN + "Applied Main Tweaks!")

@eel.expose
def getTweaksList():
    tweaks_list_url = "https://raw.githubusercontent.com/RivioxGaming/GalaxyFPS/main/tweaks/tweaks.json"
    tweaks_folder = 'https://raw.githubusercontent.com/RivioxGaming/GalaxyFPS/main/tweaks'
    tweaks_list = []
    try:
        response = requests.get(tweaks_list_url)
        response.raise_for_status()
        tweaks_list = response.json()
    except requests.RequestException as e:
        print(f"Error fetching tweaks list: {e}")
        tweaks_list = []

    except Exception as e:
        print(f"Error fetching tweaks list: {e}")

        return tweaks_list

@eel.expose
def runTweak(url):
    parsed_url = urlparse(url)

    if parsed_url.scheme:
        os.system(f'start {url}')
    else:
        print(f"Invalid URL: {url}")


@eel.expose
def netw():
    print(Fore.YELLOW + "Applying Internet Tweaks!")
    os.system('ipconfig /flushdns')
    os.system('ipconfig /registerdns')
    os.system('ipconfig /release')
    os.system('ipconfig /renew')
    os.system('netsh winsock reset')
    print(Fore.GREEN + "Applied Internet Tweaks!")
    pass
    
@eel.expose
def cleaner():
    print(Fore.YELLOW + "Cleaning Temp Files...")
    os.system('cls')
    print("Cleaning temporary files...")
    os.system('timeout 3 >nul')
    os.system(f'del /s /f /q {os.environ["SYSTEMDRIVE"]}\\windows\\temp\\*.*')
    os.system(f'rd /s /q {os.environ["SYSTEMDRIVE"]}\\windows\\temp')
    os.system('md c:\\windows\\temp')
    os.system(f'del /s /f /q {os.environ["SYSTEMDRIVE"]}\\WINDOWS\\Prefetch')
    os.system(f'del /s /f /q {os.environ["temp"]}\\*.*')
    os.system(f'rd /s /q {os.environ["temp"]}')
    os.system('cls')
    print("Successful deleted temporary files!")
    os.system('timeout 1 >nul')
    os.system('cls')
    os.system('timeout 3 >nul')
    print("Cleaning logs...")
    os.system('md %temp%')
    os.system(f'del /q /f /s {os.environ["SYSTEMDRIVE"]}\\Temp\\*.*')
    os.system(f'del /q /f /s {os.environ["WINDIR"]}\\Prefetch\\*.*')
    os.system(f'del /q /f /s {os.environ["SYSTEMDRIVE"]}\\*.log')
    os.system(f'del /q /f /s {os.environ["SYSTEMDRIVE"]}\\*.bak')
    os.system(f'del /q /f /s {os.environ["SYSTEMDRIVE"]}\\*.gid')
    os.system('cls')
    print("Successful cleaned logs!")
    os.system('timeout 2 >nul')
    print("Returning to menu...")
    os.system('timeout 3 >nul')
    print(Fore.GREEN + "Cleaned Temp files!")
    pass
    
@eel.expose
def ocmd():
    print(Fore.YELLOW + "Starting CMD.exe...")
    os.system("start")
    print(Fore.GREEN + "Started CMD.exe!")
    
@eel.expose
def adwt():
    print(Fore.YELLOW + "Applying Advanced Tweaks..")
    print(Fore.BLUE + "Downloading [advtweaks.reg]")
    reg_file_url = "https://raw.githubusercontent.com/RivioxGaming/GalaxyFPS/main/regs/advtweaks.reg"
    reg_file_name = "%temp%\\advtweaks.reg"

    response = requests.get(reg_file_url)
    if response.status_code == 200:
        with open(reg_file_name, 'wb') as reg_file:
            reg_file.write(response.content)

        if os.path.exists(reg_file_name):
            print(Fore.YELLOW + "Running advtweaks.reg")
            subprocess.run(["regedit", "/s", reg_file_name])
            print(Fore.GREEN + "Applied Advanced Tweaks!")
        else:
            pass
    
@eel.expose
def regbckp():
    print(Fore.YELLOW + "Making registry backup...")
    os.system('regedit.exe /e "C:\GalaxyFPSregbckp.reg"')
    print(Fore.GREEN + "Registry backup is at `C:\\regbckp.reg`!")
        
@eel.expose
def dwmt():
    print(Fore.YELLOW + "Applying DWM Tweaks...")
    os.system(r"""
    Reg.exe add "HKCU\Control Panel\Desktop\WindowMetrics" /v "MinAnimate" /t REG_SZ /d "0" /f
    Reg.exe add "HKCU\Control Panel\Desktop\WindowMetrics" /v "MaxAnimate" /t REG_SZ /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "ExtendedUIHoverTime" /t REG_DWORD /d "196608" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "DontPrettyPath" /t REG_DWORD /d "1" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "ListviewShadow" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "TaskbarAnimations" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\Software\Microsoft\Windows\DWM" /v "EnableAeroPeek" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DWM" /v "DWMWA_TRANSITIONS_FORCEDISABLED" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DWM" /v "DisallowAnimations" /t REG_DWORD /d "1" /f
    Reg.exe add "HKCR\Paint.Picture\DefaultIcon" /ve /t REG_SZ /d "%%1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\EnergyEstimation\TaggedEnergy" /v "DisableTaggedEnergyLogging" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\EnergyEstimation\TaggedEnergy" /v "TelemetryMaxApplication" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\EnergyEstimation\TaggedEnergy" /v "TelemetryMaxTagPerApplication" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Power\EnergyEstimation\TaggedEnergy" /v "EnergyEstimationEnabled" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\Control Panel\Desktop" /v "FontSmoothing" /t REG_SZ /d "2" /f
    Reg.exe add "HKCU\Control Panel\Desktop" /v "FontSmoothingType" /t REG_DWORD /d "2" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MultitaskingView\AllUpView" /v "AllUpView" /t REG_DWORD /d "0" /f
    Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MultitaskingView\AllUpView" /v "Remove TaskView" /t REG_DWORD /d "1" /f
    Reg.exe add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer" /v "AltTabSettings" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Kernel" /v "DisableExceptionChainValidation" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Kernel" /v "KernelSEHOPEnabled" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Kernel" /v "UseNormalStack" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Kernel" /v "UseNewEaBuffering" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Kernel" /v "StackSubSystemStackSize" /t REG_DWORD /d "65536" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Kernel" /v "SystemResponsivenessReserved" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "EnableUserModeCache" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "EnableLowLatencyIo" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "EnableFsCacheHost" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "DisableSystemPTEWriteBack" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "KernelStackSize" /t REG_DWORD /d "8192" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "PfnMaxLookahead" /t REG_DWORD /d "16" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "LatencyMode" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "EnableLowMemoryKiller" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "CpuRelaxedSpeculation" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "DisableDynamicTick" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "DynamicTick" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "EnergyDriverPolicy" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "EnergyDriverPolicyVideo" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "TimerBResolution" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "TimerMinResolution" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "TimerReliability" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "KernelIoPriority" /t REG_DWORD /d "3" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "DisableLowQosTimerResolution" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "SerializeTimerExpiration" /t REG_DWORD /d "2" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "TimerCheckFlags" /t REG_DWORD /d "8" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "SplitLargeCaches" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "SchedulerAssistThreadFlagOverride" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "GlobalTimerResolutionRequests" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "EnablePerCpuClockTickScheduling" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "CacheErrataOverride" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "CacheAwareScheduling" /t REG_DWORD /d "5" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "ForceApicPhysicalDestinationMode" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "TscInvariant" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "ForceClockSync" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "TscSyncPolicy" /t REG_DWORD /d "2" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "TscAdjustDisable" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "ContextNoPatchMode" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "DisableTsx" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "DisableLowQosTimerResolution" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "KernelSEHOPEnabled" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "CoalescingTimerInterval" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "DebugPollInterval" /t REG_DWORD /d "1000" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "RebalanceMinPriority" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "MaxDynamicTickDuration" /t REG_DWORD /d "10" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "MaximumDpcQueueDepth" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "MaximumDpcRate" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "MaximumSharedReadyQueueSize" /t REG_DWORD /d "128" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "BufferSize" /t REG_DWORD /d "32" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "IoQueueWorkItem" /t REG_DWORD /d "32" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "IoQueueWorkItemToNode" /t REG_DWORD /d "32" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "IoQueueWorkItemEx" /t REG_DWORD /d "32" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "IoQueueThreadIrp" /t REG_DWORD /d "32" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "ExTryQueueWorkItem" /t REG_DWORD /d "32" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "ExQueueWorkItem" /t REG_DWORD /d "32" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "IoEnqueueIrp" /t REG_DWORD /d "32" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "DisableVsyncLatencyUpdate" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "ExitLatencyCheckEnabled" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "LatencyToleranceVSyncEnabled" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "DisableLowQosTimerResolution" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "XMMIZeroingEnable" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "EnableDWMShaderIntercept" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "AllowFlipInModal" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "DwmTearingPolicy" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "MsaaQualityMode" /t REG_DWORD /d "3" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "DwmMaxQueuedBuffers" /t REG_DWORD /d "6" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "MaxD3D9BatchSize" /t REG_DWORD /d "4132" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "UseDDIForRendering" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "UseOcclusion" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "DisallowMouseDirectionOptin" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "ForceDirectDrawSuppression" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "DwmIommuEnabled" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "ForceVBlankFlipEx" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "DWMUseAlternateSolutionForRefreshIncrements" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "DWMUseGPUForWindowAnimations" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "UseDesktopDuplicationAPIs" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "DWMInputBoosted" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "ParallelModePolicy" /t REG_DWORD /d "2" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "ImageProcessing8bit" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "InteractionOutputPredictionDisabled" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "EnableImageProcessing" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "EnableFrontBufferRenderChecks" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "ResampleModeOverride" /t REG_DWORD /d "2" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "ResampleInLinearSpace" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "OverlayTestMode" /t REG_DWORD /d "5" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "DwmPresentationInterval" /t REG_DWORD /d "2" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "CompositionPolicy" /t REG_DWORD /d "0" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "UseDefaultComposition" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm" /v "UseHWInput" /t REG_DWORD /d "1" /f
    Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\Dwm\ExtendedComposition" /v "ExclusiveModeFramerateThresholdPercent" /t REG_DWORD /d "250" /f
    """)
    print(Fore.GREEN + "Applied DWM Tweaks!")
    pass

@eel.expose
def discord():
    os.system("start https://discord.gg/fpJxa2Gfa3")

if __name__ == '__main__':
    check_for_update()
    rp = os.path.abspath(menu.strip("menu.html"))
    eel.root_path = rp
    eel.init(rp)
    eel.start('menu.html', size=(600, 400))
