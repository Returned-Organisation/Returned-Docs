"""Safe Unturned -> Returned rename for product prose only."""
from pathlib import Path
import re

root = Path(r"c:\Users\Eli\Documents\Returned-Docs")
skip_dirs = {"_build", ".venv", ".git"}
files = [
    p
    for p in root.rglob("*")
    if p.suffix in {".rst", ".md"} and not any(s in p.parts for s in skip_dirs)
]

# Lines / spans to never rewrite
SKIP_LINE_RE = re.compile(
    r"("
    r"https?://"
    r"|unturned\.wiki"
    r"|code-block:: unturned"
    r"|SDG\.Unturned"
    r"|UnturnedLog"
    r"|Rocket\.Unturned"
    r"|OpenMod\.Unturned"
    r"|Unturned-Docs"
    r"|UnturnedHostBans"
    r"|UnturnedAnniversary"
    r"|Unturned_Anniversary"
    r"|Unturned Dedicated Server"
    r"|Unturned\.exe"
    r"|Window > Unturned"
    r"|Create > Unturned"
    r"|Stereo_Songs\.Unturned"
    r"|unturned_theme"
    r"|myunturnedserver"
    r"|UnturnedDat"
    r"|Unturned/Extras"
    r"|Unturned/Modules"
    r"|Unturned/Bundles"
    r"|C:\\Unturned"
    r"|C:/Unturned"
    r"|\\.\\./\\.\\./\\.\\./Unturned"
    r"|\\.\\.\\./Unturned"
    r"|Right-click \*\*Unturned\*\*"
    r"|Right-click Unturned in your Steam"
    r"|Unturned Wiki"
    r"|Unturned Roadmap"
    r"|Unturned modding documentation"
    r"|mod of \[Unturned\]"
    r"|mod of `Unturned"
    r"|documents Unturned"
    r"|chapter in Unturned docs"
    r"|retail Unturned"
    r"|Generic Unturned modding"
    r"|alongside Unturned but"
    r"|Adding \*Unturned\* to your Steam"
    r"|Use Unturned's app ID"
    r"|app ID ``304930``"
    r"|discord\.gg/unturned"
    r")"
)

# Within a line that is otherwise OK, protect inline code and links
INLINE_PROTECT = [
    re.compile(r"``[^`]*``"),
    re.compile(r"`[^`]+`_"),
    re.compile(r"`[^`]+`__"),
    re.compile(r"\[[^\]]*\]\([^\)]+\)"),
]


def protect_inline(line: str):
    slots = []

    def repl(m):
        slots.append(m.group(0))
        return f"@@I{len(slots)-1}@@"

    out = line
    for pat in INLINE_PROTECT:
        out = pat.sub(repl, out)
    return out, slots


def unprotect_inline(line: str, slots):
    for i, s in enumerate(slots):
        line = line.replace(f"@@I{i}@@", s)
    return line


WORD_REPLS = [
    (re.compile(r"\*Unturned\*'s"), "*Returned*'s"),
    (re.compile(r"Unturned's"), "Returned's"),
    (re.compile(r"\*Unturned\*"), "*Returned*"),
    (re.compile(r"\*\*Unturned\*\*"), "**Returned**"),
    (re.compile(r"\bvanilla Unturned\b"), "vanilla Returned"),
    (re.compile(r"\bcommon Unturned essentials plugins\b"), "common essentials plugins"),
    (re.compile(r"\bInstalling Unturned\b"), "Installing Returned"),
    (re.compile(r"\bMy Unturned Server\b"), "My Returned Server"),
    (re.compile(r"\bdefault Unturned UI icons\b"), "default Returned UI icons"),
    (re.compile(r"\bUnturned Configuration\b"), "Returned Configuration"),
    (re.compile(r"\bUnturned editor/dev\b"), "Returned editor/dev"),
    (re.compile(r"(?<![\w./\\-])Unturned(?![\w./\\-])"), "Returned"),
]

changed = []
for f in files:
    original = f.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)
    out_lines = []
    file_changed = False
    for line in lines:
        if SKIP_LINE_RE.search(line):
            out_lines.append(line)
            continue
        protected, slots = protect_inline(line)
        new = protected
        for pat, repl in WORD_REPLS:
            new = pat.sub(repl, new)
        new = unprotect_inline(new, slots)
        if new != line:
            file_changed = True
        out_lines.append(new)
    if file_changed:
        text = "".join(out_lines)
        if not text.endswith("\n") and original.endswith("\n"):
            text += "\n"
        f.write_text(text, encoding="utf-8", newline="\n")
        changed.append(str(f.relative_to(root)))

print(f"updated {len(changed)} files")
for c in changed:
    print(c)
assert not any("@@KEEP" in f.read_text(encoding="utf-8") or "@@I" in f.read_text(encoding="utf-8") for f in files)
print("no leftover placeholders")
