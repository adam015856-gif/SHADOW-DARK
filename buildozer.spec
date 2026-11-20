[app]

# (str) Title of your application
title = ShadowFly

# (str) Package name
package.name = shadowfly

# (str) Package domain (needed for android/ios packaging)
package.domain = org.shadow

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,wav,ogg,mp3,ttf

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# (comma separated e.g. requirements = sqlite3,kivy)
requirements = python3,kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT_TO_PY2

#
# OSX Specific
#

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (string) Presplash background color (for android presplash)
# Supported formats are #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgreen, lightblue, darkred, darkgreen, darkblue
android.presplash_color = #000000

# (string) Adaptive icon background color (for android adaptive icon)
#android.adaptive_icon_background_color = #FFFFFF

# (list) Permissions
# (php) android.permissions = INTERNET
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API you want your APP to support, it should usually match android.minapi
#android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android entry point, default is ok for kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (list) Pattern to allow while copying any files into the package
#android.add_filters = res/drawable-*/*.png

# (list) Files to add to the android project (you can add any files from the folder)
#android.add_aars =

# (list) Gradle dependencies to add (see https://developer.android.com/studio/build/dependencies for more details)
#android.gradle_dependencies =

# (list) add java compile options
# this can for example be necessary when importing certain java libraries using 'jnius'
# android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# (list) Gradle repositories to add {can be necessary for some android dependencies}
# please enclose in double quotes
# android.gradle_repositories =

# (list) packaging options to add
# see https://gradle.org/docs/current/userguide/android_plugin_basics.html#submitting_a_package_for_your_android_application
#android.add_packaging_options =

# (list) Java classes to add to the android project (can be necessary for your python code)
# android.add_src =

# (list) Android application meta-data to set (key=value format)
#android.meta_data =

# (list) Android library project to add (will be passed to the
# project.properties automatically, see the source code for details)
# android.library_references =

# (list) Android shared libraries which will be included into Android Package
#android.add_libs_armeabi_v7a = libs/android/armeabi-v7a/*.so
#android.add_libs_arm64_v8a = libs/android/arm64-v8a/*.so
#android.add_libs_x86 = libs/android/x86/*.so
#android.add_libs_x86_64 = libs/android/x86_64/*.so

# (bool) Indicate whether the game should be built with upx
#android.upx = False

# (str) python-for-android branch to use, defaults to master
#p4a.branch = develop

# (str) p4a local recipes directory
#p4a.local_recipes =

# (str) python-for-android specific commit to use
#p4a.commit =

# (str) python-for-android game version to use
#p4a.version =

# (str) OR you can use git url to use a particular branch or commit of p4a
#p4a.url =

# (list) python-for-android whitelist
#p4a.whitelist =

# (str) Issuer name for self-signed debug key
#android.debug_key_issuer =

# (str) Keystore file to use for release signing
#android.release_keystore =

# (str) Keystore password (if empty, it will be prompted for)
#android.release_keystore_passwd =

# (str) Alias name in keystore to use for release signing
#android.release_key_alias =

# (str) Key password (if empty, it will be prompted for)
#android.release_key_passwd =

# (str) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (int) overrides automatic versionCode computation (used in **only** versionCode computation)
# android.numeric_version = 1

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) If you need to insert variables into your AndroidManifest.xml
# default is {}, you can use format like {"foo":"bar"}
# android.manifest_placeholders = {}

# (bool) forces Android app to be built with Gradle
#android.gradle = True

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so

# (bool) Copy libs to build directory or not
#android.copy_libs = 1

# (str) The format used to package the application for release mode (aab or apk or aar)
android.release_artifact = apk

# (str) The format used to package the application for debug mode (aab or apk or aar)
android.debug_artifact = apk

#
# Python for android (p4a) specific
#

# (str) bootstrap to use for android (sdl2, webview, none)
p4a.bootstrap = sdl2

# (list) python-for-android arguments to pass to toolchain
#p4a.args =

#
# iOS specific
#

# (str) Path to a custom xcodeproj folder
#ios.xcodeproj =

# (str) Apple identity to use for signing (default: "iPhone Developer")
#ios.codesign.identity =

# (str) Apple team id for signing
#ios.codesign.allowed_team_ids =

# (str) developer profile to use for signing
#ios.codesign.debug = "iPhone Developer"

# (str) developer profile to use for signing
#ios.codesign.release = "iPhone Distribution"

# (bool) Whether or not to sign the code
#ios.codesign = True

# (str) Name of the certificate used for signing the debug version
#ios.codesign.debug_certificate =

# (str) Name of the certificate used for signing the release version
#ios.codesign.release_certificate =

# (str) Path to a custom entitlements file
#ios.entitlements =

# (str) Path to a custom Info.plist file
#ios.info_plist =

# (bool) Whether or not to add a launch screen storyboard
#ios.add_launch_screen = True

# (str) Custom launch screen storyboard name
#ios.custom_launch_screen =

# (str) iOS deployment target
#ios.deployment_target = 11.0


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = no, 1 = yes)
warn_on_root = 1

# (str) Path to build artifact storage, allow custom storage place
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab) storage
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    -[(list)] Custom source folders excluded from run
#    -[(list)] Source files to exclude (let empty to include all the files)
#

# (list) List of inclusions using pattern matching
#include.exts = spec

# (list) List of exclusions using pattern matching
#exclude.exts = spec

# (list) List of exclusions using pattern matching
#exclude.dirs = tests, bin, venv

# (str) Presplash image to use for the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png
