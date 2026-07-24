.. _doc_returned_custom_map_images:

Custom Map Images
=================

Returned lets a server replace the satellite and chart images shown in a player's **Information** tab. Plugins can push a remote URL, a PNG or JPG file from the server, or raw image bytes. The client displays the override instead of the level's ``Map.png`` and ``Chart.png`` files.

Overview
--------

The information dashboard normally loads map textures from the current level:

- **Satellite** view uses ``Map.png`` from the level folder.
- **Chart** view uses ``Chart.png`` from the level folder.

``CustomMapManager`` lets the server override either view per player. Overrides persist for the session and are re-sent when the player reconnects to the same server.

The client still applies the normal gameplay gates:

- Satellite view requires a GPS (or mode config that grants map access).
- Chart view requires a chart item (or mode config that grants chart access).
- Blindfolded players cannot see the real map image.

Clearing an override restores the level's default textures.

Delivery methods
----------------

Returned supports three ways to set a custom map image:

URL
``````````````

Remote clients download the image over HTTP or HTTPS, similar to other web images in Returned.

Server-local file
`````````````````

The server reads a ``.png`` or ``.jpg`` file from disk and sends the image bytes to the client. This is the recommended way to use PNG files bundled with a plugin or module folder.

Raw bytes
`````````

The server sends PNG or JPG bytes directly. Use this when your plugin already has the image in memory.

Server API
----------

All methods are on ``CustomMapManager`` and must be called on the server.

Set a satellite map URL:

.. code-block:: cs

	CustomMapManager.sendMapUrl(player, "https://example.com/maps/event-satellite.png");

Set a chart map URL:

.. code-block:: cs

	CustomMapManager.sendChartUrl(player, "https://example.com/maps/event-chart.png");

Set the same URL for every connected player:

.. code-block:: cs

	CustomMapManager.sendMapUrlToAll(isChart: false, url);

Send a server-local image file:

.. code-block:: cs

	string mapPath = @"C:\Returned\Modules\MyPlugin\Maps\custom-map.png";
	CustomMapManager.sendMapFile(player, mapPath);
	CustomMapManager.sendChartFile(player, @"C:\Returned\Modules\MyPlugin\Maps\custom-chart.png");

Send raw image bytes:

.. code-block:: cs

	byte[] pngBytes = File.ReadAllBytes(mapPath);
	CustomMapManager.sendMapImageData(player, isChart: false, pngBytes);

Clear overrides:

.. code-block:: cs

	CustomMapManager.clearMapUrl(player, isChart: false);
	CustomMapManager.clearMapUrl(player, isChart: true);
	CustomMapManager.clearAll(player);

``sendMapUrl`` also accepts a server-local file path. If the string exists on the server's filesystem, Returned sends the file bytes instead of treating the string as a web URL.

Bundled plugin PNGs
-------------------

Plugins can ship PNG files inside their module directory and reference them with an absolute path on the dedicated server:

.. code-block:: cs

	string pluginMapPath = Path.Combine(moduleDirectory, "Assets", "event-map.png");
	CustomMapManager.sendMapFile(player, pluginMapPath);

Remote clients do not need a copy of the file. The server reads the PNG and transfers the bytes to each targeted player.

Keep image files reasonably small. The current network limit is **65535 bytes** per image payload. If an image is too large, Returned logs a warning and does not send it.

Recommendations:

- Use PNG or JPG compression suited for map screenshots.
- Prefer ``sendMapFile`` or ``sendMapImageData`` for bundled assets.
- Use ``sendMapUrl`` when the image is hosted on a CDN or your own web server.

Client behaviour
----------------

When an override is active, the information tab prefers the custom texture over the level default. If a URL-based image is still downloading, the client shows the level map until the download finishes.

Overrides are cleared automatically when:

- The player disconnects.
- The level unloads.
- The server clears the override.

Example
-------

Show an event map to every connected player from a bundled PNG:

.. code-block:: cs

	void ShowEventMap(string mapFilePath)
	{
		foreach (SteamPlayer client in Provider.clients)
		{
			if (client?.player == null)
			{
				continue;
			}

			CustomMapManager.sendMapFile(client.player, mapFilePath);
		}
	}

Switch back to the normal level map when the event ends:

.. code-block:: cs

	void ClearEventMap()
	{
		CustomMapManager.sendMapUrlToAll(isChart: false, null);
	}

Limitations
-----------

- Image payloads are limited to 65535 bytes in the current Returned version.
- Overrides apply to the information dashboard map image only. They do not replace level files on disk or affect other map UI such as quest markers.
- URL delivery requires web requests to be allowed on the client. Players using ``-NoWebRequests`` cannot download remote map URLs.
- Chart and satellite overrides are independent. Set both if you need to replace both views.
