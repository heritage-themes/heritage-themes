#!/bin/sh
# Starts the Android emulator that scripts/termux/shoot.py drives, with Termux and Termux:Styling installed.
#
# Needs KVM (/dev/kvm), ImageMagick, the GitHub CLI, and the Android SDK in $ANDROID_SDK_ROOT (default ~/Android/Sdk)
# with `emulator`, `platform-tools` and `cmdline-tools/latest`. The first run downloads an Android 14 x86_64 system
# image and the Termux APKs, which it checks against the checksums the releases publish. The GitHub builds are used
# because the Play Store build is outdated. Later runs only start the emulator.
set -eu

SDK=${ANDROID_SDK_ROOT:-$HOME/Android/Sdk}
export ANDROID_SDK_ROOT="$SDK"
IMAGE="system-images;android-34;google_apis;x86_64"
AVD=termux
APP_TAG=v0.118.3
STYLING_TAG=v0.32.1
WORK=${TMPDIR:-/tmp}/heritage-termux

if [ ! -d "$HOME/.android/avd/$AVD.avd" ]; then
    yes | "$SDK/cmdline-tools/latest/bin/sdkmanager" "$IMAGE" >/dev/null
    echo no | "$SDK/cmdline-tools/latest/bin/avdmanager" create avd -n "$AVD" -k "$IMAGE" -d pixel_6 >/dev/null
    # A hardware keyboard keeps the soft keyboard from covering the lower half of the screen.
    sed -i 's/^hw.keyboard *=.*/hw.keyboard = yes/' "$HOME/.android/avd/$AVD.avd/config.ini"
fi

adb start-server >/dev/null
if ! adb get-state >/dev/null 2>&1; then
    nohup "$SDK/emulator/emulator" -avd "$AVD" -no-window -no-audio -no-snapshot -no-boot-anim \
        -gpu swiftshader_indirect -memory 4096 >"$WORK.log" 2>&1 &
    adb wait-for-device
    until [ "$(adb shell getprop sys.boot_completed | tr -d '\r')" = 1 ]; do sleep 2; done
fi
adb shell settings put secure show_ime_with_hard_keyboard 0

if ! adb shell pm list packages | grep -q '^package:com.termux$'; then
    rm -rf "$WORK"
    mkdir -p "$WORK/app" "$WORK/styling"
    gh release download "$APP_TAG" -R termux/termux-app -D "$WORK/app" -p '*x86_64.apk' -p '*sha256sums'
    gh release download "$STYLING_TAG" -R termux/termux-styling -D "$WORK/styling" -p '*.apk' -p 'checksums-sha256.txt'
    (cd "$WORK/app" && grep x86_64.apk ./*sha256sums | sha256sum -c -)
    (cd "$WORK/styling" && sha256sum -c checksums-sha256.txt)
    adb install "$WORK"/app/*.apk
    adb install "$WORK"/styling/*.apk
    # Termux installs its packages on first launch, which needs the network.
    adb shell am start -n com.termux/.app.TermuxActivity >/dev/null
    sleep 60
fi
