from pathlib import Path
import re

root = Path(r"c:\Users\Eli\Documents\Returned-Docs")
skip_dirs = {"_build", ".venv", ".git"}
files = [
    p
    for p in root.rglob("*")
    if p.suffix in {".rst", ".md"} and not any(s in p.parts for s in skip_dirs)
]

# Protect tokens that must stay Unturned / unturned
PROTECT = [
    (r"https?://[^\s`<\]'\"]+", "URL"),
    (r"`[^`]*unturned[^`]*`_", "RSTLINK"),
    (r"`[^`]*Unturned[^`]*`_", "RSTLINK2"),
    (r"\[[^\]]*\]\([^\)]*unturned[^\)]*\)", "MDLINK"),
    (r"\[[^\]]*\]\([^\)]*Unturned[^\)]*\)", "MDLINK2"),
    (r"\.\. code-block:: unturned\w*", "CODEBLOCK"),
    (r"``[^`]*``", "INLINECODE"),
    (r"SDG\.Unturned", "NS"),
    (r"UnturnedLog", "LOG"),
    (r"Rocket\.Unturned", "ROCKET"),
    (r"OpenMod\.Unturned(?:\.Module)?", "OPENMOD"),
    (r"Unturned-Docs", "DOCSREPO"),
    (r"UnturnedHostBans", "HOSTBANS"),
    (r"UnturnedAnniversary", "ANNIV1"),
    (r"Unturned_Anniversary", "ANNIV2"),
    (r"Unturned Dedicated Server", "U3DSNAME"),
    (r"Unturned\.exe", "EXE"),
    (r"Window > Unturned", "WINMENU"),
    (r"Create > Unturned", "CREATEMENU"),
    (r"Stereo_Songs\.Unturned_Theme", "SONGTOKEN"),
    (r"unturned_theme\.mp3", "SONGFILE"),
    (r"myunturnedserver", "DNSEX"),
    (r"\.\.\./Unturned", "PATHREL"),
    (r"C:\\\\Unturned", "PATHWIN"),
    (r"C:\\Unturned", "PATHWIN2"),
    (r"Unturned/Extras", "PATHEXTRA"),
    (r"Unturned/Modules", "PATHMOD"),
    (r"Unturned folder", "PATHFOLDER"),
    (r"Unturned installation directory", "PATHINSTALL"),
    (r"inside the Unturned installation", "PATHINSTALL2"),
    (r"SmartlyDressedGames/Unturned-Docs", "UPSTREAM"),
    (r"Unturned modding documentation", "UPSTREAMDOCS"),
    (r"Unturned Roadmap", "ROADMAP"),
    (r"Unturned Wiki", "WIKI"),
    (r"Pages linked from Unturned Documentation", "WIKICAT"),
    (r"non-commercial mod of `Unturned", "MODOF1"),
    (r"non-commercial mod of \[Unturned\]", "MODOF2"),
    (r"documents Unturned", "AGENTDOC"),
    (r"upstream documents Unturned", "AGENTDOC2"),
    (r"chapter in Unturned docs", "AGENTCHAP"),
    (r"not in retail Unturned", "AGENTRETAIL"),
    (r"Generic Unturned modding", "AGENTGEN"),
    (r"Right-click \*\*Unturned\*\* in your Steam", "STEAMAPP"),
    (r"Right-click Unturned in your Steam", "STEAMAPP2"),
    (r"Right-click Unturned in your Steam library", "STEAMAPP3"),
    (r"alongside Unturned but", "ALONGSIDE"),
    (r"Adding \*Unturned\* to your Steam Library", "STEAMADD"),
    (r"Use Unturned's app ID", "APPID"),
]


def protect(text: str):
    slots = []

    def make_repl(_kind: str):
        def _inner(m):
            slots.append(m.group(0))
            return f"@@KEEP{len(slots)-1}@@"

        return _inner

    out = text
    for pat, kind in PROTECT:
        out = re.sub(pat, make_repl(kind), out)
    out = re.sub(r"unturned\.wiki\.gg[^\s`']*", make_repl("WIKIDOMAIN"), out)
    return out, slots


def unprotect(text: str, slots: list[str]) -> str:
    for i, s in enumerate(slots):
        text = text.replace(f"@@KEEP{i}@@", s)
    return text


replacements = [
    (r"\*Unturned\*'s", "*Returned*'s"),
    (r"Unturned's", "Returned's"),
    (r"\*Unturned\*", "*Returned*"),
    (r"\*\*Unturned\*\*", "**Returned**"),
    (r"\bvanilla Unturned\b", "vanilla Returned"),
    (r"\bfor Unturned\b", "for Returned"),
    (r"\binto Unturned\b", "into Returned"),
    (r"\bin Unturned\b", "in Returned"),
    (r"\bto Unturned\b", "to Returned"),
    (r"\bof Unturned\b", "of Returned"),
    (r"\bon Unturned\b", "on Returned"),
    (r"\bas Unturned\b", "as Returned"),
    (r"\bwith Unturned\b", "with Returned"),
    (r"\bover Unturned\b", "over Returned"),
    (r"\bUnturned has\b", "Returned has"),
    (r"\bUnturned used\b", "Returned used"),
    (r"\bUnturned runs\b", "Returned runs"),
    (r"\bUnturned already\b", "Returned already"),
    (r"\bUnturned loads\b", "Returned loads"),
    (r"\bUnturned executes\b", "Returned executes"),
    (r"\bUnturned dedicated servers\b", "Returned dedicated servers"),
    (r"\bUnturned server\b", "Returned server"),
    (r"\bUnturned servers\b", "Returned servers"),
    (r"\bUnturned character\b", "Returned character"),
    (r"\bUnturned does\b", "Returned does"),
    (r"\bUnturned is\b", "Returned is"),
    (r"\bUnturned makes\b", "Returned makes"),
    (r"\bUnturned provides\b", "Returned provides"),
    (r"\bInstalling Unturned\b", "Installing Returned"),
    (r"\bMy Unturned Server\b", "My Returned Server"),
    (r"\bdefault Unturned UI icons\b", "default Returned UI icons"),
    (r"\bcommon Unturned essentials plugins\b", "common essentials plugins"),
    (r"\bUnturned Configuration\b", "Returned Configuration"),
    (r"\bUnturned editor/dev\b", "Returned editor/dev"),
    (r"\bUnturned's editor/dev\b", "Returned's editor/dev"),
]

replacements_final = [
    (r"(?<![\w./-])Unturned(?![\w./-])", "Returned"),
]

changed_files = []
for f in files:
    original = f.read_text(encoding="utf-8")
    text, slots = protect(original)
    new = text
    for pat, repl in replacements:
        new = re.sub(pat, repl, new)
    for pat, repl in replacements_final:
        new = re.sub(pat, repl, new)
    new = unprotect(new, slots)
    if new != original:
        f.write_text(new, encoding="utf-8", newline="\n")
        changed_files.append(str(f.relative_to(root)))

print(f"updated {len(changed_files)} files")
for c in changed_files:
    print(c)

print("\n--- remaining Unturned/unturned mentions ---")
for f in files:
    for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if re.search(r"Unturned|unturned", line):
            print(f"{f.relative_to(root)}:{i}: {line.strip()[:140]}")
