.. _doc_returned_compound_tags:

Compound Tags
=============

Returned stores per-instance metadata on items as a named compound tag tree beside the opaque ``state[]`` byte array. Tags identify and decorate a specific item instance; they are not part of the item asset definition.

Overview
--------

Every inventory ``Item`` owns a ``tags`` compound (never null; empty until something writes to it). Use tags when two items share the same asset GUID but must remain distinct at runtime — for example two pine logs that look identical but carry different plugin tracking ids.

Asset GUID alone cannot track instances. Plugins that need durable per-item identity or metadata should write namespaced keys on ``Item.tags``.

Tags are separate from ``state[]``:

- ``state[]`` remains the compact vanilla layout blob (for example gun attachments or amount flags). It is still capped at **255 bytes** for vanilla-compatible layouts.
- ``tags`` is a typed key/value tree (strings, ints, nested compounds, lists, and related types) with a larger serialized budget. Prefer tags for plugin metadata.

Example
-------

Two pine logs from the same asset can carry different plugin ids:

.. code-block:: cs

	void StampTrackId(Item item, int trackId)
	{
		item.tags.SetInt("MyPlugin.TrackId", trackId);
	}

	// Later, after the item is already in the player's inventory:
	player.inventory.sendUpdateItemTags(page, x, y);

Both jars resolve to the same pine-log asset GUID. Only the ``MyPlugin.TrackId`` values differ.

Server API
----------

Mutate tags on the server, then sync when the item is already in a player inventory slot.

.. code-block:: cs

	ItemJar jar = player.inventory.getItem(page, player.inventory.getIndex(page, x, y));
	if (jar == null || jar.item == null)
	{
		return;
	}

	CompoundTag tags = jar.item.tags;
	tags.SetString("MyPlugin.OwnerName", "Eli");
	tags.SetInt("MyPlugin.TrackId", 42);
	tags.Remove("MyPlugin.ObsoleteKey");

	player.inventory.sendUpdateItemTags(page, x, y);

Common helpers on ``CompoundTag`` include ``SetString`` / ``GetString``, ``SetInt`` / ``GetInt``, ``SetBool`` / ``GetBool``, ``Contains``, ``Remove``, and nested ``GetOrCreateCompound``.

``player.inventory.sendUpdateItemTags(page, x, y)``
	Server-only. Syncs the jar's already-mutated ``Item.tags`` to the owning client. Call this after you change tags in place on an item that is already in inventory. When you add an item that already has tags set, the normal item-add sync includes them.

Inventory coordinates match other inventory APIs. See :ref:`doc_returned_custom_item_text` for ``page`` / ``x`` / ``y`` conventions.

Namespacing
-----------

Prefix keys with your plugin id so they do not collide with other plugins or reserved Returned keys:

.. code-block:: text

	PluginId.Key

Examples: ``MyPlugin.TrackId``, ``QuestMod.DeliveryNpc``. Use a stable plugin id; do not invent keys under the ``Returned.`` prefix.

Reserved keys
-------------

Returned reserves these string keys on item compounds (also available as ``ItemTagKeys`` constants):

``Returned.DisplayName``
	Server-provided display name override (string). Prefer :ref:`doc_returned_custom_item_text` helpers unless you are writing tags directly.

``Returned.DisplayDescription``
	Server-provided display description override (string).

``Returned.V2Attachments``
	GUID-based attachment list for V2 modular clothing. Written by the clothing system; see :ref:`doc_returned_v2_modular_clothing`.

Do not overwrite reserved keys unless you intentionally replace that subsystem's data.

Custom text
-----------

Custom display name and description still use ``player.inventory.sendItemCustomText`` and ``clearItemCustomText``. Those helpers are a convenience facade: they store ``Returned.DisplayName`` and ``Returned.DisplayDescription`` inside the item's compound tags. See :ref:`doc_returned_custom_item_text`.

Size limits
-----------

- Serialized compound payloads are capped at **16 KiB** (``CompoundTagCodec.MaxSerializedSize``).
- Nested compounds and lists may nest up to depth **3** (root counts as depth 0).
- Vanilla ``state[]`` layouts remain **255 bytes**. Put plugin metadata in tags, not in ``state[]``.

Persistence
-----------

Compound tags travel with the item instance through normal gameplay (drop, pickup, storage transfer) and are written to save files:

- Player inventory (``Inventory.dat``, save version **8**).
- Storage barricades such as crates and lockers (``Barricades.dat``, save version **21**).
- Vehicle trunks (``Vehicles.dat``, save version **19**).
- Worn classic clothing pieces (``Clothing.dat``, save version **11**) keep per-slot tags across wear/unequip and save/load.

Ground items keep tags for the session. Like other ground loot, they are not saved across a server restart.

.. note::

	Saves written by this Returned version load fine on older builds up to the point of the new data, but older builds ignore compound tags. Once a save is written by the new version, load it only with a build that understands the new save version.

Authority
---------

Tags are server-authoritative. Clients receive synced tag payloads for their own inventory and for nearby ground items when relevant; they do not invent or push arbitrary tags back to the server. Mutate tags only from server-side plugin or module code, then call ``sendUpdateItemTags`` when the owning client must refresh.
