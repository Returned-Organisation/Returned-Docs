.. _doc_npcs_roaming:

Roaming NPCs
============

Roaming NPCs pathfind on dedicated **NPC** navigation meshes, wander between spawn points, and pause in place while a player talks to them. With ``Can_Combat true``, they also fight using animal-style aggression, a Primary/Secondary/Tertiary loadout, limited ammo, clothing armor, and optional loot on death.

Authoring overview
------------------

1. In the level editor, open **Environment → Navigation**.
2. Place a Flag and set **Mesh Type** to ``NPC`` (cyan volume). Zombie flags stay ``Zombie`` (default).
3. Click **Bake Navigation** once to commit the flag bounds (clears the “has not been baked yet” save warning).
4. **Save the level** so ``Bounds.dat`` is written. Returned rebuilds the Unity NavMesh on **Play / Host** (watch the console for ``NavMesh baked`` / ``NavMesh rebuild finished``). There is no ASPFP ``Navigation_N.dat`` bake.
5. Place the NPC in either of these ways (both require ``Can_Roam true`` and an **NPC** navmesh):

   - **Objects** (simple): enable the **NPCs** filter, place the ``Type NPC`` object inside the cyan volume, Save, then Play/Host. Returned converts it into a roaming NPC at runtime.
   - **Spawns → NPCs**: search/select the asset, click **Add**, place points inside the NPC navmesh. **Each spawn point creates one roaming NPC.** With a single point, the NPC wanders to random positions on that navmesh; add more points if you want more copies of the same character.

.. note::
   A static Objects placement without ``Can_Roam``, or outside an NPC navmesh, will not walk. Console line ``Roaming NPCs spawned: 0`` means nothing eligible was found.

NPC object asset properties
---------------------------

Add these keys to a ``Type NPC`` object asset (see :ref:`doc_object_asset_npc`):

Roaming
```````

**Can_Roam** *bool*: When true, level NPC spawn points for this asset create a roaming NPC. Defaults to false (static placed NPCs are unchanged).

**Speed_Walk** *float*: Walk speed while roaming. Defaults to ``3.5``.

**Roam_Idle_Min** *float*: Minimum seconds to wait between roam destinations. Defaults to ``2``.

**Roam_Idle_Max** *float*: Maximum seconds to wait between roam destinations. Defaults to ``8``.

**Interactable_While_Roaming** *bool*: When true (default), players can talk to the NPC while it is walking. When false, talk is only available while idle or already in dialogue.

Combat
``````

**Can_Combat** *bool*: Opt-in combat AI. Requires ``Can_Roam``. Defaults to false.

**Aggression** *enum* (:ref:`doc_data_eanimalbehaviour`): ``Offense``, ``Defense``, ``Counter``, or ``Ignore``. Defaults to ``Ignore``.

**Detection_Radius** *float*: Fixed detection radius in meters. ``0`` (default) uses the player stealth radius from ``AlertTool``.

**Combat_Leash_Radius** *float*: Max chase distance from spawn/home. Defaults to ``48``.

**Target_Lost_Radius** *float*: Drop target beyond this distance. Defaults to ``64``.

**Speed_Run** *float*: Chase and flee speed. Defaults to ``7``.

**Health** *uint16*: Max HP. Defaults to ``100``.

**Can_Die** *bool*: When false, health cannot reach zero. Defaults to true.

**Invulnerable** *bool*: Ignore player damage. Defaults to false.

**Respawn_Time** *float*: Seconds to respawn after death. ``0`` = no respawn. Defaults to ``300``.

**Combat_Reset_Delay** *float*: Seconds after full disengage before restoring health, ammo, clothing quality, and default held slot. Defaults to ``30``.

**Melee_Damage** *byte*: Unarmed / fallback melee damage. Defaults to ``15``.

**Melee_Range** *float*: Horizontal melee range. Defaults to ``2.25``.

**Melee_Vertical_Range** *float*: Vertical melee range. Defaults to ``2``.

**Melee_Interval** *float*: Seconds between melee attacks. Defaults to ``1``.

**Alert_On_Gunshot** *bool*: Offense NPCs investigate gunshot noise. Defaults to true.

**Hostile_Reputation_Below** *int*: Opt-in. When present, auto-aggro (or flee if Defense) players whose global reputation is below this value. Omitted = disabled. Uses ``PlayerSkills.reputation`` (see Reputation conditions/rewards).

**Ranged_Preferred_Min** / **Ranged_Preferred_Max** *float*: Legacy authoring hints. Engage stand-off is driven primarily by the held gun's ``Range`` (~28–72% of weapon range).

**Combat_Accuracy** *float*: Spread multiplier knob. Lower = tighter shots. Defaults to ``1``. Clamped roughly ``0.25``–``2.5``.

**Combat_Reaction** *float*: Scales aim-settle, suppression, investigate, and related timings. Lower = snappier. Defaults to ``1``.

**Combat_Cover_IQ** *float*: Higher = shorter open gunfights before cover and longer hides. Defaults to ``1``.

**Squad_Id** *string*: When set, only NPCs sharing this id coordinate (shared aggro, Pin/FlankHigh/Flank roles). Empty = proximity squads using ``Squad_Share_Radius``.

**Squad_Share_Radius** *float*: Proximity squad radius when ``Squad_Id`` is empty. Defaults to ``48``.

**Ally_Death_Alert_Radius** *float*: Squad mates within this distance react when an ally dies. Defaults to ``32``.

**Weapon_Swap_Cooldown** *float*: Seconds between loadout swaps. Defaults to ``0.75``.

**Primary_Ammo** / **Secondary_Ammo** / **Tertiary_Ammo** *uint16*: Starting rounds per gun slot (split into magazine + reserve from ``Ammo_Max``).

**Infinite_Ammo** *bool*: Guns never empty. Defaults to false.

**Loot_ID** *uint16*: Spawn table for death drops (same resolver as animal ``Reward_ID``).

**Loot_Min** / **Loot_Max** *int*: Drop count range.

**Loot_Chance** *float*: Applied when the rolled drop count is one. Defaults to ``1``.

**Drop_Equipped_Weapons** *bool*: Drop remaining Primary/Secondary/Tertiary items on death.

Use existing **Primary** / **Secondary** / **Tertiary** / **Equipped** keys for the combat loadout. Any slot may be a gun, melee, or throwable. The AI:

- Swaps by engage band and by what the player is holding (melee vs gun match).
- Reloads empty magazines (``Reload_Time`` / hammer rules), ducking to cover instead of dry-firing.
- Smoke (non-explosive distraction): when health drops below about half, throw smoke to screen a retreat **only if** a complete flee path exists that moves them meaningfully away from the threat. Cornered NPCs keep fighting instead of smoking into a dead end.
- Frag (explosive): when the target is unreachable (other floor / no LOS) and far enough to avoid cooking themselves, lob toward the target. Skips the throw if another combat NPC is inside the blast radius. Not used at point-blank.

Dialogue and interaction
------------------------

Roaming NPCs use the same dialogue, conditions, and vendors as static NPCs. When a player starts talking, the NPC stops pathfinding and holds position. When dialogue ends (or the player walks away), roaming resumes after an idle delay.

While the NPC is hostile (fighting, fleeing from a player threat, or otherwise in combat), new dialogue requests are **blocked**.

Combat behaviour
----------------

Aggression matches animals (:ref:`doc_data_eanimalbehaviour`), with Returned deltas:

- **Group / squad aggro:** damage and stealth/reputation entry mark the attacker. Squad mates (``Squad_Id`` or proximity) share targets. Roles are sticky by instance order: **Pin** (first engager — pressure the last-known side), **FlankHigh** (one mate — seek an elevated firing perch), **Flank** (others — wrap the opposite side).
- **Reputation hostility:** optional ``Hostile_Reputation_Below`` auto-engages low-rep players.
- **Defense** flees like animals (does not chase).
- **Clothing** from the NPC outfit applies player-like armor and movement speed multipliers.
- **Suppression:** taking hits aborts peeks, delays the next shot, widens spread briefly, flinches aim, and plays flesh/blood impact FX (same ``Flesh_Dynamic`` path as players/zombies). Hitmarkers register on living roaming NPCs.
- **Cover push:** when LOS is lost, armed gunners first hold / peek / shoot from cover for a beat; if the block persists (about 1.5–2 s) they reposition to a lateral firing angle (flank-wrap or same-floor orbit) at their preferred range instead of standing still or charging you. Repositions stay outside their minimum stand-off — they walk when closing and only run sideways / away — and never path onto the player transform while a usable gun remains. If LOS reopens mid-move they plant and fire. Only dry-ammo or melee commits actually chase. FlankHigh may climb to another elevated perch after a longer LOS block (about 6 s).
- **Last-known / deaggro:** losing sight hunts the last seen position. Hostility persists while the player stays on the **NPC** navmesh within leash; leaving that mesh for a few seconds ends the fight (after a short hunt). Cover alone does not clear aggro.
- **Ally death:** nearby squad mates investigate or engage the killer.
- **Animals / zombies:** NPC gunfire pulls offense animals and zombies onto the shooter (not onto other NPCs). Combat NPCs fight back with the same loadout; animals and zombies can damage them in return. Roamers never target or friendly-fire each other — noise investigate only reacts when a player is near the sound.
- **Weapon match:** if you pull a melee in punching range, they may knife and close; if you hold a gun, they keep firearms and hold range. Empty mag+reserve can trigger a melee push.
- After combat ends, ``Combat_Reset_Delay`` restores health, ammo, and clothing quality.

Ranged NPCs fight in a band derived from gun ``Range``, fire hitscan shots (server-authoritative), peek from hard cover with player-style Q/E lean, and plant to shoot when they have LOS. Looking away / breaking LOS does not make them charge — they hold, then reposition for a clear angle, and keep fighting. Death cause for players killed by NPCs is ``NPC``.

Navigation notes
----------------

- Do not rely on zombie Flags for roaming NPCs. Use ``Mesh Type NPC``.
- Zombie spawn points are ignored when they fall inside NPC-only bounds.
- Animals may use the NPC agent when animal pathfinding is enabled; zombie pathfinding never uses NPC surfaces.
- Roaming NPCs climb tagged ``Ladder`` colliders like players when their destination or combat target is on another floor (navmesh still will not bridge floors by itself). Melee NPCs climb to close. Gunners with a usable firearm stay on their floor, hold range, and orbit for a clear shot instead of ladder-rushing into you; if this floor has no LOS, the **FlankHigh** squad mate may climb to a **second elevated firing perch** (another roof with a clear shot, not into your face). Other gunners keep orbiting on their floor. Fleeing can still use ladders. They prefer the live threat/follow height over same-floor nav samples (elevated-vantage goals override threat height), continue across stacked ladder segments, step onto the deck at the top, and prefer climbing down rather than jumping. Only one NPC climbs a given ladder at a time; others soft-wait on staggered approach points without treating idle as stuck, and if they stop making progress while the ladder is free they sidestep / re-approach or briefly abandon that ladder. Climbs abort if the threat dies or deaggros mid-ladder. Hard falls deal bone damage and can break their legs (walk-only until regen, same mode rules as players). They cannot shoot, melee, or throw while climbing or walking to a ladder.

.. code-block:: unturneddat

   GUID 0123456789abcdef0123456789abcdef
   Type NPC
   ID 9001

   Dialogue a1b2c3d4e5f60718293a4b5c6d7e8f90

   Can_Roam true
   Speed_Walk 3.5
   Roam_Idle_Min 2
   Roam_Idle_Max 8
   Interactable_While_Roaming true

   Can_Combat true
   Aggression Offense
   Hostile_Reputation_Below 0
   Health 120
   Speed_Run 7
   Combat_Reset_Delay 30
   Combat_Accuracy 1
   Combat_Reaction 1
   Combat_Cover_IQ 1
   Squad_Id Patrol_Alpha

   Primary <rifle_guid>
   Secondary <pistol_guid>
   Tertiary <grenade_or_melee_guid>
   Equipped Primary
   Primary_Ammo 90
   Secondary_Ammo 48

   Loot_ID <spawn_table_id>
   Loot_Min 1
   Loot_Max 3
