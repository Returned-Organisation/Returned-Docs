.. _doc_returned_freelook:

Freelook
========

Hold **Freelook** (default ``Caps Lock``, rebindable in Controls) to look around without turning the body. The third-person head follows that peek and is synced for other players.

Behaviour
---------

- **First-person:** mouse moves the **camera** (and synced head) within about ±75° yaw and pitch relative to the body. The camera is sphere-cast against colliders so it cannot pass through walls or other blocking geometry.
- **Third-person:** mouse moves the **head only**; the camera stays behind the body.
- **Vehicles:** hold-to-freelook is **disabled**. Looking around in a seat already moves the camera; the head is synced to that look yaw/pitch (clamped to about ±75°) so other players see it.
- **Weapons:** freelook is **disabled** while a gun or melee is equipped (shots use screen center; peeking would desync aim from crosshair).
- **Aim / other useables:** when freelook is allowed, aim stays body-facing. Equipped items are not put away.
- **Hands / arms:** stay on the body; only the head turns.
- **Movement:** unchanged — you can walk and sprint while freelooking.
- **On release:** camera/head snap back to body forward.
- **Availability:** on foot when look input is active, except with a gun/melee equipped. Inactive in vehicles/seats, and when the game already ignores look input (for example menus or key rebinding).

Controls
--------

The bind appears under the Stance layout in the controls menu as **Freelook**. Default key is ``Caps Lock``.
