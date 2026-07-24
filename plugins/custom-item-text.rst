.. _doc_returned_custom_item_text:

Custom Item Text
================

Returned lets a server override the display name and description of a specific item instance in a player's inventory. The owning client shows the custom strings in the inventory selection panel and item tooltips instead of the item asset's localization.

Overview
--------

Custom text is a convenience facade over :ref:`doc_returned_compound_tags`. ``sendItemCustomText`` writes ``Returned.DisplayName`` and ``Returned.DisplayDescription`` on the item's compound tags; ``clearItemCustomText`` removes those keys. Prefer the helpers below unless you need other tag keys.

Custom text is stored on the item instance itself. It is separate from the item's ``state`` byte array and does not replace asset ``.dat`` localization.

When a custom name or description is set, the client resolves display text through ``ItemTool.getDisplayName`` and ``ItemTool.getDisplayDescription``. If no override exists, the client falls back to the item asset's normal name and description builder output.

Custom descriptions support the same rich-text colour tokens used elsewhere in item descriptions, such as ``<color=uncommon>`` and ``<color=rare>``.

Server API
----------

Set or clear custom text on a player inventory slot from server-side plugin code:

.. code-block:: cs

	// page, x, and y identify the item slot in the player's inventory.
	player.inventory.sendItemCustomText(page, x, y, "Custom Name", "Custom description text.");
	player.inventory.clearItemCustomText(page, x, y);

Pass ``null`` or an empty string for ``customName`` or ``customDescription`` to clear only that field. ``clearItemCustomText`` clears both fields.

Inventory coordinates
`````````````````````

Use the same ``page``, ``x``, and ``y`` values as other inventory APIs:

- ``PlayerInventory.SLOTS`` through ``PlayerInventory.AREA`` identify inventory pages.
- ``x`` and ``y`` are the slot coordinates inside that page.

For the primary and secondary equipment slots, ``page`` is ``0`` or ``1``. For the backpack grid, ``page`` is ``PlayerInventory.BACKPACK`` (``3``).

When an item is first added with custom text already set on the server, the text is included in the normal item-add sync. Use ``sendItemCustomText`` when you need to change text on an item that is already in the inventory.

Client behaviour
----------------

The inventory UI updates when custom text changes:

- The selected item name and description panel refreshes if that slot is currently selected.
- ``SleekItem`` tooltips use the custom name when present.

Custom text does not affect crafting search, vendor listings, or other systems that read item asset names directly unless those systems are updated separately.

Persistence
-----------

Custom text is stored on the item instance, so it follows the item through normal
gameplay and is written to save files.

- **Dropping and picking up:** the item keeps its custom text when dropped and picked
  up again, including when another player takes it. The interaction hint on dropped
  items uses the custom name when present.
- **Giving to another player:** transferring the item (drop then pickup, or moving it
  into shared storage) preserves the custom text.
- **Server restart:** custom text is saved to disk and restored on the next server start
  for these containers:

  - Player inventory (``Inventory.dat``, save version 8).
  - Storage barricades such as crates and lockers (``Barricades.dat``, save version 21).
  - Vehicle trunks (``Vehicles.dat``, save version 19).

These versions match the compound-tag save format documented in :ref:`doc_returned_compound_tags`.

.. note::

    Saves written by this Returned version load fine on older builds up to the point of
    the new data, but older builds will ignore the custom text. Once a save is written by
    the new version, load it only with a build that understands the new save version.

Limitations
-----------

- Only the owning client receives the inventory override. Other players see default asset
  names in inventory UI unless you add separate UI for them. Dropped items on the ground
  show the custom name in the interaction hint for all nearby clients.
- Ground items are not saved across a server restart (this matches base game behaviour), so
  custom text on a dropped item is lost only if the server restarts while it is on the ground.
- Each saved name and description is clamped to 255 UTF-8 bytes. Longer strings still work
  over the network in a session but are truncated when written to disk.

Example
-------

Give a quest item a custom label when the player receives it:

.. code-block:: cs

	void OnPlayerReceivedQuestItem(Player player, byte page, byte x, byte y)
	{
		player.inventory.sendItemCustomText(
			page,
			x,
			y,
			"Mysterious Package",
			"Deliver this to the contact at the lighthouse."
		);
	}

When the quest completes, restore the default asset text:

.. code-block:: cs

	player.inventory.clearItemCustomText(page, x, y);
