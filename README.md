Returned Documentation
======================

These are the source files for *Returned*'s modding documentation.

*Returned* is a non-commercial mod of [Unturned](https://smartlydressedgames.com/unturned/). Not affiliated with or endorsed by Smartly Dressed Games.

The built documentation is hosted by [Read the Docs](https://readthedocs.org/) here: https://returned-docs.readthedocs.io/

This repository is based on [SmartlyDressedGames/Unturned-Docs](https://github.com/SmartlyDressedGames/Unturned-Docs). It covers workshop modding (items, vehicles, maps, NPCs) and Returned server plugin / module APIs.

Offline Downloads
-----------------

PDF and ePub versions of the documentation can be [downloaded](https://readthedocs.org/projects/returned-docs/downloads/) for offline use.

Contributing
------------

Anyone can contribute towards *Returned*'s modding documentation. This repository has two branches – **latest** and **stable** – although contributions should only be made towards the "latest" branch.

- **latest**: Always has the latest documentation, including upcoming features that might not be available in the current version.

- **stable**: Occasionally updated with the additions to the "latest" branch.

The online documentation pages are generated from .rst (reStructuredText) files. These files are stored in root, but are organized into folders based on where those files appear in the table of contents. For example, the [level-asset.rst](/assets/level-asset.rst) file is located in the "assets" folder.

### Styleguide

Most documentation files are formatted similarly. Some important notes:

- Content block directives can be used to add notes, warnings, tips, and other admonitions.

- Internal links should use the `:ref:` command, usually pointing towards a custom anchor.

- Properties in the asset manual pages use one of two formats. Older pages follow a `**Name** *data type*: Description` format. Depending on the data type, it may be hyperlinked instead, or may include required (or possible) values. Newer pages follow a table-based format. These formats should not be mixed on the same page, but continuing to use the legacy format on pages that have not been converted yet is acceptable.

- Images from the Unity editor should crop out any unnecessary information. This usually includes the Title Bar (which includes details such as the Unity version, project name, and window buttons), and the Toolbar.

- The `code-block` directive can be used to display example code with syntax highlighting. Common languages include `cs`, `json`, `text`, `shell`, `bat`, and `unturneddat` (alias: `unturnedasset`).

- Including links to the [Unturned Wiki](https://unturned.wiki.gg/) can be helpful. Wiki articles linked in the Returned Documentation should have the "[Category:Pages linked from Unturned Documentation](https://unturned.wiki/wiki/Category:Pages_linked_from_Unturned_Documentation)" hidden tracking category added to them.

Building the Docs
-----------------

This section explains how to build a local copy of the documentation. Our documentation is written in [reStructuredText](https://www.writethedocs.org/guide/writing/reStructuredText/) and converted to HTML through [Sphinx](https://github.com/sphinx-doc/sphinx).

We recommend using [Visual Studio Code](https://code.visualstudio.com/) with the [reStructuredText extension](https://docs.restructuredtext.net/) (by LeXtudio Inc.), and the [Esbonio extension](https://docs.esbon.io/en/latest/index.html) (by Swyddfa) to benefit from live preview and syntax highlighting.

Use the same version of Python as configured in `.readthedocs.yaml`. If you have multiple Python versions installed, you may need to manually specify the Python Interpreter that should be used.

1. Clone the Returned Docs repository:

	```shell
	git clone https://github.com/Returned-Organisation/Returned-Docs.git
	```

2. Change directory to the Returned Docs repository:

	```shell
	cd Returned-Docs
	```

3. *(Optional)* Set up a virtual environment. Virtual environments prevent potential conflicts between the Python packages installed in `requirements.txt` and any Python packages installed on your system.

	1. Create the virtual environment:

		```shell
		py -3.12 -m venv .venv
		```

	2. Activate the virtual environment:

		```shell
		.\.venv\Scripts\Activate.ps1
		```

	3. Your terminal prompt will show `(venv)` at the beginning if activation worked.

4. Download packages from `requirements.txt`:

	```shell
	pip install -r requirements.txt
	```

	Alternatively, `pip-sync` can be used to ensure installed packages are *exactly* the same – by adding, upgrading, or removing any packages as necessary. **Doing this outside of the virtual environment is not recommended:**

	```shell
	pip-sync requirements.txt
	```

5. Build the documentation:

	```shell
	.\make html
	```

	Alternatively, you can build the documentation by running `sphinx-build` manually. This command is more cross-platform:

	```shell
	sphinx-build -b html ./ _build/html
	```

You can now browse the documentation by opening `.../Returned-Docs/_build/html/index.html` in your web browser. If Esbonio was installed, you can also preview the documentation in Visual Studio Code.

Configure Esbonio for a virtual environment
---------------------------------------------

Esbonio v1.0.0 in a virtual environment on Windows may fail to import packages from the venv and instead used Esbonio's bundled Python environment. This causes misleading `ModuleNotFoundError` errors to appear for packages installed in the virtual environment.

You can force Esbonio to use the virtual environment by configuring your `.vscode/settings.json`:

```json
{
	"esbonio.sphinx.pythonCommand": {
		"command": ["${venv:.venv}"]
	}
}
```

Updating the `requirements.txt` file
------------------------------------

Packages (including specific versions) can be pinned in `requirements.in`. This file is used to automatically generate `requirements.txt`.

Run the following command to generate a new `requirements.txt` file afterwards:

```shell
pip-compile requirements.in
```

Locally updating the TOC
------------------------

Sometimes, the Table of Contents will fail to update after changes have been made. This is an issue with the Esbonio extension, but it can be safely ignored as it should only affect your local preview of the project pages.

If needed, you can force Esbonio to rebuild these pages. Delete the files at `%APPDATA%\Code\User\workspaceStorage\...\swyddfa.esbonio\sphinx`, run `make html`, and restart the Sphinx language server (e.g., by closing and reopening Visual Studio Code, or by clicking the "Sphinx" button in the bottom-right).

Syncing Upstream Documentation
------------------------------

Returned Docs is based on [SmartlyDressedGames/Unturned-Docs](https://github.com/SmartlyDressedGames/Unturned-Docs). To pull upstream documentation updates:

```shell
git fetch upstream
git merge upstream/latest
```

The `upstream` remote should point at `https://github.com/SmartlyDressedGames/Unturned-Docs.git`.
