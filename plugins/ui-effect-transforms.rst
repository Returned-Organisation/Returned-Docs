.. _doc_returned_ui_effect_transforms:

UI Effect Duplicate, Move, and Resize
=====================================

Returned extends ``EffectManager`` so plugins can duplicate a **named child** inside an existing keyed UI effect, then move or resize that child (or the effect root) without re-sending the whole prefab.

Overview
--------

Keyed UI effects use the same plugin UI system as vanilla Returned (``SendUIEffect``, ``sendUIEffectText``, ``sendUIEffectVisibility``, ``sendUIEffectImageURL``, and related APIs). Returned adds three server methods on top of that:

- **Duplicate** — clone one named child under the same keyed UI and give the clone a new sibling name.
- **Position** — set ``RectTransform.anchoredPosition`` on a named child, or on the effect root.
- **Size** — set ``RectTransform.sizeDelta`` on a named child, or on the effect root.

Child lookup matches text and visibility: ``Transform.Find`` first, then a recursive name search.

After you duplicate a child, change it with the normal text, visibility, and image APIs using the destination name (for example ``Row_1/Label``).

Server API
----------

All methods take an ``ITransportConnection`` for the target client, the same as ``sendUIEffectText``.

Duplicate
`````````

.. code-block:: cs

	EffectManager.sendUIEffectDuplicate(
		key,
		transportConnection,
		reliable: true,
		sourceChildNameOrPath: "Row",
		destChildName: "Row_1"
	);

Behaviour:

- Finds ``sourceChildNameOrPath`` under the keyed UI.
- Instantiates a sibling under the same parent.
- Renames the clone to ``destChildName`` and places it immediately after the source.
- Replaces any existing sibling that already uses ``destChildName``.
- Preserves the source child's current text, visibility, image URLs, and layout on the clone.

``destChildName`` is a sibling **name**, not a nested path. It must differ from the source name.

Position
````````

.. code-block:: cs

	// Named child
	EffectManager.sendUIEffectPosition(key, transportConnection, reliable: true, "Panel/Title", x: 40f, y: -20f);

	// Effect root (null or empty path)
	EffectManager.sendUIEffectPosition(key, transportConnection, reliable: true, "", x: 0f, y: 50f);

Sets ``RectTransform.anchoredPosition``.

Size
````

.. code-block:: cs

	// Named child
	EffectManager.sendUIEffectSize(key, transportConnection, reliable: true, "Panel", width: 320f, height: 180f);

	// Effect root (null or empty path)
	EffectManager.sendUIEffectSize(key, transportConnection, reliable: true, "", width: 800f, height: 600f);

Sets ``RectTransform.sizeDelta``.

Changing a duplicated child
---------------------------

Duplicate does not create a second keyed effect. The clone stays under the same ``key``. Target it by the destination name:

.. code-block:: cs

	EffectManager.sendUIEffectText(key, transportConnection, reliable: true, "Row_1/Label", "Player B");
	EffectManager.sendUIEffectVisibility(key, transportConnection, reliable: true, "Row_1/Icon", true);
	EffectManager.sendUIEffectPosition(key, transportConnection, reliable: true, "Row_1", 0f, -80f);
	EffectManager.sendUIEffectSize(key, transportConnection, reliable: true, "Row_1", 320f, 48f);

Missing keys or children fail quietly (logged on the client), matching ``sendUIEffectText`` and ``sendUIEffectVisibility``.

Limitations
-----------

- Duplicate clones a child inside one keyed UI. It does not spawn a second effect under a new key.
- ``destChildName`` must be a sibling name under the source's parent.
- Position and size are anchor-relative (``anchoredPosition`` / ``sizeDelta`` only). There is no API to change ``anchorMin`` / ``anchorMax`` in this version.
- Position and size require a ``RectTransform`` (normal uGUI / TextMesh Pro UI).

Example
-------

Show a UI, clone a row, then move and relabel the clone:

.. code-block:: cs

	const short Key = 1001;

	EffectManager.SendUIEffect(hudAsset, Key, transportConnection, reliable: true);
	EffectManager.sendUIEffectText(Key, transportConnection, reliable: true, "Row/Label", "Player A");

	EffectManager.sendUIEffectDuplicate(Key, transportConnection, reliable: true, "Row", "Row_1");
	EffectManager.sendUIEffectPosition(Key, transportConnection, reliable: true, "Row_1", 0f, -80f);
	EffectManager.sendUIEffectText(Key, transportConnection, reliable: true, "Row_1/Label", "Player B");

Stack several rows for a list:

.. code-block:: cs

	for (int i = 1; i < labels.Length; i++)
	{
		string destName = "Row_" + i;
		EffectManager.sendUIEffectDuplicate(Key, transportConnection, reliable: true, "Row", destName);
		EffectManager.sendUIEffectPosition(Key, transportConnection, reliable: true, destName, 0f, -i * 36f);
		EffectManager.sendUIEffectText(Key, transportConnection, reliable: true, destName + "/Label", labels[i]);
	}
