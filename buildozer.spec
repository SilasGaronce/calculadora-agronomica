[app]
title = Calculadora Agronomica
package.name = calculadorasolo
package.domain = org.meuapp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,otf
version = 0.1

# Deixamos as dependências limpas para o Buildozer alinhar com as receitas estáveis do Android
requirements = python3, kivy, charset-normalizer

# Mudado de master para develop para carregar as correções automáticas de compilação do freetype/SDL2
p4a.branch = develop

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
