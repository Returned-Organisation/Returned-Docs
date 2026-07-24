.. _doc_returned_vehicle_carrying:

Vehicle Carrying and Moving Platforms
=====================================

Returned has three ways for one thing to carry another while moving. They look similar in-game but behave very
differently, so pick the one that matches your intent:

.. list-table::
	:header-rows: 1
	:widths: 22 20 20 38

	* - Model
	  - Carried thing
	  - Still driveable?
	  - Use for
	* - :ref:`Tow (Hook / Cargo) <doc_returned_vehicle_carrying:tow>`
	  - A vehicle
	  - No — locked to the tower
	  - Tow trucks, flatbeds that *hold* a wreck or disabled vehicle
	* - :ref:`Cargo-deck riding <doc_returned_vehicle_carrying:riding>`
	  - A vehicle
	  - Yes — physical and driveable
	  - Driving a car into a cargo plane / onto a ferry and having it move around on the deck
	* - :ref:`Moving platforms / elevators <doc_returned_vehicle_carrying:movers>`
	  - Players and vehicles
	  - N/A (the platform moves itself)
	  - Elevators, lifts, horizontal shuttles

All three build on the same networked *based movement* system that walking players use to ride vehicle platforms
(see :ref:`Allow_Whole_Vehicle_Platform <doc_assets_vehicle:allow_whole_vehicle_platform>`). Riders keep a
``baseNetId`` plus a base-relative pose, and observers rebuild the rider's world pose from the live base transform
instead of interpolating raw world snapshots. That is why a carried vehicle cannot be left behind or clip through the
carrier's walls when it moves.

.. _doc_returned_vehicle_carrying:tow:

Tow (Hook / Cargo)
------------------

A towed vehicle is **held rigidly** by the towing vehicle. While hooked it is kinematic: gravity, wheels, and buoyancy
are disabled and it rides the tower's ``Hook`` anchor frame exactly. It is not driveable in this state.

Authoring
~~~~~~~~~

Add a ``Hook`` transform to the towing vehicle's prefab. Its presence sets ``hasHook`` on the
:ref:`vehicle asset <doc_assets_vehicle>`:

.. code-block:: text

	TowTruckRoot/
	  Hook          <- attach point the towed vehicle is locked to

The towed vehicle needs no special authoring — any vehicle can be towed.

Behaviour notes
~~~~~~~~~~~~~~~

- The towed vehicle is put into a carried physics state (kinematic, gravity/wheels/buoyancy off) on the server and on
  clients, so it neither bounces against gravity nor emits ground tire particles while carried off the ground.
- Hull collision with the world is preserved, but the towed vehicle does not drive itself.
- Attach/detach is sent reliably, and hook ownership is restored for late-joining clients, so a client never keeps a
  vehicle glued to a tower that has already released it.

.. _doc_returned_vehicle_carrying:riding:

Cargo-deck riding (vehicle-on-vehicle)
--------------------------------------

A vehicle driven onto another vehicle's ride surface **stays fully physical and driveable**. It inherits the carrier's
motion through a base-relative reference frame, but its own engine, wheels, and hull collision keep working. This is the
"drive a car into the cargo plane and it moves around inside without phasing through the walls" case.

Authoring
~~~~~~~~~

The **carrier** (the vehicle being ridden on) needs ride surfaces, exactly like on-foot platform riding:

- Set :ref:`Allow_Whole_Vehicle_Platform <doc_assets_vehicle:allow_whole_vehicle_platform>` to ``true`` to make the
  whole vehicle rideable, **or**
- Add ``Platforms/Platform_#`` transforms with colliders on the ``Vehicle`` layer for specific ride surfaces.

The **carried** vehicle needs no special authoring. Wheeled vehicles attach from their wheel ground contact; other
vehicles attach from a short downward probe under the hull.

.. code-block:: unturneddat

	Allow_Whole_Vehicle_Platform true

Behaviour notes
~~~~~~~~~~~~~~~

- Attachment is detected from the carried vehicle's ground contact. A short ungrounded grace period keeps the reference
  frame while driving over deck seams and small ramps.
- The carried vehicle is carried by rigidly applying the carrier's per-tick motion delta with
  ``Rigidbody.MovePosition`` / ``MoveRotation``, so wall collision on the carrier still applies.
- A vehicle cannot be towed and ride a deck at the same time, and stacking cycles (A rides B rides A) are rejected.
- Server-side anti-teleport movement validation is relaxed while a driven vehicle is riding, so a fast carrier's motion
  is not misread as a speedhack.

.. _doc_returned_vehicle_carrying:movers:

Moving platforms / elevators
----------------------------

``ReturnedNetworkedMover`` is a first-class authoritative mover: the server drives a kinematic motion and streams the
pose to clients, which apply and interpolate it. It registers a networked movement base, so it carries **both** walking
players (through the on-foot ride path) and vehicles (through cargo-deck riding) automatically. Unlike a vehicle it is
not driveable and needs no seats or fuel.

Authoring
~~~~~~~~~

Attach ``ReturnedNetworkedMover`` to a GameObject that has:

- A collider — the surface players stand on and vehicles drive on. Put it on a layer riders can ground against (the
  ``Vehicle`` layer works for both players and vehicle wheels).
- A ``Rigidbody`` — added automatically; it is forced kinematic at runtime.

.. list-table::
	:header-rows: 1
	:widths: 22 78

	* - Field
	  - Meaning
	* - ``moverId``
	  - Unique per-map id (1..65535). Determines the shared NetId, so it **must** match across server and clients.
	    Leave ``0`` to disable the mover.
	* - ``mode``
	  - Motion profile. ``PingPong`` travels back and forth between the spawn pose and ``spawn + travelOffset``.
	* - ``travelOffset``
	  - Local-space offset of the far end of travel. e.g. ``(0, 5, 0)`` for a 5 m vertical elevator.
	* - ``moveSpeed``
	  - Travel speed in metres per second.
	* - ``pauseSeconds``
	  - Seconds to wait at each end before reversing.
	* - ``sendInterval``
	  - Seconds between authoritative pose broadcasts.

Behaviour notes
~~~~~~~~~~~~~~~

- The server is authoritative: it steps the motion in ``FixedUpdate`` and broadcasts the pose (including a resting-pose
  keepalive so late-joining clients converge). Clients never simulate the motion; they interpolate toward the received
  pose for smooth carrying.
- Movers claim their NetId deterministically from ``moverId`` in a reserved high range, so they never collide with the
  runtime spawn counter and both peers agree on the id without a spawn handshake.
- Riders resolve the mover from the collider they are standing / driving on, so no per-mover attach configuration is
  needed beyond the collider.

Server config
-------------

``Gameplay.Allow_Vehicle_Platform_Riding`` (see :ref:`vehicle assets <doc_assets_vehicle:allow_whole_vehicle_platform>`)
gates on-foot platform riding, cargo-deck vehicle riding, and mover riding together. Towing is always available.

Multiplayer notes
-----------------

- Cargo-deck ride state (``baseNetId`` + base-relative position and rotation) is replicated in the vehicle state stream,
  with a reliable attach/detach edge and late-join restore — the same reliability model as towing.
- Observers rebuild a riding vehicle's pose from the resolved base each frame instead of interpolating world snapshots,
  which prevents wall-clipping on a moving carrier.
- The local driver of a riding vehicle owns its own ride frame and ignores the server echo, avoiding prediction fights.
