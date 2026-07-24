.. _doc_returned_player_custom_map_markers:

Player Custom Map Markers
=========================

Returned integrates [Snippy420/Custom-Markers](https://github.com/Snippy420/Custom-Markers) personal map markers. Players can place multiple private waypoints on the dashboard map, rename them, recolor them, and remove them. These markers are separate from the single **group waypoint** shared with group members.

Overview
--------

Personal custom markers:

- Are placed by **right-clicking** the dashboard map.
- Belong only to the placing player.
- Persist in ``Quests.dat`` (save version 12).
- Use the **Show Markers** client toggle.

Group waypoint markers:

- Are the vanilla shared marker for you and your group.
- Still set through normal gameplay (for example scope marking).
- Use the separate **Group Markers** client toggle.

Server plugin markers via ``CustomPluginMapMarkerManager`` are a third system. See :ref:`doc_returned_custom_plugin_map_markers`.

Placing and editing markers
---------------------------

1. Open the information dashboard map with GPS access.
2. **Right-click** the map to place a new marker. The rename / color editor opens automatically.
3. **Left-click** an existing marker to open the editor again.
4. **Right-click** an existing marker to remove it.

Admins (and players granted permission by a plugin) also see a **Teleport** button in the marker editor. Teleport moves the player to ground level at the marker's map position while keeping their current yaw.

Label length is limited to **32** characters.

Server limit
------------

Set the per-player placement cap in ``Config.json`` under ``Gameplay``:

.. code-block:: json

	"Max_Player_Custom_Markers": 10

- **Default:** ``10``
- **``0``:** disables right-click placement (existing saved markers still load and remain editable)
- Plugins calling ``PlayerQuests.ServerSetCustomMarker`` are **not** limited by this value

Map toggles
-----------

When the map is visible, the map footer shows:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Toggle
     - Controls
   * - Show Markers
     - Personal custom markers placed by the player (independent of ``Group_Map``)
   * - Group Markers
     - Shared group waypoint pins for you and group members (requires ``Group_Map``)
   * - Show marker legend
     - Level-authored POI categories (see :ref:`doc_returned_custom_map_markers`)

``Group_Map`` still hides group waypoints, remote player dots, and the local player pin on Hard / when disabled. Personal markers keep working.
Plugin API
----------

Server-side methods on ``PlayerQuests`` for the **owning player only**:

.. code-block:: cs

	player.quests.ServerSetCustomMarker(
		markerId: 100,
		position: new Vector3(120f, 32f, -80f),
		text: "Objective A",
		color: Color.cyan
	);

	player.quests.ServerRemoveCustomMarker(100);
	player.quests.ServerClearCustomMarkers();

Read markers on the server with ``player.quests.customMarkers``.

Marker teleport
---------------

Server admins can teleport to their own personal markers from the marker editor without any plugin setup.

Plugins can grant or revoke teleport access for non-admin players with ``CustomMapMarkerTeleportManager.setTeleportAllowed``. When allowed, the client shows the **Teleport** button in the personal marker editor.

Cancel or modify teleports with ``CustomMapMarkerTeleportManager.onTeleportRequested``. Set ``shouldAllow`` to ``false`` to block a teleport after the server has validated permission and marker ownership.

.. code-block:: cs

	using SDG.Unturned;
	using UnityEngine;

	// Grant a player teleport access (in addition to admins).
	CustomMapMarkerTeleportManager.setTeleportAllowed(player, allowed: true);

	// Revoke plugin-granted access.
	CustomMapMarkerTeleportManager.setTeleportAllowed(player, allowed: false);

	CustomMapMarkerTeleportManager.onTeleportRequested += (
		Player teleportingPlayer,
		uint markerId,
		Vector3 position,
		ref bool shouldAllow) =>
	{
		if (teleportingPlayer.life.isDead)
		{
			shouldAllow = false;
		}
	};

Teleport requests are rate-limited on the server. The player must own the marker id being teleported to. The server raycasts from the sky to ground (same as ``/tp waypoint``) because map placement stores horizontal coordinates only.

Related
-------

- :ref:`doc_returned_custom_map_markers` — level editor POI markers and legend
- :ref:`doc_returned_custom_plugin_map_markers` — per-player server plugin pins
- :ref:`doc_server_hosting` — ``Group_Map`` and other gameplay config
