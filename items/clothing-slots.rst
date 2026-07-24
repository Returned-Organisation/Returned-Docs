.. _doc_item_clothing_slots:

Clothing Slots
==============

Returned expands the clothing system from seven to fifteen slots. Each slot is a distinct
:ref:`item type <doc_data_eitemtype>`, so it has clear ``.dat`` authoring, its own inventory row, and its
own plugin ``EItemType`` branch.

See also :ref:`doc_item_asset_clothing` for shared clothing asset properties.

Slot list
---------

Slots are listed in player-facing UI order.

.. list-table::
   :widths: 8 18 24 30 20
   :header-rows: 1

   * - #
     - Slot
     - ``Type``
     - Render model
     - Status
   * - 1
     - Hat
     - ``Hat``
     - 3D prefab on the skull
     - Existing
   * - 2
     - Mask
     - ``Mask``
     - 3D prefab on the skull
     - Existing
   * - 3
     - Glasses
     - ``Glasses``
     - 3D prefab on the skull
     - Existing
   * - 4
     - Neckwear
     - ``Neckwear``
     - 3D prefab on the neck
     - Returned
   * - 5
     - Undershirt
     - ``Undershirt``
     - Torso texture (base layer)
     - Returned
   * - 6
     - Shirt
     - ``Shirt``
     - Torso texture + optional mesh override
     - Existing
   * - 7
     - Jacket
     - ``Jacket``
     - Torso texture (outer layer)
     - Returned
   * - 8
     - Vest
     - ``Vest``
     - 3D prefab on the spine
     - Existing
   * - 9
     - Gloves
     - ``Gloves``
     - Character-material texture
     - Returned
   * - 10
     - Belt
     - ``Belt``
     - 3D prefab on the pelvis
     - Returned
   * - 11
     - Pants
     - ``Pants``
     - Leg texture + optional mesh override
     - Existing
   * - 12
     - Shoes
     - ``Shoes``
     - Character-material texture + optional mesh override
     - Returned
   * - 13
     - Backpack
     - ``Backpack``
     - 3D prefab on the spine
     - Existing
   * - 14
     - Bodysuit
     - ``Bodysuit``
     - Full-body textures + optional mesh override
     - Returned
   * - 15
     - Mesh Replacement
     - ``Mesh_Replacement``
     - Full-body mesh/material override
     - Returned

Shared authoring
----------------

Every clothing type shares the same optional capabilities.

Armor
`````

Armor is available on all fifteen slots, so masks, scarfs, gloves and other pieces can contribute
protection.

* **Armor**: multiplier applied to incoming damage on the limbs the slot covers, scaled by item quality.
  ``1.0`` means no reduction (the default); ``0.5`` halves damage.
* **Armor_Type**: which bullet calibers the piece stops. See :ref:`doc_data_earmortype`. Defaults to
  ``None`` so existing items are unaffected.

When several worn pieces cover the same limb, their ``Armor`` multipliers stack **multiplicatively**, the
same way a vest and shirt already stack on the spine. For example a ``0.5`` undershirt and a ``0.8`` shirt
on the arms combine to ``0.5 × 0.8 = 0.4`` (a 60% reduction).

.. code-block:: unturneddat

	Armor 0.5
	Armor_Type Light

Storage
```````

Any clothing type can provide storage with ``Width`` and ``Height``.

* A worn item with ``Width`` and ``Height`` greater than zero shows a storage page as usual.
* A worn item with ``0`` width and height still shows an **empty** storage page by default.
* Set ``Hide_Storage_Page`` to ``true`` to hide that empty page and restore the legacy behaviour.
* Gear-only slots (hat, mask, glasses, neckwear, mesh replacement) have no worn storage page.

.. code-block:: unturneddat

	Width 0
	Height 0
	Hide_Storage_Page true

Torso layering
--------------

The undershirt, shirt and jacket slots composite as texture overlays on the shared torso material, in
this order: undershirt first, then shirt, then jacket. There are no engine-side region masks or sleeve
flags. To reveal a lower layer — for example long undershirt sleeves under a short-sleeved shirt — leave
the corresponding areas of the upper texture transparent using its alpha channel.

Bodysuit exclusivity
--------------------

While a ``Bodysuit`` is worn it blocks the shirt, pants, gloves and shoes slots, unequipping any items in
them back to the inventory. The undershirt, jacket, vest and all accessory slots (hat, mask, glasses,
neckwear, belt, backpack, mesh replacement) can still be worn on top.

Mesh replacement
----------------

Use ``Type Mesh_Replacement`` for a dedicated full-body character mesh and material swap. It is gear-only
(no worn storage page) and does not block other clothing slots. When worn it takes priority over mesh-override
flags on shirt, pants, shoes, or bodysuit. Author 3P mesh overrides for new content; 1P override flags remain
only for compatibility. See :ref:`doc_character_mesh_replacement`.

Shirt, pants, shoes, and bodysuit can still author the same mesh-override flags as a legacy path.
