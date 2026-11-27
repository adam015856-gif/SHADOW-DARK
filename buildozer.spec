[app]

# اسم التطبيق وحزمة البناء
title = SHADOW DARK
package.name = shadowdark
package.domain = org.shadowdark

# الكود المصدري والامتدادات
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# الإصدار
version = 0.1

# المتطلبات البرمجية (Python + Kivy + pyjnius للوصول إلى Android APIs)
requirements = python3,kivy,pyjnius,android

# الاتجاه والواجهة
orientation = portrait
fullscreen = 0

# إعدادات Android (API 33 / 34 متوافقة مع Buildozer الحديث)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# صلاحيات Android المطلوبة (قراءة التطبيقات المثبتة على Android 11+)
android.permissions = INTERNET,QUERY_ALL_PACKAGES

# البناء التلقائي كـ debug APK
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# مستوى السجلات
log_level = 2
warn_on_root = 1
