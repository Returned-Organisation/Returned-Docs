.. _doc_returned_build_tool:

Build Tool
==========

Open **Window → Unturned → Build Tool** in the Unity editor.

This page documents the Returned fork's Build Tool in detail. For mod identity and git policy, see :ref:`doc_returned_development`.

Build section
-------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Button
     - What it does
   * - **Restore Windows 64-bit Target**
     - Switches the active build target back to Windows 64-bit if it was changed.
   * - **Build Standalone Platforms**
     - Exports Windows, macOS, and Linux player builds under ``Builds/Windows64``, ``Builds/OSX64``, ``Builds/Linux64``, etc. Intended for Steam standalone mod distribution.
   * - **Code Documentation**
     - Generates XML docs for plugin/mod developers and copies them into built players.
   * - **Hash**
     - Hashes built assemblies (used by the release pipeline).
   * - **Build Test**
     - Creates a development Windows build at ``Builds/Test/Unturned.exe`` with debug logging and dev tools enabled.
   * - **Build Test (Scripts Only)**
     - Same as Build Test, but only recompiles scripts (faster iteration).
   * - **Build Player Prefab Bundle**
     - Builds the player/character prefab asset bundle into ``Builds/Shared/PlayerPrefabs/``. Required for character models in SDK builds that do not ship those assets in git.

**Build Test** compiles your SDK code into ``Builds/Test/``, then automatically syncs base game assets from your local Steam Unturned install (no Steam login required). The sync overlays the retail install while preserving your compiled ``Unturned.exe``, ``Unturned_Data/Managed/``, and related SDK files. Large folders (``Bundles``, ``Maps``, ``Localization``, etc.) are junctioned back to the Steam install. BattlEye files and locked files are skipped.

After **Build Test**, run the game from:

.. code-block:: text

   Builds/Test/Unturned.exe

Steam section
-------------

These buttons manage Steam-sourced game content for local development:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Button
     - What it does
   * - **Link Retail Game Content (Steam)**
     - Creates junctions from ``Builds/Shared/`` and ``Builds/Test/`` to your Steam Unturned install (``Bundles``, ``Maps``, ``Localization``, etc.). Safe — no multi-GB copy.
   * - **Sync Test Build from Steam Install**
     - Re-runs the Steam sync on ``Builds/Test/`` without a full rebuild. Uses your local Steam Unturned install — no login required. **Build Test** already runs this automatically.
   * - **Restore SDK Unturned_Data (Fix Merge)**
     - Fixes a corrupted test build after a bad retail overlay. Restores SDK scenes from ``Library/PlayerDataCache`` while keeping your compiled ``Managed/`` assemblies.
   * - **Run SteamCmd**
     - Launches SteamCMD for depot/SDK maintenance.
   * - **Update Steam Dedicated Server SDK**
     - Downloads the Steam dedicated-server redistributables used by test/headless builds.

Typical first-time workflow
---------------------------

#. **Build Test** — create ``Builds/Test/Unturned.exe`` (Steam sync + content links + prefab bundle run automatically)
#. Run ``Builds/Test/Unturned.exe``

If assets are missing in ``Builds/Shared/``, click **Link Retail Game Content (Steam)** first. If the game crashes on startup with a corrupted ``level0`` error, click **Restore SDK Unturned_Data (Fix Merge)** then **Build Test (Scripts Only)**.
