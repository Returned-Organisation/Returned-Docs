.. _doc_data_eanimalbehaviour:

EAnimalBehaviour
================

The ``EAnimalBehaviour`` enumerated type controls how an :ref:`animal asset <doc_assets_animal>` reacts to nearby players and to damage. Roaming combat NPCs reuse the same enum via the ``Aggression`` property (see :ref:`doc_npcs_roaming`).

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
     - Ignores nearby players until damaged, then attacks the attacker.
   * - ``Ignore``
     - 4
     - Flees when damaged. Does not proactively hunt.

Counter Behaviour
`````````````````

``Counter`` is intended for animals that should appear passive until provoked.

Unlike ``Offense`` animals, ``Counter`` animals are not alerted by nearby players or gunshots. They only become hostile after taking damage. When damaged by a player, the animal targets that player through ``Animal.alertDamagedByPlayer``. ``DamageTool.damageAnimal`` routes player-instigated damage through this path when ``AlertPosition`` is set.

The **Capelobo** on the Rio de Janeiro map (ID **36085**) is a useful example. In the retail map it uses ``Offense``; setting ``Behaviour Counter`` makes it ignore players until attacked:

.. code-block:: unturneddat

	Behaviour Counter

See :ref:`doc_assets_animal` for other animal properties.
