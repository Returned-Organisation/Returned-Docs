.. _doc_returned_dashboard_open_hooks:

Dashboard Open Hooks
====================

Returned lets server plugins cancel opening the inventory, crafting, skills, or information (map) dashboard tabs. The hook uses the same ``ref bool shouldAllow`` pattern as craft and equip request handlers.

Overview
--------

When a player presses a dashboard hotkey or tab button, the owning client asks the server for permission. The server raises ``Player.onDashboardOpenRequested`` before telling the client to open the tab.

Level config flags such as ``Allow_Crafting``, ``Allow_Skills``, and ``Allow_Information`` still apply on both client and server. The plugin hook runs only when those checks already allow the tab.

Opening a tab that is already active (toggle close) stays local and does not call the server.

.. note::

	Remote clients wait one network round-trip before the dashboard appears after the server approves the request.

Server API
----------

.. code-block:: cs

	public enum EPlayerDashboardTab
	{
		Inventory,
		Crafting,
		Skills,
		Information
	}

	public delegate void DashboardOpenRequestedHandler(Player player, EPlayerDashboardTab tab, ref bool shouldAllow);

	// On Player:
	public static event DashboardOpenRequestedHandler onDashboardOpenRequested;

Set ``shouldAllow`` to ``false`` to cancel. Only the tab in the request is affected.

Example
-------

Block the map tab during a cutscene, but leave inventory usable:

.. code-block:: cs

	void OnEnable()
	{
		Player.onDashboardOpenRequested += OnDashboardOpenRequested;
	}

	void OnDisable()
	{
		Player.onDashboardOpenRequested -= OnDashboardOpenRequested;
	}

	void OnDashboardOpenRequested(Player player, EPlayerDashboardTab tab, ref bool shouldAllow)
	{
		if (tab == EPlayerDashboardTab.Information && isCutsceneActive)
		{
			shouldAllow = false;
		}
	}
