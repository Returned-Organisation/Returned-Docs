.. _doc_returned_custom_plugin_map_markers:

Custom Plugin Map Markers
=========================

Returned lets a server show custom markers on a player's **Information** tab map without replacing the player's own group marker. Plugins can set marker name, color, and world position per player. Multiple markers are supported and identified by a string id.

Overview
--------

Players can place their own map marker through normal gameplay (group marker). That marker uses ``PlayerQuests.replicateSetMarker`` and appears alongside group members.

``CustomPluginMapMarkerManager`` is a separate system:

- Markers are server-authored and synced per player.
- They do not change or clear the player's quest/group marker.
- They appear on the dashboard map whenever the player can see the map (GPS or mode config).
- They are not hidden by the **Show markers** toggle, which only controls player and group markers.

Use plugin map markers when you need to guide a specific player to a location (quest objectives, waypoints, event pings) without taking over their personal marker slot. Use :ref:`level editor map markers <doc_returned_custom_map_markers>` when the point of interest is fixed for everyone on the map.

Markers persist for the session and are re-sent when the player reconnects to the same server.

Marker data
-----------

Each marker is a ``PluginMapMarker`` with these fields:

- ``id`` — stable key used to update or remove the marker.
- ``label`` — text shown beside the pin on the map. Optional.
- ``position`` — world-space ``Vector3`` on the level.
- ``color`` — ``Color32`` tint for the pin icon.

When to use which API
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - System
     - Who sets it
     - Overrides player marker?
   * - Quest / group marker
     - Player (or plugin via ``PlayerQuests``)
     - Yes — one shared marker slot
   * - Level editor POI markers
     - Mapper in the editor
     - No
   * - ``CustomPluginMapMarkerManager``
     - Server plugin
     - No

Server API
----------

All methods are on ``CustomPluginMapMarkerManager`` and must be called on the server.

Set or update a marker
``````````````````````

``sendMarker`` returns ``true`` when the marker was accepted and sent. It returns ``false`` when called off-server, when ``player`` is null, when ``id`` is empty or too long, or when the player already has 64 markers and ``id`` is new.

.. code-block:: cs

	using SDG.Unturned;
	using UnityEngine;

	CustomPluginMapMarkerManager.sendMarker(
		player,
		id: "quest_dropoff",
		label: "Drop Off Supplies",
		color: Color.yellow,
		position: new Vector3(100f, 32f, -200f)
	);

Calling ``sendMarker`` again with the same ``id`` updates that marker in place.

Remove one marker
`````````````````

``removeMarker`` returns ``true`` when a marker with that id existed and was removed.

.. code-block:: cs

	CustomPluginMapMarkerManager.removeMarker(player, "quest_dropoff");

Clear all plugin markers
````````````````````````

.. code-block:: cs

	CustomPluginMapMarkerManager.clearAll(player);

Clear plugin markers when a player disconnects, finishes a quest chain, or leaves an event so stale pins do not carry over.

Limits
------

- Up to **64** markers per player (``MAX_MARKERS_PER_PLAYER``).
- Marker id: up to **64** characters (trimmed). Required and used as the update key.
- Label: up to **64** characters (trimmed). Optional; pass an empty string for icon-only markers.

Client behaviour
----------------

When the server updates a player's markers, the client redraws plugin pins on the information dashboard map. Each pin uses the default map marker icon tinted with your chosen color. If ``label`` is not empty, the text appears to the right of the pin.

The client still applies the normal map visibility gates:

- Satellite view requires a GPS (or mode config that grants map access).
- Blindfolded players cannot see the real map image.

Plugin markers are drawn in a separate overlay from player/group markers and from level-authored POI markers. They remain visible even when **Show markers** is disabled.

Overrides are cleared automatically when:

- The player disconnects.
- The level unloads.
- The server calls ``removeMarker`` or ``clearAll``.

Client read API
---------------

Plugins that need to react on the client can read the local player's synced markers:

.. code-block:: cs

	foreach (PluginMapMarker marker in CustomPluginMapMarkerManager.getClientMarkers())
	{
		// marker.id, marker.label, marker.position, marker.color
	}

Subscribe to ``CustomPluginMapMarkerManager.onClientMarkersChanged`` when your UI should refresh after the server updates markers.

Example
-------

Guide a player through a two-step quest without touching their group marker:

.. code-block:: cs

	void StartQuest(Player player, Vector3 pickup, Vector3 dropoff)
	{
		CustomPluginMapMarkerManager.sendMarker(
			player,
			id: "quest_pickup",
			label: "Pick Up Package",
			color: Color.cyan,
			position: pickup
		);

		CustomPluginMapMarkerManager.sendMarker(
			player,
			id: "quest_dropoff",
			label: "Deliver Package",
			color: Color.yellow,
			position: dropoff
		);
	}

	void OnPackageCollected(Player player)
	{
		CustomPluginMapMarkerManager.removeMarker(player, "quest_pickup");
	}

	void OnQuestComplete(Player player)
	{
		CustomPluginMapMarkerManager.clearAll(player);
	}

Limitations
-----------

- Markers are session-only. They are not written to player save files.
- Each player has their own marker list. There is no broadcast-to-all helper; loop ``Provider.clients`` if you need the same marker on every player.
- Plugin markers do not appear on the chart view's named location labels or the level editor legend. They are dashboard-map pins only.
- Do not use ``PlayerQuests.replicateSetMarker`` for plugin waypoints if you want to keep the player's own marker independent.
- Personal player markers (right-click placement) use ``PlayerQuests.ServerSetCustomMarker`` instead. See :ref:`doc_returned_player_custom_map_markers`.

Related
-------

- :ref:`doc_returned_custom_map_markers` — level-authored POI markers with categories and a per-category legend.
- :ref:`doc_returned_custom_map_images` — server-sent map image overrides (background texture only).
