.. _doc_returned_server_sent_ui:

Server Sent UI
==============

Returned lets server plugins create HUD widgets in code. The owning client builds each widget with the player's active :ref:`Glazier <doc_glazier>` backend (IMGUI, uGUI, or UIToolkit), instead of spawning a uGUI ``EffectAsset`` prefab.

Overview
--------

Keyed UI effects (``EffectManager.SendUIEffect`` and related APIs) still work and still use uGUI prefabs. Prefer **Server Sent UI** when you need the UI to follow the player's Glazier setting, or when you want to describe widgets in code rather than author a Canvas prefab.

Widgets are parented under a fullscreen display root on ``PlayerUI``. They are not inserted into vanilla menus such as inventory or the map.

When the UI needs a mouse cursor, enable ``EPluginWidgetFlags.Modal`` on the player (the same flag used by other plugin UIs). Server Sent UI does not invent a separate modal flag.

Quick start
-----------

.. code-block:: cs

	player.enablePluginWidgetFlag(EPluginWidgetFlags.Modal);

	ServerUIButton button = ServerUI.CreateButton(player);
	button.Text = "Hello";
	button.SizeOffset_X = 200f;
	button.SizeOffset_Y = 30f;
	button.PositionScale_X = 0.5f;
	button.PositionScale_Y = 0.5f;
	button.PositionOffset_X = -100f;
	button.PositionOffset_Y = -15f;
	button.OnClicked += clicked =>
	{
		// Server-side click handler
	};

	// Later:
	ServerUI.DestroyAll(player);
	player.disablePluginWidgetFlag(EPluginWidgetFlags.Modal);

Factory methods
---------------

- ``ServerUI.CreateFrame(player)``
- ``ServerUI.CreateBox(player)``
- ``ServerUI.CreateLabel(player)``
- ``ServerUI.CreateButton(player)``
- ``ServerUI.CreateField(player)`` — string input; submits on Enter
- ``ServerUI.CreateImage(player)`` — texture from a web URL or PNG/JPG bytes, or a live render (icon / entity / character)
- ``ServerUI.CreateSlider(player)`` — Glazier slider (defaults to horizontal)

``ServerUI.GetDisplayRoot(player)`` returns the fullscreen root. New widgets are parented there by default. Call ``parent.AddChild(child)`` to reparent into a tree (for example a box containing a label and button).

Destroy one widget with ``element.Destroy()`` (children are destroyed with it), or clear everything with ``ServerUI.DestroyAll(player)``.

Layout and appearance
---------------------

Common layout (all widgets):

- ``PositionOffset_X`` / ``PositionOffset_Y``
- ``PositionScale_X`` / ``PositionScale_Y``
- ``SizeOffset_X`` / ``SizeOffset_Y``
- ``SizeScale_X`` / ``SizeScale_Y``
- ``IsVisible``

These match Sleek / Glazier coordinates: scale is relative to the parent (0–1), offset is in pixels.

By widget type:

- ``Text`` on label, box, button, and field
- ``TextColor`` (custom RGBA) on label, box, button, and field
- ``BackgroundColor`` (custom RGBA) on box, button, and field
- ``TooltipText`` and ``IsClickable`` on button and field
- ``TintColor`` on image
- ``Value`` (0–1) and ``Orientation`` on slider
- ``BindPreviewYaw(image)`` on slider — rotates a live ``RenderCharacter`` / ``RenderEntity`` preview on the owning client

Limits
------

- ``ServerUI.MaxWidgetsPerPlayer`` — 256 user-created widgets per player
- ``ServerUI.MaxTextLength`` — 512 characters for text and tooltips
- ``ServerUI.MaxUrlLength`` — 2048 characters for image URLs
- ``ServerUI.MaxImageDataLength`` — 65535 bytes for PNG/JPG payloads

Images
------

``ServerUIImage`` supports two sources. Setting one clears the other.

Web URL
```````

The client downloads with the same icon query path as ``sendUIEffectImageURL``:

.. code-block:: cs

	ServerUIImage image = ServerUI.CreateImage(player);
	image.SizeOffset_X = 128f;
	image.SizeOffset_Y = 128f;
	image.SetUrl("https://example.com/icon.png", cache: true);
	// Optional: image.SetUrl(url, cache: true, forceRefresh: true);

Plugin bytes
````````````

Send PNG or JPG bytes from the plugin (for example ``File.ReadAllBytes`` next to the module). The client decodes them with ``Texture2D.LoadImage``:

.. code-block:: cs

	byte[] pngBytes = System.IO.File.ReadAllBytes(pluginIconPath);
	image.SetImageData(pngBytes);

Clear with ``image.ClearImage()``. An empty URL or null/empty bytes also clears the texture.

Live renders
````````````

``ServerUIImage`` can also draw client-side previews without a UI effect prefab:

- ``RenderIcon(type, assetGuid)`` — flat item or vehicle icon
- ``RenderEntity(type, assetGuid)`` — spinnable zombie or animal (drag to rotate)
- ``RenderCharacter()`` — the owning player's inventory mannequin

Sliders
-------

``ServerUI.CreateSlider`` creates the same Glazier slider vanilla menus use. ``Value`` is normalized 0–1. Orientation defaults to horizontal.

Bind a slider to a live preview so dragging it rotates the model on the owning client (same idea as inventory character yaw):

.. code-block:: cs

	ServerUIImage image = ServerUI.CreateImage(player);
	image.RenderCharacter();

	ServerUISlider slider = ServerUI.CreateSlider(player);
	slider.BindPreviewYaw(image);
	slider.OnValueChanged += (changedSlider, value) =>
	{
		// Optional server-side handler (rate-limited)
	};

Parenting example
-----------------

.. code-block:: cs

	ServerUIBox panel = ServerUI.CreateBox(player);
	panel.SizeOffset_X = 320f;
	panel.SizeOffset_Y = 120f;
	panel.PositionScale_X = 0.5f;
	panel.PositionScale_Y = 0.5f;
	panel.PositionOffset_X = -160f;
	panel.PositionOffset_Y = -60f;

	ServerUILabel label = ServerUI.CreateLabel(player);
	label.Text = "Hello from the server";
	label.SizeOffset_X = 300f;
	label.SizeOffset_Y = 30f;
	label.PositionOffset_X = 10f;
	label.PositionOffset_Y = 40f;
	panel.AddChild(label);

Events
------

- Instance: ``ServerUIButton.OnClicked``, ``ServerUIField.OnTextSubmitted``, ``ServerUISlider.OnValueChanged``
- Static: ``ServerUI.onButtonClicked(Player, ServerUIButton)``, ``ServerUI.onTextSubmitted(Player, ServerUIField, string)``, ``ServerUI.onSliderValueChanged(Player, ServerUISlider, float)``

Clicks, text submits, and slider changes are rate-limited similarly to EffectManager button/input callbacks. Server state is cleared on disconnect; the client tears down widgets when ``PlayerUI`` is destroyed.

.. _doc_returned_server_sent_ui_dashboard:

Dashboard extensibility
-----------------------

Widgets created with ``ServerUI`` normally sit on a fullscreen root and never touch vanilla menus. ``ServerUIDashboard`` extends the system so plugins can also edit the player dashboard surface: hide curated pieces of the Inventory, Crafting, Skills, and Information tabs, and inject ``ServerUI`` widgets into named attach slots inside those panels.

This is a fixed registry of visibility targets and attach points maintained in game code. It is not free-form targeting of arbitrary UI children by name.

.. note::

	Dashboard visibility **composes** with the vanilla rules. A plugin can only hide a piece; it cannot force-show something the level already hides (for example Crafting and Skills on a ``HORDE`` map).

Hiding parts
````````````

Each hidable piece is a bit in the ``EServerUIDashboardPart`` flags enum:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Part
     - Effect when hidden
   * - ``TabInventory``
     - Inventory tab strip button; also refuses opening the tab.
   * - ``TabCrafting``
     - Crafting tab strip button; also refuses opening the tab.
   * - ``TabSkills``
     - Skills tab strip button; also refuses opening the tab.
   * - ``TabInformation``
     - Information tab strip button; also refuses opening the tab.
   * - ``InfoQuests``
     - Information Quests header button and quests list.
   * - ``InfoGroups``
     - Information Groups header button and groups panel.
   * - ``InfoPlayers``
     - Information Players header button and players panel.

.. code-block:: cs

	// Hide the Information Quests button and list.
	ServerUIDashboard.SetVisible(player, EServerUIDashboardPart.InfoQuests, isVisible: false);

	// Hide several pieces at once (flags).
	ServerUIDashboard.SetPartsVisible(player, EServerUIDashboardPart.TabCrafting | EServerUIDashboardPart.TabSkills, isVisible: false);

	// Restore everything.
	ServerUIDashboard.Reset(player);

Hiding a top-tab part greys the strip button and refuses ``askDashboardOpen`` for that tab, so the hotkey path is blocked too. This runs before the plugin ``onDashboardOpenRequested`` cancel hook, so both gates apply.

Hiding an Information sub-tab (Quests / Groups / Players) hides its header button and panel. If the hidden sub-tab was the active one, the panel falls back to the first still-visible sub-tab.

``ServerUIDashboard.IsPartHidden(player, part)`` and ``ServerUIDashboard.IsTabHidden(player, tab)`` read the current per-player state on the server.

Attach slots
````````````

Each dashboard panel creates an empty frame at build time and registers it as a slot in ``EServerUIDashboardSlot``:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Slot
     - Location
   * - ``TabStripExtra``
     - Top band across the four dashboard tab buttons.
   * - ``InventoryFooter``
     - Bottom strip of the Inventory panel.
   * - ``CraftingFooter``
     - Bottom strip of the Crafting panel.
   * - ``SkillsFooter``
     - Bottom strip of the Skills panel.
   * - ``InformationFooter``
     - Bottom strip of the Information panel.
   * - ``InformationSideHeader``
     - Right column beside the Quests/Groups/Players header row.

Create a widget as usual, then parent it into a slot with ``ServerUIDashboard.Attach``:

.. code-block:: cs

	ServerUIButton button = ServerUI.CreateButton(player);
	button.Text = "Plugin Craft Action";
	button.PositionOffset_X = 10f;
	button.PositionOffset_Y = 10f;
	button.SizeOffset_X = -20f;
	button.SizeOffset_Y = 40f;
	button.SizeScale_X = 1f;
	button.OnClicked += clicked => { /* server-side handler */ };

	ServerUIDashboard.Attach(player, EServerUIDashboardSlot.CraftingFooter, button);

The widget's layout is relative to the slot frame, so position it from the slot's top-left. Attached widgets follow the panel: they only show while that dashboard tab is open, and do not need ``EPluginWidgetFlags.Modal`` (the dashboard provides the cursor).

Attached widgets are not destroyed by ``ServerUIDashboard.Reset`` (which only restores visibility). Remove them with ``element.Destroy()`` or ``ServerUI.DestroyAll(player)``. The hidden-parts mask clears on disconnect; slot registrations are rebuilt when the dashboard UI is recreated.

Compared with UI effects
------------------------

=========================== =============================================== ===========================================
Concern                     Server Sent UI                                  EffectManager UI effects
=========================== =============================================== ===========================================
Backend                     Player's Glazier                                Always uGUI prefab
Authoring                   Code (create button/label/image/…)              Workshop ``EffectAsset`` prefab
Layout                      Sleek position/size scales and offsets          RectTransform (Returned position/size APIs)
Images                      URL, bytes, or live render on ``CreateImage``   Prefab + ``sendUIEffectImageURL`` / render
Sliders                     ``CreateSlider`` + optional ``BindPreviewYaw``  Prefab Slider (uGUI)
=========================== =============================================== ===========================================

See also :ref:`doc_returned_ui_effect_transforms` for duplicate / move / resize on keyed UI effects.
