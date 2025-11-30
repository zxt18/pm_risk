// static/js/pm_risk_table.js

let hot;
let todayDate;
let urls;

// Initialize the entire page
function initPmRiskTable(options) {
    todayDate = options.today;
    urls = options.urls;
    
    initHandsontable();
    bindEventListeners();
    loadInitialData();
}

function initHandsontable() {
    const container = document.querySelector('#pm-risk-table');
    hot = new Handsontable(container, {
        theme: 'ht-theme-main-dark-auto',
        columns: [{
            data: 'book_name',
            title: 'Book',
            readOnly: true,
        }, {
            data: 'risk',
            title: 'Risk'
        }, {
            data: 'target',
            title: 'Target'
        }, {
            data: 'stop',
            title: 'Stop'
        }, {
            data: 'worst_case_bp',
            title: 'Worst Case (bp)'
        }, {
            data: 'worst_case_k',
            title: 'Worst Case (k)'
        }, {
            data: 'comment',
            title: 'Comment on stress estimation'
        }],
        data: [],
        width: '100%',
        height: 'auto',
        manualRowMove: false,
        manualRowResize: true,
        colHeaders: true,
        copyPaste: true,
        licenseKey: 'non-commercial-and-evaluation'
    });
}

// Helper function to get current PM ID from dropdown
function getCurrentPmId() {
    return document.getElementById('pm-selector').value;
}

async function apiFetch(url, options = {}) {
    try {
        const res = await fetch(url, options);
        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
            const msg = data.error || `Request failed (${res.status})`;
            throw new Error(msg);
        }

        return data;
    } catch (err) {
        alert(err.message || "Network error");
        throw err;
    }
}

async function loadRiskData(pmId, selectedDate = null) {
    const url = new URL(urls.dailyRiskData, window.location.origin);
    url.searchParams.set("pm_id", pmId);
    if (selectedDate) url.searchParams.set("date", selectedDate);

    const result = await apiFetch(url);
    hot.loadData(result);
}

async function copyToToday() {
    const pmId = getCurrentPmId();
    const button = document.getElementById('copy-to-today-btn');
    button.disabled = true;

    try {
        const url = new URL(urls.copyToToday, window.location.origin);
        url.searchParams.set("pm_id", pmId);

        const result = await apiFetch(url);

        if (Array.isArray(result.entries) && result.entries.length > 0) {
            document.getElementById('risk-date').value = result.date;
            hot.loadData(result.entries);
        } else {
            alert("No data from yesterday");
        }
    } finally {
        button.disabled = false;
    }
}

function bindEventListeners() {
    document.getElementById('risk-date').addEventListener('change', function() {
        const pmId = getCurrentPmId();
        loadRiskData(pmId, this.value);
    });

    document.getElementById('copy-to-today-btn').addEventListener('click', copyToToday);

    document.getElementById('pm-selector').addEventListener('change', function() {
        const newPmId = this.value;
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('risk-date').value = today;
        loadRiskData(newPmId, today)
    });

    // Submit button handler
    const submitBtn = document.getElementById('submit-btn');
    if (submitBtn) {
        submitBtn.addEventListener('click', handleSubmit);
    }
}

function loadInitialData() {
    const pmId = getCurrentPmId();
    loadRiskData(pmId, todayDate);
}

async function handleSubmit() {
    const pmId = getCurrentPmId();
    const selectedDate = document.getElementById('risk-date').value;

    if (!selectedDate) return alert("Please choose a date");

    const cleaned = hot.getSourceData().map(r => ({
        book_id: r.book_id,
        risk: r.risk || null,
        target: r.target || null,
        stop: r.stop || null,
        worst_case_bp: r.worst_case_bp || null,
        worst_case_k: r.worst_case_k || null,
        comment: r.comment || null,
    }));

    await apiFetch(urls.submitRiskData, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            pm_id: pmId,
            date: selectedDate,
            entries: cleaned
        })
    });

    alert("Saved successfully!");
}

window.initPmRiskTable = initPmRiskTable;