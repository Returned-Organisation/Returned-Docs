.. _doc_physics_prop_example:

Physics Prop Example (Soccer Ball)
==================================

Returned includes a minimal physics-prop object you can use as a template for bouncy, resettable props. For property reference, see :ref:`doc_assets_object` (``Interactability Physics_Prop`` and ``Physics_Prop_`` properties).

Example Files
-------------

- ``Assets/Game/Sources/Objects/Examples/Soccer_Ball_0/Soccer_Ball_0.dat`` — tracked backup for the Medium object definition (ID **65500**)
- ``Assets/Game/Sources/Objects/Examples/Soccerball/Soccerball.dat`` — tracked backup for the Sandbox Small definition (ID **65501**)
- ``Builds/Test/Bundles/Objects/Medium/Soccer_Ball_0/Soccer_Ball_0.dat`` — runtime copy (gitignored; wiped by **Build Test** / Steam sync)
- ``Builds/Test/Bundles/Objects/Medium/Soccer_Ball_0/Soccer_Ball_0.unity3d`` — legacy asset bundle (built from Unity, not the master bundle)
- ``Builds/Test/Sandbox/Soccertest/Soccerball/`` — Sandbox runtime copy and bundle

The ``.dat`` includes ``Exclude_From_Master_Bundle`` and ``Asset_Bundle_Version 6`` so Unturned loads the sibling ``Soccer_Ball_0.unity3d`` file instead of ``core.masterbundle``.

Who Can Move a Physics Prop
---------------------------

By default, **all sources are allowed**. Omit these keys for the soccer ball behaviour (players, zombies, animals, vehicles, melee, bullets, and explosions).

Allow List
``````````

Only the listed sources can move the prop:

.. code-block:: unturneddat

	Physics_Prop_Allowed Players, Zombies, Animals

Deny List
`````````

Start from ``All``, then remove sources:

.. code-block:: unturneddat

	Physics_Prop_Denied Bullets, Explosions

Per-Source Booleans
```````````````````

Override individual sources. These can be combined with allow/deny lists:

.. code-block:: unturneddat

	Physics_Prop_Allow_Players true
	Physics_Prop_Allow_Zombies false
	Physics_Prop_Allow_Animals true
	Physics_Prop_Allow_Vehicles true
	Physics_Prop_Allow_Melee true
	Physics_Prop_Allow_Bullets false
	Physics_Prop_Allow_Explosions false

Valid source names are ``Players``, ``Zombies``, ``Animals``, ``Vehicles``, ``Melee``, ``Bullets``, ``Explosions``, and ``All``.

Players-Only Puzzle Ball
````````````````````````

.. code-block:: unturneddat

	Interactability Physics_Prop
	Interactability_Reset 120
	Physics_Prop_Allowed Players

Horde Toy Ball
``````````````

Zombies can kick the ball, but guns cannot:

.. code-block:: unturneddat

	Physics_Prop_Allowed Players, Zombies, Animals, Melee
	Physics_Prop_Denied Bullets

Workflow (Legacy .unity3d)
--------------------------

1. Open the Unity project
`````````````````````````

Use Unity **2022.3.62f3**, then open ``Assets/GameStartup.unity``.

2. Copy .dat files into ``Builds/Test/``
````````````````````````````````````````

``Builds/Test/`` is gitignored and gets wiped by **Build Test** / Steam sync. Copy tracked backups from ``Assets/Game/Sources/Objects/Examples/`` into the matching runtime folders under ``Builds/Test/``.

3. Build the legacy bundle
````````````````````````````

Open **Window > Unturned > Bundle Tool**. Select the ``Soccer_Ball_0`` source folder, grab assets, and save as ``Soccer_Ball_0.unity3d`` beside the ``.dat`` in ``Builds/Test/Bundles/Objects/Medium/Soccer_Ball_0/``.

4. Rebuild scripts if needed
``````````````````````````````

If you changed code, run **Build Test (Scripts Only)** to refresh ``Builds/Test/Unturned.exe``.

5. Place in the level editor
``````````````````````````````

Run ``Builds/Test/Unturned.exe``, then place **Soccer Ball** under **Medium** (ID **65500**).

Sandbox Small Variant
`````````````````````

Copy ``Assets/Game/Sources/Objects/Examples/Soccerball/`` into ``Builds/Test/Sandbox/Soccertest/Soccerball/``, build ``Soccerball.unity3d`` with **Bundle Tool**, then place **Soccerball** (ID **65501**).

Troubleshooting
---------------

Missing "Object" GameObject
```````````````````````````

The ``.dat`` loaded, but ``Soccer_Ball_0.unity3d`` is missing or does not contain a prefab named ``Object``. Rebuild the legacy bundle with **Bundle Tool**.

.dat Files Disappeared from ``Builds/Test/``
`````````````````````````````````````````````

This is expected after **Build Test** or Steam sync. Copy them again from ``Assets/Game/Sources/Objects/Examples/``.

Ball Falls Through Ground
`````````````````````````

Unturned's physics matrix only lets the **ITEM** layer collide with terrain. Physics props switch to ITEM at runtime. Rebuild scripts and the legacy bundle (collider center fix).

Ball Does Not React to Punches, Bullets, or Explosions
``````````````````````````````````````````````````````

Rebuild **Build Test (Scripts Only)**. Melee, gun, and explosion hits apply impulses; vehicles and other colliders push via physics contact.

Ball Vibrates or Will Not Move When Pushed
``````````````````````````````````````````

Rebuild scripts and re-export the legacy bundle if needed.

Ball Bounces Up and Down Instead of Rolling
```````````````````````````````````````````

Rebuild **Build Test (Scripts Only)**. Ground contact now zeros vertical velocity and terrain snap no longer fights gravity on every frame.

Ball Collision Does Not Match the Visible Sphere
````````````````````````````````````````````````

Rebuild the legacy bundle after prefab collider changes. Collider radius/center should match the mesh. The soccer ball uses radius **0.5** and center **y: 0.5**.

Ball Barely Moves When Pushed or Punched
``````````````````````````````````````````

Rebuild scripts and the legacy bundle. Push overlap, force multipliers, drag, and minimum melee impulse were tuned for a heavier rolling feel.

Fists Do Not Move the Ball
``````````````````````````

Rebuild **Build Test (Scripts Only)**. Default punch (``PlayerEquipment.punch``) now applies physics-prop impulse; only melee weapons did before.

Animals Do Not Move the Ball
````````````````````````````

Rebuild **Build Test (Scripts Only)**. Animals now use the same overlap and controller push pattern as players and zombies.
