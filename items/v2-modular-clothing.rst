.. _doc_returned_v2_modular_clothing:

V2 Modular Clothing
===================

Returned supports modular clothing for the V2 character body. Instead of fixed visual categories such as shirt, pants, vest, and backpack, a wearable item declares the body regions it covers and the layer it occupies.

Overview
--------

A V2 wearable can cover one or more body regions such as the head, torso, arms, hands, legs, and feet. Layers control stacking. For example, an undershirt, jacket, armor vest, and equipment rig can all cover the torso if each item uses a different layer.

Only one item can occupy the same region and layer at the same time. If a vest covers ``Torso`` on the ``Armor`` layer, another ``Torso``/``Armor`` item is rejected until the vest is removed.

Wearable fields
---------------

Add these fields to an ``ItemClothingAsset`` item to make it available to the V2 modular clothing path:

.. code-block:: unturneddat

	Type Vest
	V2_Regions Torso Left_Arm Right_Arm
	V2_Layer Armor
	V2_Covered_Regions Torso

``V2_Regions``
	Lists the body regions occupied by the wearable for layer conflicts. Valid values are ``Head``, ``Neck``, ``Torso``, ``Left_Arm``, ``Right_Arm``, ``Left_Hand``, ``Right_Hand``, ``Left_Leg``, ``Right_Leg``, ``Left_Foot``, and ``Right_Foot``. Occupying a region does **not** hide the base body by itself.

``V2_Layer``
	Sets the occupied layer. Valid values are ``Base``, ``Under``, ``Shirt``, ``Outer``, ``Armor``, ``Equipment``, and ``Accessory``.

``V2_Covered_Regions``
	Optional. Force-hides the listed base V2 body parts while worn. Use this when you need to hide skin without a ``V2_Mesh_*`` replacement (for example a classic ``Vest.prefab`` overlay). If omitted, no extra regions are force-hidden.

Region meshes
-------------

Add optional bundle objects named for each region mesh:

.. code-block:: text

	V2_Mesh_3P_Torso
	V2_Mesh_3P_Left_Arm
	V2_Mesh_3P_Right_Arm
	V2_Mesh_1P_Left_Hand
	V2_Mesh_1P_Right_Hand
	V2_Material_Torso

When Returned applies ``V2_Mesh_3P_Torso`` (or another region mesh), it hides that base body part and shows the replacement. Regions without a mesh stay visible, so pouches and other add-ons can sit on top of the body without deleting it.

Third-person meshes render on the world character. First-person meshes render only for supported viewmodel regions, usually arms and hands. If a first-person mesh is not supplied, that region is skipped in first person.

If no ``V2_Mesh_*`` assets are present, Returned falls back to the classic clothing prefab for that item type (for example ``Vest.prefab`` parented to Spine). Prefab fallback does not hide body parts unless you set ``V2_Covered_Regions``.

Attachment sockets
------------------

Wearables can expose attachment sockets. Each socket has an id, a transform name on the wearable model, and optional compatibility tags:

.. code-block:: unturneddat

	V2_Attachment_Slot_0 slot_1
	V2_Attachment_Slot_0_Transform slot_1
	V2_Attachment_Slot_0_Compatible_Tags pouch plate

Like a gun's ``Sight`` / ``Tactical`` / ``Grip`` fields, you can optionally author a starting attachment per socket:

.. code-block:: unturneddat

	V2_Attachment_Slot_0_Default_ID 65002
	V2_Attachment_Slot_0_Default_Quality 100

When those keys are set, new item instances apply the defaults into compound tags under ``Returned.V2Attachments`` so loot and ``/give`` spawn the wearable already fitted. ``getState`` returns an empty ``item.state`` for V2 wearables; attachments live in tags instead. Omit the keys and the socket starts empty. Quality defaults to ``100`` when omitted. Missing default item ids are skipped with a warning. World and admin origins share the same authored defaults.

Player-facing socket names live in the wearable language file (for example ``English.dat``). Use the socket id as the key:

.. code-block:: unturneddat

	Name Testing Vest
	Description Modular test vest with pouch sockets.

	slot_1 Mag Pouch Left
	slot_2 Mag Pouch Center
	slot_3 Mag Pouch Right
	slot_4 Utility Slot

If a key is missing, the inventory UI falls back to the raw socket id. The attached item is a real inventory item with its own GUID, quality, and state. Attachments stay bound to the wearable: unequipping gives a single clothing item that carries its attachments in compound tags, and re-equipping restores the filled sockets. Detaching an attachment while the wearable is worn still returns a standalone item.

.. note::

	Attachments persist on the clothing item itself, not as separate inventory items. When you unequip, drop, or die (with clothing loss enabled), the wearable keeps its attachments under the reserved compound-tag key ``Returned.V2Attachments`` (GUID, socket id, and quality per filled socket). Legacy compact ``item.state`` attachment layouts are upgraded into that tag on load. See :ref:`doc_returned_compound_tags`. This keeps a kitted-out wearable as one item everywhere the inventory or ground loot moves it.

``Attachment.prefab`` is parented to the socket transform at local identity. Author the attachment mesh in socket-local space (origin at the mount point), not in spine/vest-root clothing space. Classic clothing-to-spine ``Model_0`` offsets are for wearable prefabs only.

Attaching and removing
----------------------

In the inventory UI:

* Select an attachment item (for example a pouch) and click **Attach**.
* If more than one worn V2 piece has a free compatible socket, choose which clothing piece to use.
* Then choose a free compatible socket from the button list. Returned mounts the attachment on that socket.
* If only one worn piece is compatible, the wearable step is skipped and you go straight to socket selection.
* With ``-LegacyUIs``, on the modular storage header (backpack page), click **Attachments** to inspect the worn wearable. Each filled socket has a **Remove** button. Use **Unequip** to take the wearable off. (The default inventory hides that button and uses the right-click socket column instead.)
* Inspecting a worn V2 wearable shows combined stats from the piece and its attachments (storage, armor, movement, and related clothing modifiers).

On a V2 body with the default (modern) inventory:

* Worn modular pieces appear in the matching paper-doll equip wells (for example a V2 vest in **VEST**).
* Left-click a worn well to inspect / unequip that piece.
* Right-click a worn well that has attachment sockets to open a column of **1x1 socket slots**: to the right of left-column wells, to the left of right-column wells, and below the hat. Empty sockets show ``+``; filled sockets show the attachment icon.
* Drag any-size compatible attachment from your inventory into an empty socket slot to mount it. Left-click a filled socket to detach.
* Right-click the same clothing well again to close the socket column.

Attachment items
----------------

Use ``Clothing_Attachment`` for items that can be placed into V2 clothing sockets. The item still needs a normal item ``Type`` for inventory behavior.

.. code-block:: unturneddat

	Metadata
	{
		GUID 0123456789abcdef0123456789abcdef
		Type Clothing_Attachment
	}

	Type Supply
	ID 65002
	V2_Attachment_Tags pouch
	Width 3
	Height 2
	Movement_Speed_Multiplier 0.98

``Metadata.Type Clothing_Attachment`` selects the C# asset class (registered name). Root ``Type Supply`` sets the inventory item category (``EItemType``). Put ``GUID`` inside ``Metadata``, not at the root.

Optional attachment stats include ``Armor``, ``Armor_Explosion``, ``Armor_Type``, ``Movement_Speed_Multiplier``, ``Falling_Damage_Multiplier``, and ``Prevents_Falling_Broken_Bones``.

Storage
-------

V2 storage comes from the worn item plus its attachments. Returned aggregates this storage into a modular worn-equipment page for compatibility with the existing inventory system.

Vendors and NPC rewards
-----------------------

Sell or reward a kitted V2 wearable the same way gun attachments are overridden:

.. code-block:: unturneddat

	Selling_0_ID 65001
	Selling_0_V2_Attachment_0_Slot slot_1
	Selling_0_V2_Attachment_0_ID 65002
	Selling_0_V2_Attachment_0_Quality 100

Quest item rewards use ``Reward_#_V2_Attachment_#_Slot/ID/Quality``. When no overrides are set, the wearable uses its asset socket defaults written into ``Returned.V2Attachments``.

NPC visual outfits
------------------

NPC assets can list modular wearables with ``V2_Wearable_#`` (and holiday-prefixed variants). See :ref:`doc_object_asset_npc`. Classic shirt/pants/vest keys still work for V1 body and cosmetics.

Placeable mannequins
--------------------

The vanilla cloth and metal mannequin barricades keep their gray mannequin skin. Returned force-swaps **only those two assets** to the V2 character body so modular outfits render even when the server body generation is V1. Modded mannequins (custom GUID / custom prefab) are not force-swapped.

Mannequins store a full V2 clothing snapshot in barricade state (after the classic pose byte). Use the existing mannequin UI:

* **Add** a held V2 wearable (with attachments in compound tags) onto the mannequin.
* **Remove** returns each V2 piece as a single item with attachments encoded in ``Returned.V2Attachments``.
* **Swap** exchanges the player's worn V2 outfit with the mannequin's.
* Destroying the barricade drops the same encoded kits.

Classic seven-slot clothing still works on mannequins for non-V2 items and cosmetics.

Zombie visual outfits
---------------------

When the active body is V2:

* Put a V2 wearable in a zombie table **hat** or **gear** slot (legacy clothing ids), or
* Author ``V2_Wearable_#`` on a :ref:`zombie difficulty asset <doc_assets_zombie_difficulty>`.

Zombie outfits are visual only (no inventory pages). Attachments use the wearable's asset defaults or difficulty-authored ``V2_Wearable_#_Attachment_*`` keys.
