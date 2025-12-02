[app]
title = Burmese Wireless Debugging Toolkit
package.name = wirelessdebugging
package.domain = org.burmese.debugging
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

# အရေးကြီးဆုံးအပိုင်း (adb-shell နှင့် key generation အတွက် လိုအပ်သည်များ)
requirements = python3,kivy,adb-shell,cryptography,pyasn1,rsa,openssl,libffi

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_WIFI_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Android Config
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a

# Entry point (ဖိုင်နာမည် main.py ပြောင်းထားလျှင် ပိုကောင်းသည်)
android.entrypoint = main.py

# Colab အတွက် License လက်ခံခြင်း
android.accept_sdk_license = True

# Manifest
android.manifest.intent_filters = <intent-filter><action android:name="android.intent.action.MAIN" /><category android:name="android.intent.category.LAUNCHER" /></intent-filter>

[buildozer]
log_level = 2
warn_on_root = 1
