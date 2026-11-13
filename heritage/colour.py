"""Colour measures that the targets share: CIE L*a*b*, the CIE76 distance between two colours, and the role of
preprocessor directives, which the palettes give no role of their own. It imports nothing from the other modules, so
any of them can import it."""

# The least CIE76 distance at which the colour of a preprocessor directive reads as another colour than a keyword's. The
# palettes keep their keyword at least 15 from each of their other code colours.
DIRECTIVE_APART = 20


def lab(rgb):
    """CIE L*a*b* of an sRGB colour given as (r, g, b) in 0-255."""
    def linear(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = map(linear, rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116
    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))


def distance(a, b):
    """The CIE76 distance between two six-digit hex colours."""
    def channels(hex_colour):
        return [int(hex_colour[i:i + 2], 16) for i in (0, 2, 4)]
    return sum((x - y) ** 2 for x, y in zip(lab(channels(a)), lab(channels(b)))) ** 0.5


def directive(p):
    """The palette role of preprocessor directives, such as C's #include, which Visual Studio's own themes colour apart
    from keywords: annotation, as for macros and attributes, or constant where the palette gives annotations a colour
    within DIRECTIVE_APART of the keyword's."""
    return "annotation" if distance(p["annotation"], p["keyword"]) >= DIRECTIVE_APART else "constant"
