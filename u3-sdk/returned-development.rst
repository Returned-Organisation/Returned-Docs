.. _doc_returned_development:

Returned Development Guide
==========================

*Returned* is a non-commercial mod fork of the `U3 SDK <https://github.com/SmartlyDressedGames/U3-SDK>`_ for `Unturned <https://store.steampowered.com/app/304930/>`_. Use this guide for day-to-day mod development, build workflows, and what belongs in git.

.. note::

	Returned is not affiliated with or endorsed by Smartly Dressed Games.

Git Remotes
-----------

This fork uses two remotes:

- **origin** — `Returned-Organisation/Returned <https://github.com/Returned-Organisation/Returned>`_. Push your changes here.
- **upstream** — `SmartlyDressedGames/U3-SDK <https://github.com/SmartlyDressedGames/U3-SDK>`_. Pull official SDK updates from here.

If you have the Git CLI installed, you can clone the fork with this command:

.. code-block:: shell

	git clone https://github.com/Returned-Organisation/Returned.git

Prerequisites
-------------

You'll need the same version of the Unity editor as described in :ref:`doc_getting_started:installing_unity`. For Returned, this is currently version **2022.3.62f3**.

Steam needs to be running, and `Unturned <https://store.steampowered.com/app/304930/>`_ must be installed. Large game assets (bundles, maps, localization, etc.) are loaded from your Steam Unturned install — they are not stored in this repository.

To run the game in the editor, open the ``Assets/GameStartup.unity`` scene and click Play.

For general Unity setup, refer to :ref:`doc_sdk_unity_project` and :ref:`doc_getting_started`.

Build Tool
----------

Open **Window > Unturned > Build Tool** in the Unity editor. For a full button reference and first-time workflow, see :ref:`doc_returned_build_tool`.

Mod Configuration
-----------------

Edit ``Builds/Shared/ModInfo.json`` to set your mod name, version, and description. Server browser filtering uses the ``Name`` field.

``Builds/Shared/Status.json`` is used for status/update metadata in the build pipeline.

``Builds/`` Folder and Git
--------------------------

The entire ``Builds/`` tree is gitignored **except** ``Builds/Shared/ModInfo.json`` and ``Builds/Shared/Status.json``. Those two JSON files track your mod identity and build metadata.

Everything else under ``Builds/`` is local output or copied from Steam and must not be committed. This includes ``Builds/Test/`` (the dev executable and overlaid Steam content), platform export folders such as ``Builds/Windows64/`` and ``Builds/Linux64/``, and Steam-sourced folders like ``Builds/Shared/Bundles/``, ``Builds/Shared/Maps/``, and ``Builds/Shared/Localization/``.

The upstream SDK also documents selective map allowlisting in ``.gitignore``; this fork uses a stricter allowlist and only tracks the two JSON files above.

Licensed Third-Party Content
----------------------------

Do not commit packages or generated integration files for assets that require a separate license. See ``.gitignore`` and ``THIRDPARTYNOTICES.txt``.

Notable examples include the **A\* Pathfinding Project** (install locally; integration stubs ship in source), the **Highlighting System plugin** (install locally if licensed), **Unity Standard Assets** (water/reflection enhancements), and **BattlEye** (not included in the SDK).

Returned Fork Features
----------------------

Returned adds documentation for features that are not yet available in the official game:

- **Counter animal behaviour** — a new ``Behaviour Counter`` AI type. Animals ignore players until damaged, then attack the attacker. See :ref:`doc_data_eanimalbehaviour` and :ref:`doc_assets_animal`.
- **Physics props** — bouncy, resettable objects with per-source push rules. See :ref:`doc_physics_prop_example` and :ref:`doc_assets_object`.
- **Vehicle platform riding** — players can stand on moving vehicle surfaces in multiplayer. See :ref:`doc_vehicle_platform_riding`.

License Reminder
----------------

Mod development under the U3 SDK License is **non-commercial**. Include ``LICENSE.txt`` and ``THIRDPARTYNOTICES.txt`` with any distribution. See the :ref:`doc_sdk_faq`.
