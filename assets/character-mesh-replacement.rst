.. _doc_character_mesh_replacement:

Character Mesh Replacement
==========================

The player's character mesh can be entirely replaced with a dedicated ``Mesh_Replacement`` clothing item.
Author it with ``Type Mesh_Replacement`` and the mesh-override flags below. Prefer this type for new content.

Shirt, pants, shoes, and bodysuit can still carry the same flags as a legacy path. When a ``Mesh_Replacement``
item is worn, its meshes and material win over those legacy overrides.

Returned uses the third-person character body for the local player view as well. Author **3P** replacement
meshes for new content. The 1P override flags and prefabs remain for compatibility with older assets and
the classic separate-viewmodel path; they are not required for new ``Mesh_Replacement`` items.

There's an example CharacterMeshReplacementTest item (ID 1522) that still uses a shirt for historical reasons,
as well as example source files in the ExampleAssets.unitypackage under the Shirts directory.

.. note::

	See :ref:`doc_item_clothing_slots` for the ``Mesh_Replacement`` slot and how it relates to the other
	clothing slots.

.. code-block:: unturneddat

	Type Mesh_Replacement
	Character_Mesh_3P_Override_LODs 1
	Has_Character_Material_Override True
	Hair_Visible False
	Beard_Visible False

Properties Reference
--------------------

* **Character_Mesh_3P_Override_LODs**: >0 (primary for new content)
* **Has_Character_Material_Override**: true
* **Has_1P_Character_Mesh_Override**: true (compatibility only)
* **Hair_Visible**: true/false
* **Beard_Visible**: true/false

If ``Character_Mesh_3P_Override_LODs`` is greater than zero then the game will try to load prefabs for each LOD index (e.g., Character_Mesh_3P_Override_0). These should have MeshFilter components for the third person replacement meshes. This is the mesh used on the world character and on the unified local player view.

If ``Has_Character_Material_Override`` is true then the game will try to load a material named "Character_Material_Override" to replace the character mesh materials. Without this, equipped shirt and pants textures will be used by default.

Compatibility: 1P override
--------------------------

``Has_1P_Character_Mesh_Override`` and ``Character_Mesh_1P_Override_0`` are kept so existing assets that
authored a separate first-person arms mesh still load. New content does not need them.

If ``Has_1P_Character_Mesh_Override`` is true then the game will try to load a prefab named
"Character_Mesh_1P_Override_0". Historically this was an arms-only mesh for the separate first-person
viewmodel. Prefer 3P overrides instead.
