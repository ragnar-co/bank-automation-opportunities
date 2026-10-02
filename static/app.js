// Client-side search, sort, and pagination for the "All Tasks" table.
// Operates only on data already rendered by the server — no new data is
// fetched or uploaded.
(function () {
    const table = document.getElementById("task-table");
    if (!table) return;

    const tbody = table.querySelector("tbody");
    const searchInput = document.getElementById("task-search");
    const statusEl = document.getElementById("task-table-status");
    const paginationEl = document.getElementById("task-pagination");
    const headers = Array.from(table.querySelectorAll("thead th"));

    const PAGE_SIZE = 50;
    let allRows = Array.from(tbody.querySelectorAll("tr"));
    let sortState = { index: null, direction: "asc" };
    let currentPage = 1;

    function rowMatches(row, query) {
        if (!query) return true;
        return row.textContent.toLowerCase().includes(query);
    }

    function getCellValue(row, index, type) {
        const cell = row.children[index];
        if (type === "number") {
            const raw = cell.getAttribute("data-value");
            return raw !== null ? parseFloat(raw) : parseFloat(cell.textContent) || 0;
        }
        return cell.textContent.trim().toLowerCase();
    }

    function getFilteredRows() {
        const query = (searchInput?.value || "").trim().toLowerCase();
        return allRows.filter((row) => rowMatches(row, query));
    }

    function getSortedRows(rows) {
        if (sortState.index === null) return rows;
        const header = headers[sortState.index];
        const type = header.getAttribute("data-sort") || "string";
        const sorted = rows.slice().sort((a, b) => {
            const va = getCellValue(a, sortState.index, type);
            const vb = getCellValue(b, sortState.index, type);
            if (va < vb) return -1;
            if (va > vb) return 1;
            return 0;
        });
        if (sortState.direction === "desc") sorted.reverse();
        return sorted;
    }

    function render() {
        const filtered = getFilteredRows();
        const sorted = getSortedRows(filtered);
        const totalPages = Math.max(1, Math.ceil(sorted.length / PAGE_SIZE));
        currentPage = Math.min(currentPage, totalPages);

        tbody.innerHTML = "";
        const start = (currentPage - 1) * PAGE_SIZE;
        sorted.slice(start, start + PAGE_SIZE).forEach((row) => tbody.appendChild(row));

        statusEl.textContent = `Showing ${sorted.length === 0 ? 0 : start + 1}-${Math.min(start + PAGE_SIZE, sorted.length)} of ${sorted.length} tasks`;

        renderPagination(totalPages);
    }

    function renderPagination(totalPages) {
        paginationEl.innerHTML = "";
        if (totalPages <= 1) return;

        const makeButton = (label, page, disabled, active) => {
            const btn = document.createElement("button");
            btn.textContent = label;
            btn.disabled = !!disabled;
            if (active) btn.classList.add("active");
            btn.addEventListener("click", () => {
                currentPage = page;
                render();
            });
            return btn;
        };

        paginationEl.appendChild(makeButton("Prev", currentPage - 1, currentPage === 1));

        const windowSize = 5;
        let start = Math.max(1, currentPage - Math.floor(windowSize / 2));
        let end = Math.min(totalPages, start + windowSize - 1);
        start = Math.max(1, end - windowSize + 1);

        for (let page = start; page <= end; page++) {
            paginationEl.appendChild(makeButton(String(page), page, false, page === currentPage));
        }

        paginationEl.appendChild(makeButton("Next", currentPage + 1, currentPage === totalPages));
    }

    headers.forEach((header, index) => {
        if (!header.getAttribute("data-sort")) return;
        header.addEventListener("click", () => {
            if (sortState.index === index) {
                sortState.direction = sortState.direction === "asc" ? "desc" : "asc";
            } else {
                sortState.index = index;
                sortState.direction = header.getAttribute("data-sort-default") || "asc";
            }
            headers.forEach((h) => h.classList.remove("sorted-asc", "sorted-desc"));
            header.classList.add(sortState.direction === "asc" ? "sorted-asc" : "sorted-desc");
            currentPage = 1;
            render();
        });
    });

    let searchTimeout = null;
    searchInput?.addEventListener("input", () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            currentPage = 1;
            render();
        }, 150);
    });

    // Default sort: Weekly Effort, descending (matches the "Top 3" ordering).
    const defaultIndex = headers.findIndex((h) => h.getAttribute("data-sort-default"));
    if (defaultIndex !== -1) {
        sortState.index = defaultIndex;
        sortState.direction = headers[defaultIndex].getAttribute("data-sort-default");
        headers[defaultIndex].classList.add("sorted-desc");
    }

    render();
})();

// Count-up reveal for Dashboard stat cards. No-ops on pages without these
// data attributes. Mirrors the server-side `human_minutes` Jinja filter so
// the animated value matches the final server-rendered text exactly.
(function () {
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const DURATION_MS = 900;

    function humanMinutes(totalMinutes) {
        totalMinutes = Math.round(totalMinutes);
        const hours = Math.floor(totalMinutes / 60);
        const minutes = totalMinutes % 60;
        if (hours && minutes) return `${hours}h ${minutes}m`;
        if (hours) return `${hours}h`;
        return `${minutes}m`;
    }

    function animateValue(el, target, render) {
        if (reduceMotion) {
            el.textContent = render(target);
            return;
        }
        const start = performance.now();
        function tick(now) {
            const progress = Math.min((now - start) / DURATION_MS, 1);
            const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
            el.textContent = render(Math.round(target * eased));
            if (progress < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
    }

    document.querySelectorAll("[data-count-to]").forEach((el) => {
        animateValue(el, parseInt(el.getAttribute("data-count-to"), 10) || 0, (v) => String(v));
    });

    document.querySelectorAll("[data-count-minutes]").forEach((el) => {
        animateValue(el, parseInt(el.getAttribute("data-count-minutes"), 10) || 0, humanMinutes);
    });
})();
