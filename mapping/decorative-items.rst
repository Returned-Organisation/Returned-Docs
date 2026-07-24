.. _doc_mapping_decorative_items:

Decorative Items
================

The level editor **Objects** tool can place regular items (guns, food, clothing, and other non-buildable items) as **static decoration**.

Placed decorative items:

- Use the item's world ``Item`` prefab mesh
- Have player and vehicle collision
- Are **not** pickable loot
- Are **not** barricades or structures

Barricades and structures still use the existing **Barricades** / **Structures** toggles and save as map buildable defaults.

Usage
-----

1. Open the level editor **Objects** tool.
2. Enable the **Items** toggle.
3. Select an item from the list and place it like any other object.
4. Move, rotate, and scale as needed.

Save format
-----------

Decorative placements are stored in ``Level/DecorItems.dat`` inside the map folder. They are separate from ``Objects.dat`` and ``Buildables.dat``.

Only items with a valid world ``Item`` prefab appear in the list. Cosmetics without an Item model are skipped.
