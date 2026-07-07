.. _doc_vehicle_platform_riding:

Vehicle Platform Riding
=====================

Walking players can stand on moving vehicle surfaces in multiplayer when the vehicle prefab defines platform geometry, or when whole-vehicle riding is enabled in the ``.dat`` file.

.. note::

	Vehicle platform riding is a Returned fork feature.

Prefab Setup
------------

Add a ``Platforms`` folder to the vehicle prefab hierarchy:

.. code-block:: text

	VehicleRoot/
	  Platforms/
	    Platform_0
	    Platform_1
	  Seats/
	    Seat_0

Each ``Platform_#`` transform should have a collider (BoxCollider recommended) on the **VEHICLE** layer. Riders are parented to the matching platform transform for network sync.

Vehicle .dat Options
--------------------

**Allow_Whole_Vehicle_Platform** *bool*: When ``true``, any vehicle collider can be ridden (not just ``Platform_#`` surfaces). Defaults to ``false``.

Truck bed only (default):

.. code-block:: unturneddat

	Allow_Whole_Vehicle_Platform false

Allow standing anywhere on the hull:

.. code-block:: unturneddat

	Allow_Whole_Vehicle_Platform true

See :ref:`doc_assets_vehicle` for other vehicle properties.

Server Config
-------------

``Gameplay.Allow_Vehicle_Platform_Riding`` in the server gameplay config toggles the feature globally. Defaults to ``true``.

Multiplayer Test Checklist
--------------------------

1. Run **Build Test (Scripts Only)** after code changes.
2. Run **Window > Unturned > Net Gen > Generate** if you add or change RPCs.
3. Listen-server test with two clients: driver and rider on ``Platform_0`` through turns and braking.
4. Confirm remote clients see the rider move with the vehicle without sliding.
