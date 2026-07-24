// Collapsible sidebar TOC for Groundwork (captions + nested page trees).

document.addEventListener("DOMContentLoaded", () => {
	const sidebar = document.querySelector(".sphinxsidebarwrapper");
	if (!sidebar) {
		return;
	}

	const isCurrentBranch = (element) =>
		Boolean(
			element.classList.contains("current") ||
				element.querySelector(
					":scope > a.current, :scope li.current, :scope a.current"
				)
		);

	const setExpanded = (toggle, list, expanded) => {
		toggle.classList.toggle("expanded", expanded);
		list.classList.toggle("expanded", expanded);
	};

	// Top-level section captions (About, Returned, …)
	sidebar.querySelectorAll("p.caption").forEach((caption) => {
		const list = caption.nextElementSibling;
		if (!list || list.tagName !== "UL") {
			return;
		}

		caption.classList.add("toc-toggle");
		caption.setAttribute("role", "button");
		caption.setAttribute("tabindex", "0");
		list.classList.add("toc-collapse");
		setExpanded(caption, list, isCurrentBranch(list));

		const toggleCaption = () => {
			setExpanded(caption, list, !list.classList.contains("expanded"));
		};

		caption.addEventListener("click", toggleCaption);
		caption.addEventListener("keydown", (event) => {
			if (event.key === "Enter" || event.key === " ") {
				event.preventDefault();
				toggleCaption();
			}
		});
	});

	// Page entries with in-page heading children
	sidebar.querySelectorAll("li.toctree-l1").forEach((item) => {
		const childList = item.querySelector(":scope > ul");
		const link = item.querySelector(":scope > a");
		if (!childList || !link) {
			return;
		}

		item.classList.add("toc-branch");
		childList.classList.add("toc-collapse");

		const button = document.createElement("button");
		button.type = "button";
		button.className = "toc-expand";
		button.setAttribute("aria-label", "Toggle section");
		item.insertBefore(button, link);

		const expand = isCurrentBranch(item);
		setExpanded(item, childList, expand);
		button.setAttribute("aria-expanded", expand ? "true" : "false");

		button.addEventListener("click", (event) => {
			event.preventDefault();
			event.stopPropagation();
			const next = !childList.classList.contains("expanded");
			setExpanded(item, childList, next);
			button.setAttribute("aria-expanded", next ? "true" : "false");
		});
	});
});
