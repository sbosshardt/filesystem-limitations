# filesystem-limitations

A cross-platform Python library providing a simple way to determine filesystem limitations of a given directory.


## Information Returned
| Name | Type | Value Description |
|--|--|--|
| NAME_MAX | int (long) | Maximum number of characters that a file's name can be. |
| PATH_MAX | int (long) | Maximum number of characters that a file's path (including the file's name) can be. |
| PATH_COMPONENT_MAX | int (long) | Maximum number of characters that a path component can be. In practice this can be useful for determining how long a new subdirectory's name can be. |
| NAME_MAX_BYTES | int (long) | Maximum number of bytes that a file's name can be. |
| PATH_MAX_BYTES | int (long) | Maximum number of bytes that a file's path (including the file's name) can be. |
| PATH_COMPONENT_BYTES | int (long) | Maximum number of bytes that a path component can be. |
| FILE_MAX_SIZE_BYTES | int (long) | Maximum size that a file can be (in bytes). |
| FILESIZEBITS | int (long) | Number of bits used by the filesystem to address file data. |
| SYSTEM | string | e.g. "Linux", "Darwin", or "Windows". Mainly platform.system(), but compensates for Java (returns the host system instead of "Java"). |
| WINDOWS_LONG_PATHS | Boolean or None | On Windows this value is True if Windows long paths are enabled (and False if not). This value is None if running in a non-Windows environment. |

## Supported Systems
 - Linux
 - Mac OSX (macOS)
 - Windows

**Also (more testing needed):**
 - Java (Jython)
 - Unix (untested on unixes other than MacOS and Linux)


## Usage
TODO: write examples
