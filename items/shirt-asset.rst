.. _doc_item_asset_shirt:

Shirt Assets
============

Shirts are created from the ItemShirtAsset class. They can be worn by players and zombies.

This inherits the :ref:`BagAsset <doc_item_asset_bag>` class.

Item Asset Properties
---------------------

**GUID** *32-digit hexadecimal*: Refer to :ref:`GUID <doc_data_guid>` documentation.

**Type** *enum* (``Shirt``)

**Useable** *enum* (``Clothing``)

**ID** *uint16*: Must be a unique identifier.

Shirt Asset Properties
----------------------

**Ignore_Hand** *flag*: Specified if shirt should ignore a player's left-handed setting.

Body Mesh Replacements
----------------------

For the full documentation, refer to the :ref:`Character Mesh Replacement <doc_character_mesh_replacement>` documentation.

**Has_1P_Character_Mesh_Override** *bool*: Compatibility only. A prefab named "Character_Mesh_1P_Override_0" should be loaded. Defaults to false. Prefer 3P overrides; see :ref:`doc_character_mesh_replacement`.

**Character_Mesh_3P_Override_LODs** *uint16*: Number of prefabs to load for each LOD index. Defaults to 0. Primary path for new content.

**Has_Character_Material_Override** *bool*: A material named "Character_Material_Override" should be loaded to replace the character mesh materials. Defaults to false.
