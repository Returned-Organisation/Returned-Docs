.. _doc_returned_admin_commands:

Admin Commands
==============

Returned ships a set of native server admin commands inspired by common essentials plugins. They are built into the game executable and do not require Rocket or other plugins.

Requirements
------------

- The server must have **cheats enabled** (``Provider.hasCheats``). Use the vanilla ``cheats`` command if needed.
- In-game callers must be a **Steam admin** on dedicated servers. The existing chat command gate in ``ChatManager.process`` applies.
- The dedicated server console can run these commands without Steam admin, but most player-targeting commands require a player name when run from console.

Console usage generally prefixes the target player name before other arguments. For example: ``heal PlayerName`` or ``tphere TargetPlayer DestinationPlayer``.

Player Commands
---------------

.. list-table::
   :header-rows: 1

   * - Command
     - Usage
     - Description
   * - ``clearinventory``
     - ``clearinventory [player|*]``
     - Clears inventory pages and unequips clothing. ``*`` clears everyone.
   * - ``checkowner``
     - ``checkowner``
     - Prints the owner SteamID of the barricade, structure, or vehicle you are looking at. In-game only.
   * - ``zombieignore``
     - ``zombieignore [player]``
     - Toggles zombie aggro on the target player.
   * - ``fly``
     - ``fly [player]``
     - Toggles Returned editor/dev fly (``enableFly``).
   * - ``freeze``
     - ``freeze [player|*]``
     - Toggles movement freeze. ``*`` freezes everyone.
   * - ``maxskills``
     - ``maxskills [player|*]``
     - Maxes all skills. ``*`` applies to everyone.
   * - ``position``
     - ``position [player]``
     - Prints world coordinates for the target player.
   * - ``repair``
     - ``repair [player]``
     - Sets all inventory item quality to 100%.
   * - ``repairvehicle``
     - ``repairvehicle [player|all]``
     - Repairs the target player's current vehicle, or all vehicles when ``all`` is specified.
   * - ``heal``
     - ``heal [player|*]``
     - Restores health, food, water, virus, stamina, bleeding, and broken bones.
   * - ``god``
     - ``god [player]``
     - Toggles god mode: damage immunity, infinite stamina, and no hunger, thirst, oxygen drain, radiation, or broken legs. Enabling refills vitals.
   * - ``effect``
     - ``effect <effect-id-or-guid> [player]``
     - Triggers a **world** effect at the target player. This is separate from the vanilla ``effectui`` UI command.
   * - ``tp``
     - ``tp <player|place|x y z>`` or ``tp <player> <player|place|x y z>``
     - Teleports to a player, devkit location name, or coordinates. Separate from vanilla ``teleport``.
   * - ``tphere``
     - ``tphere <player>`` (in-game) or ``tphere <player> <destination>`` (console)
     - Teleports the target player to you, or to another player from console.

World Commands
--------------

.. list-table::
   :header-rows: 1

   * - Command
     - Usage
     - Description
   * - ``broadcast``
     - ``broadcast <message>``
     - Sends a server-colored message to all players.
   * - ``respawnanimals``
     - ``respawnanimals``
     - Respawns all dead animals at their pack spawn points.
   * - ``respawnitems``
     - ``respawnitems``
     - Drops items from all level item spawnpoints.
   * - ``respawnvehicles``
     - ``respawnvehicles``
     - Destroys dead empty vehicles and spawns replacements at level vehicle spawn points.
   * - ``respawnzombies``
     - ``respawnzombies``
     - Respawns all dead zombies at spawn points in their navmesh region.

Notes
-----

- **Fly** uses the same ``enableFly`` toggle as Returned's editor/dev chat ``fly`` command (active in ``UNITY_EDITOR`` / ``DEVELOPMENT_BUILD``). Movement follows the camera; hold **Sprint** for a speed boost.
- **Freeze** uses ``sendPluginSpeedMultiplier(0)`` and is independent of cinematic camera movement lock.
- **Zombie ignore** prevents new alerts and clears active hunts when enabled.
- Existing vanilla commands such as ``teleport``, ``say``, and ``effectui`` are unchanged.
