.. _doc_data_earmortype:

EArmorType
==========

The ``EArmorType`` enumerated type controls which bullet calibers a worn clothing piece can stop. It works
alongside the existing ``Armor`` percentage on :ref:`clothing assets <doc_item_clothing_slots>`. The
``Armor`` percentage still decides how much melee and zombie damage the piece reduces; the armor type
decides what gunfire it blocks. It is authored with the ``Armor_Type`` property.

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
     - Default. No caliber stop; only the ``Armor`` percentage applies. Existing clothing keeps its current behaviour.
   * - ``Light``
     - 1
     - No caliber stop, authored explicitly so descriptions can communicate the intended tier.
   * - ``Medium``
     - 2
     - Stops pistol-tier and lower calibers. Rifle-tier and above penetrate.
   * - ``Heavy``
     - 3
     - Stops rifle-tier and lower calibers. Higher calibers penetrate per weapon configuration.

See :ref:`doc_item_clothing_slots` for how armor stacks across worn pieces.
