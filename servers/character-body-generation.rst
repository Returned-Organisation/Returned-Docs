.. _doc_returned_character_body_generation:

Character Body Generation (V1/V2)
=================================

Returned can render every humanoid with one of two character body generations:

- **V1** — the vanilla Returned monolithic body mesh.
- **V2** — the multi-part "Human 2" body (head, neck, torso, arms, hands, legs, and feet, each skinned separately).

The active generation applies to every humanoid body: players (first- and third-person), NPCs, mannequins, menu and entity previews, zombies, and ragdolls. Clothing, faces, hair, skins, and mythic effects are unaffected — a full-body clothing mesh override still takes precedence over the generation swap.

Singleplayer
------------

In singleplayer the generation is chosen per survivor in the survivor **Appearance** menu with the **Character V1 / Character V2** toggle. The choice is saved with that survivor's profile, so different survivors can use different bodies.

Multiplayer
-----------

In multiplayer the server owns the choice for the whole session. Set it with the ``Character_Body_Generation`` option in the server's ``Config.txt`` under ``Gameplay`` (see :ref:`doc_servers_server_configuration`):

.. code-block:: text

	Gameplay
	{
		// Options: V1, V2
		// Default: V1
		Character_Body_Generation V2
	}

- The default is **V1**.
- The value is replicated to every client when they join, so all humanoids on the server render the server's generation.
- Clients cannot override the server's choice; the survivor Appearance toggle only affects singleplayer.

The setting is auto-documented in the generated ``Config.txt`` comments, including the list of valid options.
