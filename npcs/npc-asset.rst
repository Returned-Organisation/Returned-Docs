.. _doc_object_asset_npc:

NPC Character Assets
====================

**GUID** *32-digit hexadecimal*: Refer to :ref:`GUID <doc_data_guid>` documentation.

**Type** *enum* (``NPC``)

**ID** *uint16*: Must be a unique identifier.

**PlayerKnowsNameFlagID** *uint16*: If non-zero, NPC name is shown as ??? until bool flag is true. For example if set to 20 the NPC name is ??? until a Flag_Bool reward with ID 20 is set to true.

Clothing
--------

**Shirt** *uint16* or *GUID*: ID or GUID of shirt to wear.

**Pants** *uint16* or *GUID*: ID or GUID of pants to wear.

**Hat** *uint16* or *GUID*: ID or GUID of hat to wear.

**Backpack** *uint16* or *GUID*: ID or GUID of backpack to wear.

**Vest** *uint16* or *GUID*: ID or GUID of vest to wear.

**Mask** *uint16* or *GUID*: ID or GUID of mask to wear.

**Glasses** *uint16* or *GUID*: ID or GUID of glasses to wear.

Holiday outfits
```````````````

NPC characters can have event-specific outfits, which will only appear during the assigned seasonal event.

**Has_Halloween_Outfit** *flag*: Specified if event-specific clothing should be worn during the Halloween event.

**Halloween_Shirt** *uint16* or *GUID*: ID or GUID of shirt to wear during the Halloween event.

**Halloween_Pants** *uint16* or *GUID*: ID or GUID of pants to wear during the Halloween event.

**Halloween_Hat** *uint16* or *GUID*: ID or GUID of hat to wear during the Halloween event.

**Halloween_Backpack** *uint16* or *GUID*: ID or GUID of backpack to wear during the Halloween event.

**Halloween_Vest** *uint16* or *GUID*: ID or GUID of vest to wear during the Halloween event.

**Halloween_Mask** *uint16* or *GUID*: ID or GUID of mask to wear during the Halloween event.

**Halloween_Glasses** *uint16* or *GUID*: ID or GUID of glasses to wear during the Halloween event.

**Has_Christmas_Outfit** *flag*: Specified if event-specific clothing should be worn during the Festive event.

**Christmas_Shirt** *uint16* or *GUID*: ID or GUID of shirt to wear.

**Christmas_Pants** *uint16* or *GUID*: ID or GUID of pants to wear.

**Christmas_Hat** *uint16* or *GUID*: ID or GUID of hat to wear.

**Christmas_Backpack** *uint16* or *GUID*: ID or GUID of backpack to wear.

**Christmas_Vest** *uint16* or *GUID*: ID or GUID of vest to wear.

**Christmas_Mask** *uint16* or *GUID*: ID or GUID of mask to wear.

**Christmas_Glasses** *uint16* or *GUID*: ID or GUID of glasses to wear.

Appearance
----------

While in the Appearance menu in-game, modders can press Page Down to copy the player's current appearance to clipboard.

**Face** *int*: Index of face image.

**Hair** *int*: Index of hair mesh.

**Beard** *int*: Index of beard mesh.

**Color_Skin** *hex triplet*: Six-digit hexadecimal number representing RGB color.

**Color_Hair** *hex triplet*: Six-digit hexadecimal number representing RGB color.

**Backward** *flag*: Specified if character is left-handed.

Pose
----

**Primary** *uint16* or *GUID*: ID or GUID of the weapon carried on the character's back, parallel to the spine.

**Secondary** *uint16* or *GUID*: ID or GUID of the weapon carried on the character's hip, perpendicular to the spine.

**Tertiary** *uint16* or *GUID*: ID or GUID of a non-weapon item to carry.

**Equipped** *enum* (``Primary``, ``Secondary``, ``Tertiary``): The item in the specified slot will be held in the character's hands, rather than carried.

**Dialogue** *uint16* or *GUID*: ID or GUID of the dialogue asset to open when interacted with.

**Pose** *enum* (``Asleep``, ``Crouch``, ``Passive``, ``Prone``, ``Rest``, ``Sit``, ``Stand``, ``Surrender``, ``Under_Arrest``): Idle animation.

**Pose_Head_Offset** *float*: Offset of the NPC's head from their body, in meters. Positive numbers offset it forward, while negative numbers offset it backward. Defaults to 0.1.

**Pose_Lean** *float*: How far the NPC leans left or right, as a number from -1 to 1. Positive numbers learn to the NPC's left, while negative numbers lean to the NPC's right. Defaults to 0.

**Pose_Pitch** *float*: How far the NPC leans forward or backward, in degrees. Numbers greater than 90 lean forward, while numbers less than 90 lean backward. Defaults to 90.

Roaming
-------

Returned supports pathfinding roaming NPCs. See :ref:`doc_npcs_roaming` for navmesh setup, spawn points, and dialogue pause behaviour.

**Can_Roam** *bool*: When true, level NPC spawn points for this asset create a roaming NPC. Defaults to false.

**Speed_Walk** *float*: Walk speed while roaming. Defaults to ``3.5``.

**Roam_Idle_Min** *float*: Minimum idle seconds between roam destinations. Defaults to ``2``.

**Roam_Idle_Max** *float*: Maximum idle seconds between roam destinations. Defaults to ``8``.

**Interactable_While_Roaming** *bool*: Allow talk while walking. Defaults to true.

Combat (Returned)
`````````````````

See :ref:`doc_npcs_roaming` for behaviour details.

**Can_Combat** *bool*: Enable combat AI. Defaults to false.

**Aggression** *enum* (:ref:`doc_data_eanimalbehaviour`): Defaults to ``Ignore``.

**Detection_Radius** *float*: ``0`` = stealth radius. Defaults to ``0``.

**Combat_Leash_Radius** *float*: Defaults to ``48``.

**Target_Lost_Radius** *float*: Defaults to ``64``.

**Speed_Run** *float*: Defaults to ``7``.

**Health** *uint16*: Defaults to ``100``.

**Can_Die** *bool*: Defaults to true.

**Invulnerable** *bool*: Defaults to false.

**Respawn_Time** *float*: Defaults to ``300``. ``0`` = no respawn.

**Combat_Reset_Delay** *float*: Defaults to ``30``.

**Melee_Damage** *byte*: Defaults to ``15``.

**Melee_Range** *float*: Defaults to ``2.25``.

**Melee_Vertical_Range** *float*: Defaults to ``2``.

**Melee_Interval** *float*: Defaults to ``1``.

**Alert_On_Gunshot** *bool*: Defaults to true.

**Hostile_Reputation_Below** *int*: Opt-in low-reputation auto-aggro threshold.

**Ranged_Preferred_Min** *float*: Defaults to ``8``.

**Ranged_Preferred_Max** *float*: Defaults to ``24``.

**Weapon_Swap_Cooldown** *float*: Defaults to ``0.75``.

**Primary_Ammo** / **Secondary_Ammo** / **Tertiary_Ammo** *uint16*: Starting gun ammo per slot.

**Infinite_Ammo** *bool*: Defaults to false.

**Loot_ID** *uint16*: Death loot spawn table.

**Loot_Min** / **Loot_Max** *int*: Drop count range.

**Loot_Chance** *float*: Defaults to ``1``.

**Drop_Equipped_Weapons** *bool*: Drop P/S/T items on death.

Conditions
----------

An NPC character can be made to only appear while certain :ref:`conditions <doc_npc_asset_conditions>` are met by the player.

Localization
------------

**Name** *string*: Object name in level editors.

**Character** *string*: Character name displayed when interacted with. 
