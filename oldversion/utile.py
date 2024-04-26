import os
import subprocess
import platform



def find_spotify_path():
    os_type = platform.system()
    if os_type == "Windows":
        # the default path for spotify
        path = os.path.expanduser("~\\AppData\\Roaming\\Spotify\\Spotify.exe")
        if os.path.exists(path):
            return path
        # if not exit,try looking for the register to find the path
        try:
            reg_path = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Spotify"
            reg_query = subprocess.check_output(['reg', 'query', 'HKCU\\' + reg_path, '/v', 'InstallLocation'],
                                                encoding='utf-16')
            for line in reg_query.splitlines():
                if "InstallLocation" in line:
                    return line.split("REG_SZ")[1].strip()
        except Exception as e:
            print(e)
            return "Spotify installation path not found on Windows."
    elif os_type == "Darwin":  # macOS
        path = "/Applications/Spotify.app"
        if os.path.exists(path):
            return path
        else:
            return "Spotify installation path not found on macOS."
    else:
        return "Unsupported OS."


spotify_path = find_spotify_path()
print(f"Spotify path: {spotify_path}")







