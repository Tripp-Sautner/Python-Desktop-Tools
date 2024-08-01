import ctypes
from ctypes import wintypes

# Define necessary structures and constants
class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName", wintypes.WCHAR * 32),
        ("dmSpecVersion", wintypes.WORD),
        ("dmDriverVersion", wintypes.WORD),
        ("dmSize", wintypes.WORD),
        ("dmDriverExtra", wintypes.WORD),
        ("dmFields", wintypes.DWORD),
        ("dmPositionX", wintypes.LONG),
        ("dmPositionY", wintypes.LONG),
        ("dmDisplayOrientation", wintypes.DWORD),
        ("dmDisplayFixedOutput", wintypes.DWORD),
        ("dmColor", wintypes.SHORT),
        ("dmDuplex", wintypes.SHORT),
        ("dmYResolution", wintypes.SHORT),
        ("dmTTOption", wintypes.SHORT),
        ("dmCollate", wintypes.SHORT),
        ("dmFormName", wintypes.WCHAR * 32),
        ("dmLogPixels", wintypes.WORD),
        ("dmBitsPerPel", wintypes.DWORD),
        ("dmPelsWidth", wintypes.DWORD),
        ("dmPelsHeight", wintypes.DWORD),
        ("dmDisplayFlags", wintypes.DWORD),
        ("dmDisplayFrequency", wintypes.DWORD),
        ("dmICMMethod", wintypes.DWORD),
        ("dmICMIntent", wintypes.DWORD),
        ("dmMediaType", wintypes.DWORD),
        ("dmDitherType", wintypes.DWORD),
        ("dmReserved1", wintypes.DWORD),
        ("dmReserved2", wintypes.DWORD),
        ("dmPanningWidth", wintypes.DWORD),
        ("dmPanningHeight", wintypes.DWORD)
    ]

ENUM_CURRENT_SETTINGS = -1
CDS_UPDATEREGISTRY = 0x00000001
DISP_CHANGE_SUCCESSFUL = 0

# Define necessary functions
EnumDisplayDevices = ctypes.windll.user32.EnumDisplayDevicesW
EnumDisplayDevices.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.POINTER(DEVMODE), wintypes.DWORD]
EnumDisplayDevices.restype = wintypes.BOOL

EnumDisplaySettings = ctypes.windll.user32.EnumDisplaySettingsW
EnumDisplaySettings.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.POINTER(DEVMODE)]
EnumDisplaySettings.restype = wintypes.BOOL

ChangeDisplaySettingsEx = ctypes.windll.user32.ChangeDisplaySettingsExW
ChangeDisplaySettingsEx.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(DEVMODE), wintypes.HWND, wintypes.DWORD, wintypes.LPVOID]
ChangeDisplaySettingsEx.restype = wintypes.LONG

def set_display_settings(device_name, width, height, frequency):
    devmode = DEVMODE()
    devmode.dmSize = ctypes.sizeof(DEVMODE)
    
    # Get current settings
    if not EnumDisplaySettings(device_name, ENUM_CURRENT_SETTINGS, ctypes.byref(devmode)):
        print("Failed to get display settings")
        return
    
    # Modify settings
    devmode.dmPelsWidth = width
    devmode.dmPelsHeight = height
    devmode.dmDisplayFrequency = frequency
    devmode.dmFields = 0x00080000 | 0x00100000 | 0x00400000  # DM_PELSWIDTH | DM_PELSHEIGHT | DM_DISPLAYFREQUENCY
    
    # Apply new settings
    result = ChangeDisplaySettingsEx(device_name, ctypes.byref(devmode), None, CDS_UPDATEREGISTRY, None)
    if result == DISP_CHANGE_SUCCESSFUL:
        print("Display settings changed successfully")
    else:
        print("Failed to change display settings")

# Example usage
device_name = "\\\\.\\DISPLAY1"  # You may need to enumerate devices to get the correct name
set_display_settings(device_name, 1920, 1080, 60)