(() => {
  "use strict";

  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));
  const boot = window.SITE_BOOT || {};
  const state = { index: [], selected: 0, query: "" };

  const toast = (() => {
    const node = document.createElement("div");
    node.className = "toast";
    node.setAttribute("role", "status");
    node.setAttribute("aria-live", "polite");
    document.body.appendChild(node);
    let timer = 0;
    return (message) => {
      node.textContent = message;
      node.classList.add("show");
      window.clearTimeout(timer);
      timer = window.setTimeout(() => node.classList.remove("show"), 1900);
    };
  })();

  function setupNavigation() {
    const toggle = $("[data-nav-toggle]");
    const closeTargets = $$('[data-nav-close]');
    const close = () => {
      document.body.classList.remove("nav-open");
      toggle?.setAttribute("aria-expanded", "false");
    };
    toggle?.addEventListener("click", () => {
      const open = !document.body.classList.contains("nav-open");
      document.body.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", String(open));
    });
    closeTargets.forEach((node) => node.addEventListener("click", close));
    $$(".primary-nav a").forEach((link) => link.addEventListener("click", close));
    window.addEventListener("resize", () => {
      if (window.innerWidth > 940) close();
    });
    return close;
  }

  function setupReadingProgress() {
    const bar = $("#reading-progress-bar");
    if (!bar) return;
    const update = () => {
      const max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
      const pct = Math.max(0, Math.min(100, (window.scrollY / max) * 100));
      bar.style.width = `${pct}%`;
    };
    update();
    document.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update, { passive: true });
  }

  function setupHeadingLinks() {
    $$("[data-article] h2[id], [data-article] h3[id]").forEach((heading) => {
      const link = document.createElement("a");
      link.className = "heading-link";
      link.href = `#${heading.id}`;
      link.setAttribute("aria-label", `Link to ${heading.textContent.trim()}`);
      link.textContent = "#";
      link.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(`${location.href.split("#")[0]}#${heading.id}`);
          toast("Section link copied");
        } catch (_) {
          // Navigation still works even when clipboard permission is unavailable.
        }
      });
      heading.prepend(link);
    });
  }

  function setupTocObserver() {
    const links = $$(".page-toc a[href^='#']").filter((a) => a.getAttribute("href") !== "#main");
    if (!links.length || !("IntersectionObserver" in window)) return;
    const byId = new Map(links.map((link) => [link.getAttribute("href").slice(1), link]));
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
        if (!visible) return;
        links.forEach((link) => link.classList.remove("is-active"));
        byId.get(visible.target.id)?.classList.add("is-active");
      },
      { rootMargin: "-18% 0px -68% 0px", threshold: [0, 1] }
    );
    byId.forEach((_, id) => {
      const heading = document.getElementById(id);
      if (heading) observer.observe(heading);
    });
  }

  function setupCodeCopy() {
    $$(".code-copy").forEach((button) => {
      button.addEventListener("click", async () => {
        const pre = button.closest("pre");
        const code = pre?.querySelector("code")?.textContent || "";
        try {
          await navigator.clipboard.writeText(code);
          button.textContent = "Copied";
          toast("Code copied");
          window.setTimeout(() => (button.textContent = "Copy"), 1300);
        } catch (_) {
          toast("Clipboard permission unavailable");
        }
      });
    });
  }

  async function loadSearchIndex() {
    if (state.index.length || !boot.searchIndex) return state.index;
    try {
      const response = await fetch(boot.searchIndex, { cache: "no-store" });
      if (!response.ok) throw new Error(`Search index ${response.status}`);
      state.index = await response.json();
    } catch (error) {
      console.warn("Search index unavailable", error);
      state.index = [];
    }
    return state.index;
  }

  function scoreResult(item, query) {
    if (!query) return 1;
    const q = query.toLowerCase();
    const title = item.title.toLowerCase();
    const headings = (item.headings || []).join(" ").toLowerCase();
    const description = item.description.toLowerCase();
    const text = (item.text || "").toLowerCase();
    let score = 0;
    if (title === q) score += 90;
    if (title.startsWith(q)) score += 48;
    if (title.includes(q)) score += 30;
    if (headings.includes(q)) score += 18;
    if (description.includes(q)) score += 12;
    if (text.includes(q)) score += 3;
    q.split(/\s+/).filter(Boolean).forEach((token) => {
      if (title.includes(token)) score += 10;
      if (headings.includes(token)) score += 5;
      if (description.includes(token)) score += 3;
    });
    return score;
  }

  function setupSearch(closeNav) {
    const dialog = $("#command-dialog");
    const query = $("#command-query");
    const results = $("#command-results");
    const openers = $$('[data-search-open]');
    const closer = $("[data-search-close]");
    if (!dialog || !query || !results) return;

    const render = () => {
      const q = state.query.trim();
      const ranked = state.index
        .map((item) => ({ item, score: scoreResult(item, q) }))
        .filter((row) => row.score > 0)
        .sort((a, b) => b.score - a.score || a.item.title.localeCompare(b.item.title))
        .slice(0, 12);
      state.selected = Math.min(state.selected, Math.max(0, ranked.length - 1));
      if (!ranked.length) {
        results.innerHTML = '<div class="command-empty">No matching page. Try a mechanism, gate, evidence state, or visitor goal.</div>';
        return;
      }
      results.innerHTML = ranked
        .map(({ item }, index) => `
          <button class="command-result${index === state.selected ? " is-selected" : ""}" type="button" role="option" aria-selected="${index === state.selected}" data-result="${item.route}">
            <span><strong>${escapeHtml(item.title)}</strong><span>${escapeHtml(item.description)}</span></span>
            <small>${escapeHtml(boot.site || "site")}</small>
          </button>`)
        .join("");
      $$("[data-result]", results).forEach((button) => {
        button.addEventListener("click", () => navigateTo(button.dataset.result));
      });
      $(".command-result.is-selected", results)?.scrollIntoView({ block: "nearest" });
    };

    const open = async () => {
      closeNav?.();
      await loadSearchIndex();
      state.query = "";
      state.selected = 0;
      query.value = "";
      render();
      if (!dialog.open) dialog.showModal();
      window.setTimeout(() => query.focus(), 20);
    };
    const close = () => {
      if (dialog.open) dialog.close();
    };
    const navigateTo = (route) => {
      close();
      const prefix = boot.route ? "../" : "";
      location.href = route === "./" ? (boot.route ? "../" : "./") : `${prefix}${route}`;
    };

    openers.forEach((node) => node.addEventListener("click", open));
    closer?.addEventListener("click", close);
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) close();
    });
    query.addEventListener("input", () => {
      state.query = query.value;
      state.selected = 0;
      render();
    });
    query.addEventListener("keydown", (event) => {
      const rows = $$("[data-result]", results);
      if (event.key === "ArrowDown") {
        event.preventDefault();
        state.selected = Math.min(state.selected + 1, Math.max(0, rows.length - 1));
        render();
      } else if (event.key === "ArrowUp") {
        event.preventDefault();
        state.selected = Math.max(0, state.selected - 1);
        render();
      } else if (event.key === "Enter" && rows[state.selected]) {
        event.preventDefault();
        rows[state.selected].click();
      }
    });
    document.addEventListener("keydown", (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        open();
      }
    });
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function setupWorkbench() {
    const form = $("#pbhp-workbench");
    if (!form) return;
    const output = $("#receipt-output");
    const stateNode = $("#receipt-state");
    const rationaleNode = $("#receipt-rationale");
    const jsonNode = $("#receipt-json");
    let currentReceipt = null;

    const harmRank = { GREEN: 0, YELLOW: 1, ORANGE: 2, RED: 3, BLACK: 4 };
    const stateFor = (data) => {
      let rank = harmRank[data.harm] ?? 0;
      const notes = [];
      if (data.classification === "Wall") {
        rank = Math.max(rank, 4);
        notes.push("The path is classified as a Wall.");
      }
      if (data.classification === "Gap") {
        rank = Math.max(rank, 2);
        notes.push("A material Gap remains unresolved.");
      }
      if ((data.power === "asymmetric" || data.power === "extreme") && data.reversibility === "irreversible") {
        rank = Math.max(rank, 2);
        notes.push("Power asymmetry plus irreversibility creates an ORANGE floor.");
      }
      if (data.power === "extreme" && (data.reversibility === "hard" || data.reversibility === "irreversible")) {
        rank = Math.max(rank, 3);
        notes.push("Extreme power plus difficult reversal creates a RED floor.");
      }
      if (!data.maybe.trim() || !data.therefore.trim()) {
        rank = Math.max(rank, 2);
        notes.push("Maybe/Therefore is incomplete.");
      }
      if (rank >= 4) return ["REFUSE", notes.length ? notes : ["A BLACK or Wall condition governs."]];
      if (rank === 3) return ["DELAY OR REFUSE PENDING INDEPENDENT CONFIRMATION", notes.length ? notes : ["A RED condition governs."]];
      if (rank === 2) return ["CONSTRAIN AND REVIEW", notes.length ? notes : ["An ORANGE condition governs."]];
      if (rank === 1) return ["PROCEED WITH MITIGATIONS", notes.length ? notes : ["A YELLOW condition requires safeguards."]];
      if (data.classification === "Door") return ["PROCEED — SCOPED", ["The entered fields indicate a GREEN Door; the responsible owner must still verify the evidence."]];
      return ["HOLD — CLASSIFICATION REQUIRED", ["A clear Door has not been established."]];
    };

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const data = Object.fromEntries(new FormData(form).entries());
      const [decisionState, notes] = stateFor(data);
      const now = new Date();
      currentReceipt = {
        schema: "pbhp-draft-receipt-v1",
        created_at: now.toISOString(),
        release_date: document.querySelector("time[datetime]")?.getAttribute("datetime") || null,
        action: data.action,
        affected_parties: data.affected,
        classification: data.classification,
        who_pays_first: data.who_pays,
        power_relationship: data.power,
        reversibility: data.reversibility,
        entered_harm_threshold: data.harm,
        evidence_basis: data.evidence || "not supplied",
        maybe: data.maybe,
        therefore: data.therefore,
        safeguards_or_smaller_door: data.safeguards || "not supplied",
        owner_and_effectiveness_check: data.followup || "not supplied",
        draft_decision_state: decisionState,
        routing_notes: notes,
        disclaimer: "Client-side draft only. Not certification, authorization, legal advice, or independent review."
      };
      stateNode.textContent = decisionState;
      rationaleNode.textContent = notes.join(" ");
      jsonNode.textContent = JSON.stringify(currentReceipt, null, 2);
      output.hidden = false;
      output.scrollIntoView({ behavior: "smooth", block: "start" });
    });

    form.addEventListener("reset", () => {
      currentReceipt = null;
      output.hidden = true;
    });

    $("#copy-receipt")?.addEventListener("click", async () => {
      if (!currentReceipt) return;
      try {
        await navigator.clipboard.writeText(JSON.stringify(currentReceipt, null, 2));
        toast("Receipt JSON copied");
      } catch (_) {
        toast("Clipboard permission unavailable");
      }
    });

    $("#download-receipt")?.addEventListener("click", () => {
      if (!currentReceipt) return;
      const blob = new Blob([JSON.stringify(currentReceipt, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `PBHP_receipt_${new Date().toISOString().replace(/[:.]/g, "-")}.json`;
      link.click();
      URL.revokeObjectURL(url);
    });
  }

  function setupGauges() {
    const input = $("#gauge-search");
    const category = $("#gauge-category");
    const cards = $$("[data-gauge]");
    if (!input || !category || !cards.length) return;
    const filter = () => {
      const query = input.value.trim().toLowerCase();
      const selected = category.value;
      let visible = 0;
      cards.forEach((card) => {
        const matchesText = !query || (card.dataset.search || "").includes(query);
        const matchesCategory = selected === "all" || card.dataset.category === selected;
        card.hidden = !(matchesText && matchesCategory);
        if (!card.hidden) visible += 1;
      });
      input.setAttribute("aria-description", `${visible} gauges shown`);
    };
    input.addEventListener("input", filter);
    category.addEventListener("change", filter);
    filter();
  }


  function setupComponentLibrary() {
    const library = $("[data-component-library]");
    if (!library) return;
    const input = $("#component-search");
    const category = $("#component-category");
    const status = $("#component-status");
    const reset = $("#component-reset");
    const count = $("#component-count");
    const cards = $$('[data-component]', library);
    const sections = $$('[data-component-section]', library);
    if (!cards.length || !input || !category || !status) return;

    const params = new URLSearchParams(location.search);
    if (params.get("q")) input.value = params.get("q");
    if (params.get("category") && $$('option', category).some((option) => option.value === params.get("category"))) {
      category.value = params.get("category");
    }
    if (params.get("state") && $$('option', status).some((option) => option.value === params.get("state"))) {
      status.value = params.get("state");
    }

    const filter = () => {
      const query = input.value.trim().toLowerCase();
      const selectedCategory = category.value;
      const selectedStatus = status.value;
      let visible = 0;
      cards.forEach((card) => {
        const matchesText = !query || (card.dataset.search || "").includes(query);
        const matchesCategory = selectedCategory === "all" || card.dataset.category === selectedCategory;
        const matchesStatus = selectedStatus === "all" || card.dataset.status === selectedStatus;
        card.hidden = !(matchesText && matchesCategory && matchesStatus);
        if (!card.hidden) visible += 1;
      });
      sections.forEach((section) => {
        section.hidden = !$$('[data-component]', section).some((card) => !card.hidden);
      });
      if (count) count.textContent = `${visible} of ${cards.length} components`;
      input.setAttribute("aria-description", `${visible} components shown`);

      const nextParams = new URLSearchParams(location.search);
      query ? nextParams.set("q", query) : nextParams.delete("q");
      selectedCategory !== "all" ? nextParams.set("category", selectedCategory) : nextParams.delete("category");
      selectedStatus !== "all" ? nextParams.set("state", selectedStatus) : nextParams.delete("state");
      const queryString = nextParams.toString();
      history.replaceState(null, "", `${location.pathname}${queryString ? `?${queryString}` : ""}${location.hash}`);
    };

    input.addEventListener("input", filter);
    category.addEventListener("change", filter);
    status.addEventListener("change", filter);
    reset?.addEventListener("click", () => {
      input.value = "";
      category.value = "all";
      status.value = "all";
      filter();
      input.focus();
    });
    filter();
  }

  function setupDetailsPersistence() {
    $$(".glossary details").forEach((details) => {
      details.addEventListener("toggle", () => {
        if (details.open) details.scrollIntoView({ block: "nearest" });
      });
    });
  }

  const closeNav = setupNavigation();
  setupReadingProgress();
  setupHeadingLinks();
  setupTocObserver();
  setupCodeCopy();
  setupSearch(closeNav);
  setupWorkbench();
  setupGauges();
  setupComponentLibrary();
  setupDetailsPersistence();
})();
