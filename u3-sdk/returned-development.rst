.. _doc_returned_development:

Returned Development Guide
==========================

**Returned** is a non-commercial mod fork of the `U3 SDK <https://github.com/SmartlyDressedGames/U3-SDK>`_ for `Unturned <https://store.steampowered.com/app/304930/Unturned/>`_. Use this guide for day-to-day mod development, build workflows, and what belongs in git.

Not affiliated with or endorsed by Smartly Dressed Games.

Git remotes
-----------

.. list-table::
   :header-rows: 1
   :widths: 15 40 45

   * - Remote
     - URL
     - Purpose
   * - ``origin``
     - `Returned-Organisation/Returned <https://github.com/Returned-Organisation/Returned>`_
     - This fork — push your changes here
   * - ``upstream``
     - `SmartlyDressedGames/U3-SDK <https://github.com/SmartlyDressedGames/U3-SDK>`_
     - Official U3 SDK — pull SDK updates from here

.. code-block:: shell

   git clone https://github.com/Returned-Organisation/Returned.git

Prerequisites
-------------

#. Unity **2022.3.62f3** via Unity Hub
#. Steam running with `Unturned <https://store.steampowered.com/app/304930/Unturned/>`_ installed
#. Open ``Assets/GameStartup.unity`` and press Play

Large game assets (bundles, maps, localization, etc.) are loaded from your Steam Unturned install — they are not stored in this repository.

For general Unity setup, refer to :ref:`doc_sdk_unity_project` and :ref:`doc_getting_started`.

Build Tool
----------

Open **Window → Unturned → Build Tool** in the Unity editor. For a full button reference and first-time workflow, see :ref:`doc_returned_build_tool`.

Mod configuration
-----------------

Edit ``Builds/Shared/ModInfo.json`` to set your mod name, version, and description. Server browser filtering uses the ``Name`` field.

``Builds/Shared/Status.json`` is used for status/update metadata in the build pipeline.

``Builds/`` folder and git
--------------------------

The entire ``Builds/`` tree is gitignored **except two files**:

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Tracked in git
     - Purpose
   * - ``Builds/Shared/ModInfo.json``
     - Your mod identity and version
   * - ``Builds/Shared/Status.json``
     - Build/status metadata

Everything else under ``Builds/`` is local output or copied from Steam and must not be committed:

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Path
     - Why it stays local
   * - ``Builds/Test/``
     - Dev game executable and overlaid Steam content
   * - ``Builds/Windows64/``, ``Builds/Linux64/``, etc.
     - Platform export output
   * - ``Builds/Shared/Bundles/``
     - ``core.masterbundle`` and other game bundles from Steam
   * - ``Builds/Shared/Maps/``
     - Map data loaded from Steam
   * - ``Builds/Shared/Localization/``
     - Language files from Steam
   * - ``Builds/Shared/PlayerPrefabs/``
     - Output of **Build Player Prefab Bundle**
   * - ``Builds/Shared/Cloud/``, ``Worlds/``, ``Logs/``
     - Local saves and runtime data

The upstream SDK also documents selective map allowlisting in ``.gitignore``; this fork uses a stricter allowlist and only tracks the two JSON files above.

Licensed third-party content
----------------------------

Do not commit packages or generated integration files for assets that require a separate license. See ``.gitignore`` and ``THIRDPARTYNOTICES.txt``.

Notable examples:

* **A\* Pathfinding Project** — install locally; integration stubs ship in source
* **Highlighting System plugin** — install locally if licensed
* **Unity Standard Assets** — water/reflection enhancements
* **BattlEye** — not included in the SDK

Returned fork features
----------------------

* **Counter animal behaviour** — new ``Behaviour Counter`` AI type. Animals ignore players until damaged, then attack the attacker. See :ref:`doc_data_eanimalbehaviour` and :ref:`doc_assets_animal`.
* **Physics props** — bouncy, resettable objects with per-source push rules. See :ref:`doc_physics_prop_example`.

License reminder
----------------

Mod development under the U3 SDK License is **non-commercial**. Include ``LICENSE.txt`` and ``THIRDPARTYNOTICES.txt`` with any distribution. See the :ref:`doc_sdk_faq`.
