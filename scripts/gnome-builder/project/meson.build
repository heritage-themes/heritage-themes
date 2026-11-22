project('heritage-builder-test', 'c', default_options: ['warning_level=3'])

# main.c builds and runs, for breakpoints and the debugger.
executable('demo', 'main.c')

# diagnostics.c holds deliberate errors and warnings, so it is not built by default.
executable('diagnostics', 'diagnostics.c', build_by_default: false)
