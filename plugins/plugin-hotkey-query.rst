.. _doc_returned_plugin_hotkey_query:

Plugin Hotkey Query
===================

Returned lets a server ask a player's client for the ``KeyCode`` bindings of the five plugin hotkeys. Use this when a plugin needs the actual bound keys (for logging, conditional logic, or custom UI) rather than only whether a key is currently held.

Overview
--------

Returned already exposes plugin hotkey **held state** on the server through ``PlayerInput.onPluginKeyTick`` and ``PlayerInput.IsPluginKeyHeld``. Those APIs do not include the bound ``KeyCode``.

Returned adds an asynchronous query:

1. The server calls ``player.input.queryPluginKeyCodes``.
2. The owning client reads ``ControlsSettings.getPluginKeyCode`` for indices ``0``–``4``.
3. The client relays the five ``KeyCode`` values back to the server.
4. The server caches them, invokes the optional callback, and raises ``PlayerInput.onPluginKeyCodesReceived``.

For display-only text in chat or UI effects, prefer the existing ``<plugin_0/>`` … ``<plugin_4/>`` tokens. The client replaces those locally without a server round-trip.

Server API
----------

.. code-block:: cs

	public delegate void PluginKeyCodesReadyHandler(Player player, KeyCode[] keyCodes);

	// On PlayerInput:
	public static PluginKeyCodesReadyHandler onPluginKeyCodesReceived;

	player.input.queryPluginKeyCodes(callback: null);

	bool hasCache = player.input.HasCachedPluginKeyCodes;
	KeyCode[] copy = player.input.GetCachedPluginKeyCodes();
	bool ok = player.input.TryGetCachedPluginKeyCode(index, out KeyCode keyCode);

- ``keyCodes`` length is ``ControlsSettings.NUM_PLUGIN_KEYS`` (``5``).
- Index ``0`` is plugin key 0 (``<plugin_0/>``), through index ``4``.
- ``queryPluginKeyCodes`` is server-only and must run on the game thread.
- The reply is asynchronous on remote clients (one network round-trip). On a listen-server host, the reply is handled locally in the same call path.

Example
-------

Query a player's bindings and log them:

.. code-block:: cs

	void OnEnable()
	{
		PlayerInput.onPluginKeyCodesReceived += OnPluginKeyCodesReceived;
	}

	void OnDisable()
	{
		PlayerInput.onPluginKeyCodesReceived -= OnPluginKeyCodesReceived;
	}

	void QueryBindings(Player player)
	{
		player.input.queryPluginKeyCodes((Player queriedPlayer, KeyCode[] keyCodes) =>
		{
			for (int i = 0; i < keyCodes.Length; i++)
			{
				UnturnedLog.info($"Plugin key {i}: {keyCodes[i]}");
			}
		});
	}

	void OnPluginKeyCodesReceived(Player player, KeyCode[] keyCodes)
	{
		// Optional global listener for every successful query.
	}

Limitations
-----------

- The cache is per player session. It is not persisted across reconnects.
- Rebinding controls on the client does not push an update. Call ``queryPluginKeyCodes`` again when you need fresh values.
- Clients can report any ``KeyCode`` integers. Treat the values as untrusted display or logic input.
