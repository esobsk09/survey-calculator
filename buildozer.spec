[app]

title = Survey Calculator
package.name = surveycalculator
package.domain = org.surveycalculator

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_exts = spec

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 23
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a

p4a.branch = master

[buildozer]

log_level = 2
warn_on_root = 1
