# https://github.com/Shizmob/clippy
# coding=utf-8
# clippy
# get or set text data on your clipboard.
import sys
import os
import os.path as path
import subprocess
import locale
import ctypes


## Utilities.

py3 = sys.version_info >= (3, 0)


def unicode_or_bytes(input):
    if py3:
        return isinstance(input, (str, bytes))
    else:
        return isinstance(input, (unicode, str))


def to_unicode(input, encoding="ascii"):
    if py3:
        if isinstance(input, str):
            return input
        if isinstance(input, bytes):
            return input.decode(encoding)
    else:
        if isinstance(input, unicode):
            return input
        if isinstance(input, str):
            return unicode(input, encoding)


def to_bytes(input, encoding="utf-8"):
    if py3:
        if isinstance(input, str):
            return input.encode(encoding)
        if isinstance(input, bytes):
            return input
    else:
        if isinstance(input, unicode):
            return input.encode(encoding)
        if isinstance(input, str):
            return input


def which(name, flag=os.X_OK):
    """ Search PATH for given executable name. """
    executables = []

    paths = [entry for entry in os.environ.get("PATH", "").split(os.pathsep) if entry]
    extensions = [ext for ext in os.environ.get("PATHEXT", "").split(os.pathsep) if ext]

    for entry in paths:
        base = path.join(entry, name)

        # No PATHEXT? Go for bare executables.
        if not extensions and os.access(base, flag) and base not in executables:
            executables.append(base)
        else:
            # Search PATHEXT.
            for ext in extensions:
                wanted = base + "." + ext
                if os.access(wanted, flag) and wanted not in executables:
                    executables.append(wanted)

    return executables


def supported():
    """ Return whether clippy supports this platform or not. """
    return get != unknown_get and set != unknown_set and clear != unknown_clear


## OS APIs.

# Win32.

WIN32_CF_TEXT = 1
WIN32_CF_UNICODETEXT = 13
WIN32_ENCODING = "ascii"
WIN32_UNICODE_ENCODING = "utf-16-le"


def win32_setup():
    """ Setup relevant ctypes argtypes and return (user32, kernel32) pair. """
    # Make ctypes happy.
    if not hasattr(win32_setup, "user32"):
        win32_setup.user32 = ctypes.windll.user32

        user32 = win32_setup.user32
        user32.OpenClipboard.argtypes = [ctypes.c_void_p]
        user32.GetClipboardData.restype = ctypes.c_void_p
        user32.SetClipboardData.argtypes = [ctypes.c_uint, ctypes.c_void_p]
        user32.SetClipboardData.restype = ctypes.c_void_p
        user32.GetActiveWindow.restype = ctypes.c_void_p

    if not hasattr(win32_setup, "kernel32"):
        win32_setup.kernel32 = ctypes.windll.kernel32

        kernel32 = win32_setup.kernel32
        kernel32.GlobalAlloc.argtypes = [ctypes.c_uint, ctypes.c_size_t]
        kernel32.GlobalAlloc.restype = ctypes.c_void_p
        kernel32.GlobalFree.argtypes = [ctypes.c_void_p]
        kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
        kernel32.GlobalLock.restype = ctypes.c_void_p
        kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]

    return win32_setup.user32, win32_setup.kernel32


def win32_clear():
    """ Clear clipboard text data. """
    user32, kernel32 = win32_setup()

    window = user32.GetActiveWindow()
    user32.OpenClipboard(window)
    user32.EmptyClipboard()
    user32.CloseClipboard()


def win32_get():
    """ Get clipboard text data. Returns a unicode instance or None. """
    user32, kernel32 = win32_setup()
    data = None

    window = user32.GetActiveWindow()
    user32.OpenClipboard(window)

    if data is None:
        # Try Unicode data first.
        contents = user32.GetClipboardData(WIN32_CF_UNICODETEXT)
        if contents is not None:
            # Lock data, decode data, unlock it.
            lock = kernel32.GlobalLock(contents)
            data = ctypes.c_wchar_p(contents).value
            kernel32.GlobalUnlock(lock)
    if data is None:
        # Try normal text.
        contents = user32.GetClipboardData(WIN32_CF_TEXT)
        if contents is not None:
            # Lock data, decode data, unlock it.
            lock = kernel32.GlobalLock(contents)
            data = to_unicode(ctypes.c_char_p(contents).value, WIN32_ENCODING)
            kernel32.GlobalUnlock(lock)

    user32.CloseClipboard()
    return data


def win32_set(data):
    """ Set clipboard text data. Accepts unicode or str. """
    user32, kernel32 = win32_setup()

    if not unicode_or_bytes(data):
        raise TypeError("Clipboard data can only be unicode strings or bytes.")
    unidata = to_unicode(data).encode(WIN32_UNICODE_ENCODING)
    asciidata = to_bytes(data, WIN32_ENCODING)

    window = user32.GetActiveWindow()
    user32.OpenClipboard(window)
    user32.EmptyClipboard()

    # Set UNICODETEXT.
    try:
        win32_set_data(WIN32_CF_UNICODETEXT, unidata)
    except RuntimeError:
        pass

    # Set TEXT.
    try:
        win32_set_data(WIN32_CF_TEXT, asciidata)
    except RuntimeError:
        pass

    user32.CloseClipboard()


def win32_set_data(type, data):
    """ Set clipboard data for specific type from data. """
    user32, kernel32 = win32_setup()
    ptr = kernel32.GlobalAlloc(0, len(data) + 1)

    if ptr is not None:
        # Copy data over.
        lock = kernel32.GlobalLock(ptr)
        dataptr = ctypes.c_char_p(data)
        ctypes.memmove(ptr, dataptr, len(data) + 1)
        kernel32.GlobalUnlock(lock)

        # Set clipboard.
        res = user32.SetClipboardData(type, ptr)
        if res is None:
            # Setting data failed. Deallocate.
            kernel32.GlobalFree(ptr)
            raise RuntimeError("Could not set clipboard data.")


# OS X.


def osx_pb_clear():
    """ Clear clipboard text data. """
    with open(os.devnull, "rb") as f:
        process = subprocess.Popen(["pbcopy"], stdin=f)
        process.wait()


def osx_pb_get():
    """ Get clipboard text data. Return a unicode instance, or None. """
    process = subprocess.Popen(["pbpaste"], stdout=subprocess.PIPE)
    data, _ = process.communicate()
    encoding = locale.getpreferredencoding()

    return to_unicode(data, encoding) if data else None


def osx_pb_set(data):
    """ Set clipboard text data. Accepts a unicode or str. """
    if not unicode_or_bytes(data):
        raise TypeError("Clipboard data can only be unicode or str.")
    data = to_unicode(data)

    encoding = locale.getpreferredencoding()
    raw = data.encode(encoding)

    process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
    process.communicate(raw)


# X windowing system: xclip.

X_CLIPBOARDS = ["CLIPBOARD", "PRIMARY"]


def x_xclip_clear():
    """ Clear clipboard text data. """
    with open(os.devnull, "rb") as f:
        for clipboard in X_CLIPBOARDS:
            process = subprocess.Popen(
                ["xclip", "-selection", clipboard.lower(), "-i"], stdin=f
            )
            process.wait()


def x_xclip_get():
    """ Get clipboard text data. Return a unicode instance, or None. """
    raw = None
    encoding = locale.getpreferredencoding()

    for clipboard in X_CLIPBOARDS:
        process = subprocess.Popen(
            ["xclip", "-selection", clipboard.lower(), "-o"], stdout=subprocess.PIPE
        )
        raw, _ = process.communicate()

        if process.returncode == 0 and raw:
            break

    return to_unicode(raw, encoding) if raw else None


def x_xclip_set(data):
    """ Set clipboard text data. Accepts a unicode or str. """
    if not unicode_or_bytes(data):
        raise TypeError("Clipboard data can only be unicode or str.")
    data = to_unicode(data)

    encoding = locale.getpreferredencoding()
    raw = data.encode(encoding)

    for clipboard in X_CLIPBOARDS:
        process = subprocess.Popen(
            ["xclip", "-selection", clipboard.lower(), "-i"], stdin=subprocess.PIPE
        )
        process.communicate(raw)


# X windowing system: xsel.


def x_xsel_clear():
    """ Clear clipboard text data. """
    with open(os.devnull, "rb") as f:
        for clipboard in X_CLIPBOARDS:
            process = subprocess.Popen(
                ["xsel", "--" + clipboard.lower(), "-i"], stdin=f
            )
            process.wait()


def x_xsel_get():
    """ Get clipboard text data. Return a unicode instance, or None. """
    raw = None
    encoding = locale.getpreferredencoding()

    for clipboard in X_CLIPBOARDS:
        process = subprocess.Popen(
            ["xsel", "--" + clipboard.lower()], stdout=subprocess.PIPE
        )
        raw, _ = process.communicate()

        if process.returncode == 0 and raw:
            break

    return to_unicode(raw, encoding) if raw else None


def x_xsel_set(data):
    """ Set clipboard text data. Accepts a unicode or str. """
    if not unicode_or_bytes(data):
        raise TypeError("Clipboard data can only be unicode or str.")
    data = to_unicode(data)

    encoding = locale.getpreferredencoding()
    raw = data.encode(encoding)

    for clipboard in X_CLIPBOARDS:
        process = subprocess.Popen(
            ["xsel", "--" + clipboard.lower()], stdin=subprocess.PIPE
        )
        process.communicate(raw)


# Unknown platform. Just error.


def unknown_clear():
    raise RuntimeError(
        "clippy hasn't been ported to this platform ({}) yet.".format(sys.platform)
    )


def unknown_get():
    raise RuntimeError(
        "clippy hasn't been ported to this platform ({}) yet.".format(sys.platform)
    )


def unknown_set(data):
    raise RuntimeError(
        "clippy hasn't been ported to this platform ({}) yet.".format(sys.platform)
    )


## Selecta!

if sys.platform.startswith("win") or sys.platform == "cygwin":
    get = win32_get
    set = win32_set
    clear = win32_clear
elif sys.platform == "darwin" and which("pbcopy") and which("pbpaste"):
    get = osx_pb_get
    set = osx_pb_set
    clear = osx_pb_clear
elif which("xclip"):
    get = x_xclip_get
    set = x_xclip_set
    clear = x_xclip_clear
elif which("xsel"):
    get = x_xsel_get
    set = x_xsel_set
    clear = x_xsel_clear
else:
    get = unknown_get
    set = unknown_set
    clear = unknown_clear


## Tests.

if __name__ == "__main__":
    print("testing ASCII...")
    set("foo!")
    assert get() == u"foo!"
    print("success")

    print("testing Unicode...")
    set(u"( ≖‿≖)")
    assert get() == u"( ≖‿≖)"
    print("success")

    print("testing clear...")
    clear()
    assert get() is None
    print("success")
