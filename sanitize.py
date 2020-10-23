
substitutions = (
    ('<',  '_esc__0_'),
    ('>',  '_esc__1_'),
    ('@',  '_esc__2_'),
    ('\\', '_esc__3_'),
    (',',  '_esc__4_'),
    ('-',  '_esc__5_'),
    ('$',  '_esc__6_')
)


def sanitizeLabel(string):
    for s in substitutions:
        string = string.replace(s[0], s[1])
    return string


def desanitizeLabel(string):
    for s in substitutions:
        string = string.replace(s[1], s[0])
    return string
