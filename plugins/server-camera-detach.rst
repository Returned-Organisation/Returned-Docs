.. _doc_returned_server_camera_detach:

Server Camera Detach
====================

Returned lets a server force a player's local camera off the character to a world position and rotation, then re-attach it later. This is useful for cutscenes, dialogue framing, or scripted camera beats without enabling admin freecam.

Overview
--------

``PlayerLook`` already supports admin freecam and plugin allow-flags such as ``sendFreecamAllowed``. Server camera detach is separate:

- The server chooses the world pose.
- The owning client applies it and cannot override it with freecam or perspective keys.
- The player body keeps simulating (movement and look input still run).

Detach forces third-person parenting and locks the camera to the given world pose each frame. Attach clears that lock and restores normal first- or third-person parenting from the server's camera mode.

Cinematic bundle
----------------

For cutscenes that need more than a locked camera pose, ``sendServerCameraCinematicStart`` and ``sendServerCameraCinematicEnd`` apply and restore optional locks in one call:

.. list-table::
   :header-rows: 1

   * - Flag
     - Effect
   * - ``HideHud``
     - Hides gameplay HUD on the owning client.
   * - ``LockInput``
     - Ignores look input (same path as barricade placement).
   * - ``LockMovement``
     - Freezes the player at their current world position and rotation (restored on end).
   * - ``LockEquipment``
     - Enables cutscene mode (hides viewmodel, blocks item use).

``EServerCameraCinematicFlags.Default`` enables all four flags.

.. code-block:: cs

	player.look.sendServerCameraCinematicStart(worldPosition, yaw, pitch, EServerCameraCinematicFlags.Default);

	// Animate the camera by sending updated poses while cinematic is active:
	player.look.sendServerCameraDetach(newPosition, newYaw, newPitch);

	player.look.sendServerCameraCinematicEnd();

``sendServerCameraAttach`` also ends an active cinematic if one is running.

Server API
----------

Call these methods from server-side plugin code on the target ``Player``:

.. code-block:: cs

	player.look.sendServerCameraDetach(worldPosition, yaw, pitch);
	player.look.sendServerCameraAttach();
	player.look.sendServerCameraCinematicStart(worldPosition, yaw, pitch, EServerCameraCinematicFlags.Default);
	player.look.sendServerCameraCinematicEnd();

- ``worldPosition`` — world-space camera position.
- ``yaw`` / ``pitch`` — camera rotation in degrees (pitch is clamped to ``[-90, 90]``).

Only the owning client receives the RPC.

Client behaviour
----------------

While detached:

- Freecam hotkeys (Shift+F1–F5, Shift+F8) are ignored.
- Perspective toggle is ignored.
- Vehicle third-person orbit mouse input does not move the detached camera.
- Character pitch and yaw still update from normal look input.

While detached, network interest (regions, other players, vehicles) follows the detach pose the same way freecam interest follows the freecam camera. See :ref:`doc_returned_freecam_photomode`.

Lifecycle cleanup clears detach and cinematic automatically when:

- The player dies (movement lock, cutscene mode, HUD, input, and camera all reset).
- The player enters or leaves a vehicle seat.
- The camera returns to first-person through the normal perspective path.

Example
-------

Frame a target, then restore the camera:

.. code-block:: cs

	void ShowNpcCloseup(Player player, Transform npc)
	{
		Vector3 eye = npc.position + Vector3.up * 1.5f;
		Vector3 cameraPos = eye - npc.forward * 4f;
		Vector3 euler = Quaternion.LookRotation((eye - cameraPos).normalized).eulerAngles;

		player.look.sendServerCameraDetach(cameraPos, euler.y, euler.x);
	}

	void EndNpc(Player player)
	{
		player.look.sendServerCameraAttach();
	}
