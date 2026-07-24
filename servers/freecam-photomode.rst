.. _doc_returned_freecam_photomode:

Freecam and Photomode
=====================

Returned improves admin freecam for world exploration and content capture. Network interest follows the camera while freecaming (or while a server camera detach / cinematic is active), and Shift+F8 opens freecam camera settings.

Camera-follow streaming
-----------------------

Visual LOD (objects, trees, roads, foliage) already follows the main camera, but networked content — barricades, structures, items, resources, object state, other players, and vehicle replication — is normally centered on the player body.

Returned drives that interest from the freecam / detached camera pose instead:

- Region load radius uses the camera world position while freecam or server camera detach is active.
- Other-player visibility (default 576 m horizontal) and vehicle state distance use the same viewer interest position.
- Bound, navigation, safezone, snow, and related character gameplay checks remain on the body.

Admin freecam and plugin-granted freecam (``sendFreecamAllowed``) both get this behaviour. While detached via :ref:`doc_returned_server_camera_detach`, the server-owned detach pose drives interest without trusting the client.

- Outside freecam/detach, interest stays on the player body as before.
- Zombies stream by navigation **interest bound** (camera while freecamming); quest/body ``bound`` stays on the character.
- Animals are already globally networked.

Photomode settings (Shift+F8)
-----------------------------

While freecam is active (Shift+F1-F5 modes), **Shift+F8** toggles a camera settings panel:

+------------------+------------------------------------------+
| Control          | Effect                                   |
+==================+==========================================+
| Tilt             | Camera roll (+/-180 degrees)             |
+------------------+------------------------------------------+
| Snap buttons     | ``0`` / ``-45`` / ``+45`` / ``90`` deg   |
+------------------+------------------------------------------+
| FOV              | Base vertical field of view              |
+------------------+------------------------------------------+
| Zoom             | Optical zoom multiplier (FOV / zoom)     |
+------------------+------------------------------------------+
| Speed            | Freecam move speed                       |
+------------------+------------------------------------------+
| Exposure         | Post exposure lift in EV (local only)    |
+------------------+------------------------------------------+
| Depth of field   | Focus distance + aperture                |
+------------------+------------------------------------------+
| Freeze time      | Local day-cycle freeze                   |
+------------------+------------------------------------------+
| Time of day      | Scrub the local day cycle (0-24h)        |
+------------------+------------------------------------------+
| Filter           | Grayscale, sepia, cool, warm, contrast,  |
|                  | vignette                                 |
+------------------+------------------------------------------+
| Reset            | Restores defaults                        |
+------------------+------------------------------------------+

Notes:

- Exposure, DoF, filters, and time override are **local client** capture tools. They do not change server lighting for other players.
- Dragging **Time of day** automatically enables freeze.
- Leaving freecam clears zoom, exposure, DoF, filters, and any time override.

Hotkey summary
--------------

Hold **Left Shift**:

- F1 — Orbit / control freecam
- F2 — Tracking
- F3 — Locking
- F4 — Focusing
- F5 — Smoothing
- F6 — Workzone (separate permission)
- F7 — Spectator stats overlay
- F8 — Freecam camera settings (when freecam is active)

See also :ref:`doc_returned_server_camera_detach` for plugin-driven camera poses.
