.. _doc_data_eanimalbehaviour:

EAnimalBehaviour
================

The ``EAnimalBehaviour`` enumerated type controls how an :ref:`animal asset <doc_assets_animal>` reacts to nearby players and to damage.

Enumerators
```````````

.. list-table::
   :widths: 20 10 70
   :header-rows: 1

   * - Named Value
     - Index
     - Description
   * - ``None``
     - 0
     - No special behaviour. Treated like ``Defense`` when damaged.
   * - ``Offense``
     - 1
     - Proactively hunts players who enter alert range, and attacks when damaged.
   * - ``Defense``
     - 2
     - Flees when alerted or damaged.
   * - ``Counter``
     - 3
     - **Returned fork.** Ignores nearby players until damaged, then attacks the attacker. Does not proactively hunt from footstep or gunshot alerts.
   * - ``Ignore``
     - 4
     - Flees when damaged. Does not proactively hunt.

Returned fork notes
```````````````````

``Counter`` is intended for animals that should appear passive until provoked — for example, the **Capelobo** from the Rio de Janeiro map (ID **36085**). In the retail map it uses ``Offense``; setting ``Behaviour Counter`` makes it ignore players until attacked.

When a ``Counter`` animal takes damage from a player (melee, gunfire, punch, etc.), ``Animal.alertDamagedByPlayer`` targets that player. ``DamageTool.damageAnimal`` routes player-instigated damage through this path when ``AlertPosition`` is set.

.. code-block:: unturneddat

   Behaviour Counter

See :ref:`doc_assets_animal` for other animal properties.
