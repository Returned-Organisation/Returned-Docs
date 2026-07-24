.. _doc_returned_interaction_menu:

Interaction Menu
================

Returned can replace the hold-gesture radial (default key **C**) with a category interaction menu: pick **Emotes**, **Faces**, or a plugin category, then drill into nested submenus.

.. note::

	With ``-LegacyUIs`` (see :ref:`launch options <doc_launch_options>`), the classic faces ring and center emote labels are used instead, and plugin categories are not shown.

Player experience
-----------------

1. Hold the gesture key (default **C**) to open the menu.
2. The root radial shows built-in categories (**Emotes**, **Faces**) plus any plugin categories registered for that player.
3. Selecting a category opens that submenu as another radial. Nested categories are allowed.
4. The center **Back** button returns one level without closing the menu.
5. Selecting an emote, face, or plugin action applies it and closes the menu.
6. Releasing the gesture key closes the menu from any level.

Emote entries still respect the usual stance and equipment rules (hidden while prone, driving, sitting, or holding a useable). Pro-locked faces keep the same lock behaviour as the classic menu.

Plugin API
----------

Server plugins register categories and actions per player. The client owns radial layout; plugins do not create Sleek widgets for this menu.

Reserved ids (do not register these, and do not parent under ``builtin.*``):

- ``PlayerInteractionMenu.RootId`` (empty string) — root radial
- ``PlayerInteractionMenu.BuiltinEmotesId`` (``builtin.emotes``)
- ``PlayerInteractionMenu.BuiltinFacesId`` (``builtin.faces``)

.. code-block:: cs

	// Root category
	PlayerInteractionMenu.RegisterCategory(player, PlayerInteractionMenu.RootId, "myplugin.actions", "Actions");

	// Nested category
	PlayerInteractionMenu.RegisterCategory(player, "myplugin.actions", "myplugin.more", "More");

	// Leaf action — click runs on the server
	PlayerInteractionMenu.RegisterAction(player, "myplugin.actions", "myplugin.wave_extra", "Extra Wave",
		(Player clickedPlayer, string id) =>
		{
			ChatManager.say(clickedPlayer.channel.owner.playerID.steamID, "Extra wave!", Color.green);
		});

	// Remove one entry (and its descendants)
	PlayerInteractionMenu.Unregister(player, "myplugin.actions");

	// Remove all plugin entries for the player
	PlayerInteractionMenu.Clear(player);

Optional global hook:

.. code-block:: cs

	PlayerInteractionMenu.OnActionClicked += (Player player, string id) =>
	{
		// Fired after the per-action callback
	};

Entries are cleared automatically when the player disconnects. Re-register after join if the menu should stay populated.

Example module
--------------

The SDK example module supports:

.. code-block:: text

	rexample interact demo|clear

``demo`` registers a sample category tree for the target player. ``clear`` removes it. The target client must not use ``-LegacyUIs`` to see the entries in the hold-C menu.
