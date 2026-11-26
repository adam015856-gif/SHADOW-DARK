[app]

# (str) Title of your application
title = SHADOW DARK

# (str) Package name
package.name = shadowdark

# (str) Package domain (needed for android/ios packaging)
package.domain = org.shadowdark

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,ttf

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# (comma separated e.g. requirements = python3,kivy)
requirements = python3,kivy

# (list) Supported orientations
# (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) agrree to the Android SDK license
android.accept_sdk_license = True
