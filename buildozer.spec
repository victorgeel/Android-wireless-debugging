[app]
title = Burmese Wireless Debugging Toolkit
package.name = wirelessdebugging
package.domain = org.burmese.debugging
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,adb-shell
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_WIFI_STATE
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.entrypoint = wireless_debugging_app.py
android.icon = icon.png
android.manifest.intent_filters =
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>

[buildozer]
log_level = 2
warn_on_root = 1
