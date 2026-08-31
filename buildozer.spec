[app]
title = Calculadora Agronomica
package.name = calculadorasolo
package.domain = org.meuapp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,otf
version = 0.1
requirements = python3, kivy==2.3.0, charset-normalizer
p4a.branch = master
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24
android.archs = arm64-v8a
android.accept_sdk_license = True
android.entrypoint = org.kivy.android.PythonActivity
android.enable_androidx = True
android.pythons = python3

[buildozer]
log_level = 2
warn_on_root = 1
