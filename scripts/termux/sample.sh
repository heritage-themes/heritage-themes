#!/bin/sh
# The test card that scripts/termux/shoot.py shows in Termux: the theme's name, the default colours, the 16 ANSI colours
# as backgrounds and as text, and text attributes. It is laid out for a phone's 45 columns, in four blocks per row.
# Each colour block is wide enough for its pixels to be counted in a screenshot. $1 is the theme name.
esc=$(printf '\033')
printf '%s\n\n' "$1"
printf 'Default text on the default background.\n%s[1mBold%s[0m %s[2mFaint%s[0m %s[3mItalic%s[0m %s[4mUnderline%s[0m %s[7mReverse%s[0m\n\n' \
    "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc"
for row in 0 4 8 12; do
    for kind in 48 48 38; do
        i=$row
        while [ $i -lt $((row + 4)) ]; do
            if [ $kind = 48 ]; then
                printf '%s[48;5;%dm        %s[0m ' "$esc" "$i" "$esc"
            else
                printf '%s[38;5;%dm  %-6s%s[0m ' "$esc" "$i" "$i" "$esc"
            fi
            i=$((i + 1))
        done
        printf '\n'
    done
    printf '\n'
done
printf '%s[32m+ added%s[0m %s[31m- removed%s[0m %s[34mdir/%s[0m %s[33mwarning:%s[0m\n' \
    "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc"
