.. _doc_plugins:
.. _doc_returned:

Plugins & Modules
=================

This section documents server-side C# APIs for plugins and modules running on a Returned dedicated server or listen server. Use these pages when you need to call Returned APIs from Rocket, OpenMod, or a custom module.

For workshop content (items, vehicles, maps, NPCs), use the Creating Items, Creating Vehicles, Mapping, and related sections in the sidebar instead.

Getting started with plugins
----------------------------

- :ref:`doc_servers_rocket` — RocketMod plugins
- :ref:`doc_servers_openmod` — OpenMod plugins
- :ref:`doc_glazier` — UI toolkit used by server-sent UI

Plugin APIs
-----------

- :ref:`doc_returned_custom_item_text` — override display name and description on a specific inventory item instance
- :ref:`doc_returned_custom_map_images` — per-player satellite/chart image overrides
- :ref:`doc_returned_custom_plugin_map_markers` — per-player map pins separate from the player's group marker
- :ref:`doc_returned_ui_effect_transforms` — duplicate, move, and resize UI effect elements
- :ref:`doc_returned_server_sent_ui` — Glazier-backed widgets from the server (buttons, labels, fields, images)
- :ref:`doc_returned_interaction_menu` — hold-C category radial (Emotes / Faces / plugin entries); unavailable under ``-LegacyUIs``
- :ref:`doc_returned_server_camera_detach` — force camera pose and cinematic start/end locks
- :ref:`doc_returned_dashboard_open_hooks` — cancel inventory / crafting / skills / map tab opens
- :ref:`doc_returned_plugin_hotkey_query` — query client plugin hotkey ``KeyCode`` bindings

Related server features
-----------------------

These are documented under Servers & Programming or Mapping rather than as plugin APIs:

- :ref:`doc_returned_admin_commands` — native cheats-gated admin commands
- :ref:`doc_returned_character_body_generation` — V1/V2 character body (``Config.txt`` / Appearance)
- :ref:`doc_returned_freecam_photomode` — admin freecam camera-follow streaming and Shift+F8 settings
- :ref:`doc_returned_player_custom_map_markers` — personal multi-marker placement on the dashboard map
