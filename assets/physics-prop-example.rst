.. _doc_physics_prop_example:

Physics Prop Example (Soccer Ball)
==================================

Returned includes a minimal physics-prop object you can use as a template for bouncy, resettable props.

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Path
     - Purpose
   * - ``Assets/Game/Sources/Objects/Examples/Soccer_Ball_0/Soccer_Ball_0.dat``
     - **Tracked backup** — Medium object definition (ID **65500**)
   * - ``Assets/Game/Sources/Objects/Examples/Soccerball/Soccerball.dat``
     - **Tracked backup** — Sandbox Small definition (ID **65501**)
   * - ``Builds/Test/Bundles/Objects/Medium/Soccer_Ball_0/Soccer_Ball_0.dat``
     - Runtime copy (gitignored; wiped by Build Test / Steam sync)
   * - ``Builds/Test/Bundles/Objects/Medium/Soccer_Ball_0/Soccer_Ball_0.unity3d``
     - Legacy asset bundle (built from Unity, not master bundle)
   * - ``Builds/Test/Sandbox/Soccertest/Soccerball/``
     - Sandbox runtime copy + bundle

The ``.dat`` includes ``Exclude_From_Master_Bundle`` and ``Asset_Bundle_Version 6`` so Unturned loads the sibling ``Soccer_Ball_0.unity3d`` file instead of ``core.masterbundle``.

For property reference, see :ref:`doc_assets_object` (``Interactability Physics_Prop`` and ``Physics_Prop_`` properties).

Who can move a physics prop (``.dat`` flags)
--------------------------------------------

By default, **all sources are allowed**. Omit these keys for the soccer ball behaviour (players, zombies, animals, vehicles, melee, bullets, explosions).

**Allow list** — only these sources can move the prop:

.. code-block:: unturneddat

   Physics_Prop_Allowed Players, Zombies, Animals

**Deny list** — start from ``All``, then remove sources:

.. code-block:: unturneddat

   Physics_Prop_Denied Bullets, Explosions

**Per-source booleans** — override individual sources (can combine with allow/deny):

.. code-block:: unturneddat

   Physics_Prop_Allow_Players true
   Physics_Prop_Allow_Zombies false
   Physics_Prop_Allow_Animals true
   Physics_Prop_Allow_Vehicles true
   Physics_Prop_Allow_Melee true
   Physics_Prop_Allow_Bullets false
   Physics_Prop_Allow_Explosions false

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Source
     - What it covers
   * - ``Players``
     - Walking/sprinting into the prop
   * - ``Zombies``
     - Zombie movement push
   * - ``Animals``
     - Animal movement push
   * - ``Vehicles``
     - Vehicle collision push
   * - ``Melee``
     - Fists and melee weapons
   * - ``Bullets``
     - Gunfire
   * - ``Explosions``
     - Explosion blast force
   * - ``All``
     - Every source above

Example — players-only puzzle ball:

.. code-block:: unturneddat

   Interactability Physics_Prop
   Interactability_Reset 120
   Physics_Prop_Allowed Players

Example — horde toy zombies can kick but guns cannot:

.. code-block:: unturneddat

   Physics_Prop_Allowed Players, Zombies, Animals, Melee
   Physics_Prop_Denied Bullets

Workflow (legacy .unity3d)
--------------------------

#. **Open the Unity project** — Unity **2022.3.62f3**, then open ``Assets/GameStartup.unity``.
#. **Deploy .dat files** — **Window → Unturned → Deploy Soccer Ball .dat Files** (also runs automatically when you build a bundle). ``Builds/Test/`` is gitignored and gets wiped by **Build Test** / Steam sync; backups live under ``Assets/Game/Sources/Objects/Examples/``.
#. **Build the legacy bundle** — **Window → Unturned → Build Soccer Ball Legacy Bundle (Medium)**. This writes ``Builds/Test/Bundles/Objects/Medium/Soccer_Ball_0/Soccer_Ball_0.unity3d`` next to the ``.dat``.
#. **Build Test (Scripts Only)** — refresh ``Builds/Test/Unturned.exe`` if you changed code.
#. **Place in the level editor** — Run ``Builds/Test/Unturned.exe``, place **Soccer Ball** under **Medium** (ID **65500**).

For the **Sandbox** small variant: **Window → Unturned → Build Soccer Ball Legacy Bundle (Sandbox Small)**, then place **Soccerball** from the Sandbox asset origin (ID **65501**).

Alternatively, use **Window → Unturned → Bundle Tool**: select the ``Soccer_Ball_0`` source folder, grab assets, and save as ``Soccer_Ball_0.unity3d`` beside the ``.dat``.

Troubleshooting
---------------

**``missing "Object" GameObject``** — The ``.dat`` loaded but ``Soccer_Ball_0.unity3d`` is missing or does not contain a prefab named ``Object``. Re-run **Build Soccer Ball Legacy Bundle (Medium)**.

**``.dat`` files disappeared from ``Builds/Test/``** — Expected after **Build Test** or Steam sync. Run **Window → Unturned → Deploy Soccer Ball .dat Files**, or build a legacy bundle (which redeploys them automatically). Source copies are tracked in ``Assets/Game/Sources/Objects/Examples/``.

**Ball falls through ground** — Unturned's physics matrix only lets the **ITEM** layer collide with terrain. Physics props switch to ITEM at runtime. Rebuild scripts + legacy bundle (collider center fix).

**Ball doesn't react to punches, bullets, or explosions** — Rebuild **Build Test (Scripts Only)**. Melee, gun, and explosion hits apply impulses; vehicles and other colliders push via physics contact.

**Ball vibrates / won't move when pushed** — Rebuild scripts and re-export the legacy bundle if needed.

**Ball bounces up and down instead of rolling** — Rebuild **Build Test (Scripts Only)**. Ground contact now zeros vertical velocity and terrain snap no longer fights gravity on every frame.

**Ball collision does not match the visible sphere** — Rebuild the legacy bundle after prefab collider changes. Collider radius/center should match the mesh (Soccer Ball uses radius **0.5**, center **y: 0.5**).

**Ball barely moves when pushed or punched** — Rebuild scripts + legacy bundle. Push overlap, force multipliers, drag, and minimum melee impulse were tuned for a heavier rolling feel.

**Fists do not move the ball** — Rebuild **Build Test (Scripts Only)**. Default punch (``PlayerEquipment.punch``) now applies physics-prop impulse; only melee weapons did before.

**Animals do not move the ball** — Rebuild **Build Test (Scripts Only)**. Animals now use the same overlap + controller push pattern as players/zombies.
