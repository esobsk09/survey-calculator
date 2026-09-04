[app]

title = Survey Calculator
package.name = surveycalculator
package.domain = org.example

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,atlas
source.exclude_dirs = .git,.github,.buildozer,bin

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a

p4a.branch = master

[buildozer]

log_level = 2
warn_on_root = 0
