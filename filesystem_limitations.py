# coding: utf-8

from __future__ import unicode_literals

# Allow direct execution
import os
import sys
import platform
import subprocess
import logging
import ctypes

#sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class filesystem_limitations(object):

    default_limits = {
        "NAME_MAX": None,
        "NAME_MAX_BYTES": None,
        "PATH_MAX": None,
        "PATH_MAX_BYTES": None,
        "PATH_COMPONENT_MAX": None,
        "PATH_COMPONENT_MAX_BYTES": None,
        "FILESIZEBITS": None,
        "FILE_SIZE_MAX_BYTES": None,
        "SYSTEM": None,
        "WINDOWS_LONG_PATHS": None
    }

    def __init__(self):
        self.ntdll = None
        self.default_limits["SYSTEM"] = self.get_platform_system()
        if (self.default_limits["SYSTEM"] == "Windows"):
            self.ntdll = ctypes.WinDLL('ntdll')
            self.ntdll.RtlAreLongPathsEnabled.restype = ctypes.c_ubyte
            self.ntdll.RtlAreLongPathsEnabled.argtypes = ()
            if hasattr(self.ntdll, 'RtlAreLongPathsEnabled'):
                self.default_limits["WINDOWS_LONG_PATHS"] = bool(self.ntdll.RtlAreLongPathsEnabled())
        return

    # Based on: https://stackoverflow.com/questions/32807560/how-do-i-get-in-python-the-maximum-filesystem-path-length-in-unix
    def _get_filesystem_limitations_for_unix(self, target_dir):
        target_realpath = os.path.realpath(target_dir)
        target_abspath = os.path.abspath(target_realpath)
        limits = self.default_limits

        # TODO: It is likely possible for malicious values of target_abspath to cause
        # arbitrary code to execute. Likely need to escape single quotes, but what
        # about backslashes that occur before quotes?
        limits_commands = {
            "NAME_MAX": "getconf NAME_MAX '" + target_abspath + "'",
            "PATH_MAX": "getconf PATH_MAX '" + target_abspath + "'",
            "FILESIZEBITS": "getconf FILESIZEBITS '" + target_abspath + "'",
        }
        for limit_name in limits_commands:
            command = limits_commands[limit_name]
            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                output, error = process.communicate()
                retcode = process.poll()
                if (retcode == 0):
                    output = output.strip()
                    if (output != ""):
                        limits[limit_name] = output
                else:
                    logging.error("Filesystem limitations determination logic got a nonzero return value for command: " + command + ". Return value: " + retcode + ", stdout: '" + output + "', stderr: '" + error + "'.")
            except:
                logging.error("Filesystem limitations determination logic encountered an exception attempting to execute command: " + command + ".")
            
            if (limits[limit_name] != None):
                # Use long integers for values >= 1 billion.
                if ((len(limits[limit_name]) >= 10) and (sys.version_info.major >= 3)):
                    limits[limit_name] = long(limits[limit_name])
                else:
                    limits[limit_name] = int(limits[limit_name])
        # Post-processing.
        limits["NAME_MAX_BYTES"] = limits["NAME_MAX"]
        limits["PATH_MAX_BYTES"] = limits["PATH_MAX"]
        limits["PATH_COMPONENT_MAX"] = limits["PATH_MAX"]
        limits["PATH_COMPONENT_MAX_BYTES"] = limits["PATH_MAX_BYTES"]
        limits["FILE_SIZE_MAX_BYTES"] = 2 ** limits["FILESIZEBITS"]
        return limits

    def _get_filesystem_limitations_for_darwin(self, target_dir):
        limits = self._get_filesystem_limitations_for_unix(target_dir)
        return limits

    def _get_filesystem_limitations_for_linux(self, target_dir):
        limits = self._get_filesystem_limitations_for_unix(target_dir)
        return limits

    def _get_windows_volume_info_with_kernel32(self, target_dir):
        from ctypes import windll, wintypes
        target_realpath = os.path.realpath(target_dir)
        target_abspath = os.path.abspath(target_realpath)
        spdrive = os.path.splitdrive(target_abspath)
        target_rootpath = str(spdrive[0] + "\\")

        # BOOL GetVolumeInformationA(
        #   LPCSTR  lpRootPathName,
        #   LPSTR   lpVolumeNameBuffer,
        #   DWORD   nVolumeNameSize,
        #   LPDWORD lpVolumeSerialNumber,
        #   LPDWORD lpMaximumComponentLength,
        #   LPDWORD lpFileSystemFlags,
        #   LPSTR   lpFileSystemNameBuffer,
        #   DWORD   nFileSystemNameSize
        # );
        _GetVolumeInformationA = windll.kernel32.GetVolumeInformationA
        _GetLastError = windll.kernel32.GetLastError
        lpRootPathName = ctypes.create_string_buffer(target_rootpath.encode('UTF-8'))
        lpVolumeNameBuffer = ctypes.create_string_buffer(255)
        nVolumeNameSize = wintypes.DWORD(255)
        lpVolumeSerialNumber = wintypes.DWORD(0)
        lpMaximumComponentLength = wintypes.DWORD(0)
        lpFileSystemFlags = wintypes.DWORD(0)
        lpFileSystemNameBuffer = ctypes.create_string_buffer(255)
        nFileSystemNameSize = wintypes.DWORD(255)
        result = _GetVolumeInformationA(lpRootPathName, lpVolumeNameBuffer, nVolumeNameSize, ctypes.byref(lpVolumeSerialNumber), ctypes.byref(lpMaximumComponentLength), ctypes.byref(lpFileSystemFlags), lpFileSystemNameBuffer, nFileSystemNameSize)
        returninfo = "result: " + str(result)
        if (result == 0):
            lasterror = _GetLastError()
            returninfo += ", error code: " + hex(lasterror)

        return_data = {
            "lpRootPathName": str(lpRootPathName, 'UTF-8'),
            "lpVolumeNameBuffer": str(lpVolumeNameBuffer.value, 'UTF-8'),
            "lpVolumeSerialNumber": lpVolumeSerialNumber.value,
            "lpMaximumComponentLength": lpMaximumComponentLength.value,
            "lpFileSystemFlags": lpFileSystemFlags.value,
            "lpFileSystemNameBuffer": str(lpFileSystemNameBuffer.value, 'UTF-8'),
            "nFileSystemNameSize": nFileSystemNameSize.value,
        }

        if (sys.version_info.major >= 3):
            return_data["lpVolumeSerialNumber"] = int(return_data["lpVolumeSerialNumber"])
            return_data["lpMaximumComponentLength"] = int(return_data["lpMaximumComponentLength"])
            return_data["lpFileSystemFlags"] = int(return_data["lpFileSystemFlags"])
            return_data["nFileSystemNameSize"] = int(return_data["nFileSystemNameSize"])
        else:
            return_data["lpVolumeSerialNumber"] = long(return_data["lpVolumeSerialNumber"])
            return_data["lpMaximumComponentLength"] = long(return_data["lpMaximumComponentLength"])
            return_data["lpFileSystemFlags"] = long(return_data["lpFileSystemFlags"])
            return_data["nFileSystemNameSize"] = long(return_data["nFileSystemNameSize"])
        return return_data

    def _get_filesystem_limitations_for_windows(self, target_dir):
        limits = self.default_limits
        target_realpath = os.path.realpath(target_dir)
        target_abspath = os.path.abspath(target_realpath)
        try:
            volume_info = self._get_windows_volume_info_with_kernel32(target_abspath)
        except:
            # TODO: better handling of error
            logging.error("Filesystem limitations determination logic encountered an exception attempting to call Windows API function GetVolumeInformationA for target_dir: " + target_dir + ".")
            return limits
        fs_type = volume_info["lpFileSystemNameBuffer"]
        limits["NAME_MAX"] = volume_info["nFileSystemNameSize"]
        limits["PATH_COMPONENT_MAX"] = volume_info["lpMaximumComponentLength"]
        if (limits["WINDOWS_LONG_PATHS"] == True):
            limits["PATH_MAX"] = 32760
        else:
            limits["PATH_MAX"] = 260

        # https://docs.microsoft.com/en-us/windows/win32/fileio/filesystem-functionality-comparison
        limits["FILESIZEBITS"] = 64
        # All major Windows filesystems use UTF-16, taking 2 bytes per character
        limits["PATH_MAX_BYTES"] = limits["PATH_MAX"] * 2
        limits["NAME_MAX_BYTES"] = limits["NAME_MAX"] * 2
        limits["PATH_COMPONENT_MAX_BYTES"] = limits["PATH_COMPONENT_MAX"] * 2
        if (fs_type == "UDF"):
            limits["NAME_MAX_BYTES"] = limits["NAME_MAX_BYTES"] / 2
        elif (fs_type == "FAT32"):
            limits["FILESIZEBITS"] = 32
        limits["FILE_SIZE_MAX_BYTES"] = 2 ** limits["FILESIZEBITS"]
        return limits

    def get_platform_system(self):
        platform_system = platform.system()
        system = platform_system
        if (platform_system == "Java"):
            jver = platform.java_ver()
            system = jver[3][0]
        return system

    def get_filesystem_limitations(self, target_dir):
        system = self.get_platform_system()
        limits = self.default_limits

        if (os.path.isdir(target_dir) == False):
            logging.error("Target directory is required to exist prior to invoking filesystem limitation determination logic: " + target_dir + ".")
        elif (system == "Darwin"):
            limits = self._get_filesystem_limitations_for_darwin(target_dir)
        elif (system == "Linux"):
            limits = self._get_filesystem_limitations_for_linux(target_dir)
        elif (system == "Windows"):
            limits = self._get_filesystem_limitations_for_windows(target_dir)
        else:
            logging.warning("Filesystem limitation determination logic is not implemented for platform.system: " + system + ".")

        return limits

    @staticmethod
    def get(target_dir):
        limits = fs_limits.get_filesystem_limitations(target_dir)
        return limits

    def get_output_directory(self):
        return os.getcwd()

    def get_max_chars_for_output_directory_files(self):
        output_directory = os.getcwd()
        self.get_filesystem_limitations(output_directory)
        return stats.f_namemax

# Construct an instance of the class so that its static vars are initialized by __init__().
fs_limits = filesystem_limitations()

# Allow callers to have code of the form: import filesystem limitations ... filesystem_limitations.get(dir)
def get(target_dir):
    result = fs_limits.get_filesystem_limitations(target_dir)
    return result
