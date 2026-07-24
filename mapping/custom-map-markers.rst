.. _doc_returned_custom_map_markers:

Custom Map Markers
==================

Returned adds **level-authored map markers** with categories, icons, and an in-game legend. You can mark shops, gun stores, and other points of interest on the dashboard map without editing or re-uploading ``Map.png``.

Overview
--------

The workflow has two parts:

1. **Categories** — define marker types once (name, color, icon).
2. **Markers** — place nodes in the level editor and assign a category.

Players open the information dashboard map and use the **marker legend** to show or hide each category (for example, all gun stores at once).

Category files
--------------

Categories are saved in the level folder:

.. code-block:: text

	{level}/MapMarkers/Categories.dat
	{level}/MapMarkers/*.png

``Categories.dat`` stores category id, display name, color, and icon settings. Custom icon PNGs live in the ``MapMarkers`` folder next to that file.

Define categories in the editor
-------------------------------

1. Open the level in the editor.
2. Go to **Environment → Nodes**.
3. Click **Marker Categories**.
4. Add categories and set:

   - **Id** — stable key (for example ``gun_stores``).
   - **Display Name** — legend label (for example ``Gun Stores``).
   - **Color** — tint for the icon and legend swatch.
   - **Icon** — built-in icon or custom PNG path relative to ``MapMarkers/``.

5. Save the level (**Ctrl+S** or pause menu **Save**). Category edits auto-save to ``MapMarkers/Categories.dat``, but placed marker nodes are stored in ``Level.hierarchy`` and need a full level save.

Built-in icons
--------------

The category editor lists **all default Returned UI icons** from the core game bundle (menu icons, dashboard icons, HUD icons, and similar). Use the search field to filter the list, then click an icon to assign it to the selected category.

Icons are stored as a game path such as ``UI/Player/Icons/PlayerDashboardInformation/Marker``.

For **Custom PNG**, enter a path such as ``gun_store.png``. The file must exist at ``{level}/MapMarkers/gun_store.png``.

Place markers
-------------

1. In **Environment → Nodes**, click **Map Marker** on the right.
2. Click the terrain in the 3D view, then press **E** to place a marker.
3. Select the marker and set:

   - **Use category** — disable for fixed labels such as city or town names. These markers are always shown on the map and do not appear in the legend.
   - **Category** — pick from your level categories (only when **Use category** is enabled).
   - **Label** — optional text shown on the map (centered on the marker when the icon is hidden).
   - **Visible on map** — whether the marker appears on the dashboard map.
   - **Show icon** — whether the category icon is drawn. Disable for label-only markers.

4. Save the level (**Ctrl+S** or pause menu **Save**). Category edits auto-save to ``MapMarkers/Categories.dat``, but placed marker nodes are stored in ``Level.hierarchy`` and need a full level save.

Uncategorized markers
---------------------

Disable **Use category** when a marker should not be grouped in the legend. This is useful for:

- City, town, or region names
- Fixed labels that players should always see
- Text that should not be hidden when a category toggle is turned off

Uncategorized markers still respect **Visible on map** and **Show icon**. They use the default pin icon when **Show icon** is enabled. For name-only markers, disable **Show icon** and set **Label**.

In-game legend
--------------

When a player opens the information dashboard map:

- Authored markers appear as tinted icons on the satellite/chart view.
- The **marker legend** lists each category that has at least one marker on the map.
- Each category has a toggle to show or hide all markers in that category.
- Toggle state is saved per level on the client.

Legend visibility does not replace group waypoint markers or named location text labels. Those use the existing map controls.

Plugin markers from server code are separate from both systems. See :ref:`doc_returned_custom_plugin_map_markers`.

Personal multi-markers placed by players are documented in :ref:`doc_returned_player_custom_map_markers`.

Custom icons tips
-----------------

- Use small PNGs (for example 32×32 or 64×64) with transparency.
- White or light icons tint best with the category color.
- If a custom PNG is missing, the map falls back to the default pin icon.

Related
-------

- :ref:`doc_returned_custom_plugin_map_markers` — per-player server plugin markers (name, color, position).
- :ref:`doc_mapping_charts` — chart rendering colors (separate from marker icons).
- :ref:`doc_returned_custom_map_images` — server-sent map image overrides (background texture only).
