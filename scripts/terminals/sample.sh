#!/bin/sh
# The test card that preview.py --terminals shows in each terminal emulator: the theme's name, the default colours,
# the 16 ANSI colours as backgrounds and as text, and text attributes. Each colour block is wide enough for its pixels
# to be counted in a screenshot. $1 is the theme name.
esc=$(printf '\033')
printf '%s\n\n' "$1"
printf 'Default text on the default background. %s[1mBold%s[0m %s[2mFaint%s[0m %s[3mItalic%s[0m %s[4mUnderline%s[0m %s[7mReverse%s[0m\n\n' \
    "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc"
for row in 0 8; do
    i=$row
    while [ $i -lt $((row + 8)) ]; do
        printf '%s[48;5;%dm        %s[0m ' "$esc" "$i" "$esc"
        i=$((i + 1))
    done
    printf '\n'
    i=$row
    while [ $i -lt $((row + 8)) ]; do
        printf '%s[48;5;%dm        %s[0m ' "$esc" "$i" "$esc"
        i=$((i + 1))
    done
    printf '\n'
    i=$row
    while [ $i -lt $((row + 8)) ]; do
        printf '%s[38;5;%dm  %-6s%s[0m ' "$esc" "$i" "$i" "$esc"
        i=$((i + 1))
    done
    printf '\n\n'
done
printf '%s[32m+ added line%s[0m   %s[31m- removed line%s[0m   %s[34mdirectory/%s[0m   %s[33mwarning:%s[0m done\n' \
    "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc"
printf '$ '
# Keep the window open, with the cursor after the prompt, until the screenshot is taken.
exec sleep 600
