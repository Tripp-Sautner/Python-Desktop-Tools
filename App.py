import sys
import ctypes

import ctypes.wintypes


class MONITORINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.wintypes.DWORD),
        ("rcMonitor", ctypes.wintypes.RECT),
        ("rcWork", ctypes.wintypes.RECT),
        ("dwFlags", ctypes.wintypes.DWORD),
    ]


class App:
    current_layout = None

    def __init__(self):
        if len(sys.argv) > 1:
            self.input_variable = sys.argv[1]
        else:
            self.input_variable = None

    def run(self):
        self.print_monitor_info(int(self.input_variable))

    def save_layout(self):
        print("Saving current layout...")

    def apply_game_layout(self):
        self.save_layout()
        print("Applying game layout...")

    def print_monitor_info(self, which_monitor):
        print("Printing monitor info")

        # Using EnumDisplayMonitors to get monitor info print that info
        # Define the callback function for EnumDisplayMonitors
        def monitor_enum_callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
            # Get the monitor info
            monitor_info = MONITORINFO()
            monitor_info.cbSize = ctypes.sizeof(monitor_info)
            ctypes.windll.user32.GetMonitorInfoW(hMonitor, ctypes.byref(monitor_info))

            # Print the monitor info
            print("Monitor:", dwData)
            print("  Left:", monitor_info.rcMonitor.left)
            print("  Top:", monitor_info.rcMonitor.top)
            print("  Right:", monitor_info.rcMonitor.right)
            print("  Bottom:", monitor_info.rcMonitor.bottom)

            # Return True to continue enumerating monitors
            return True

        # Call EnumDisplayMonitors to enumerate all monitors
        ctypes.windll.user32.EnumDisplayMonitors(
            None,
            None,
            ctypes.WINFUNCTYPE(
                ctypes.c_bool,
                ctypes.wintypes.HMONITOR,
                ctypes.wintypes.HDC,
                ctypes.POINTER(ctypes.wintypes.RECT),
                ctypes.wintypes.LPARAM,
            )(monitor_enum_callback),
            0,
        )

    def revert(self):
        print("Running function_b")


if __name__ == "__main__":
    app = App()
    app.run()
