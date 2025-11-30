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
            hidden: true
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
        rowHeaders: function(index) {
            const rowData = hot.getSourceDataAtRow(index);
            return (rowData?.book_name) || `Row ${index}`;
        },
        rowHeaderWidth: 120,
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

async function loadRiskData(pmId, selectedDate = null) {
    const url = new URL(urls.dailyRiskData, window.location.origin);
    url.searchParams.set("pm_id", pmId);
    if (selectedDate) {
        url.searchParams.set("date", selectedDate);
    }

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        hot.loadData(data);
    } catch (error) {
        console.error('Error loading risk data:', error);
        alert('Failed to load risk data. Please try again later.');
    }
}

async function copyToToday() {
    const pmId = getCurrentPmId();
    const button = document.getElementById('copy-to-today-btn');
    button.disabled = true;

    try {
        const url = new URL(urls.copyToToday, window.location.origin);
        url.searchParams.set("pm_id", pmId);
        const response = await fetch(url);
        const result = await response.json();

        if (Array.isArray(result.entries) && result.entries.length > 0) {
            document.getElementById('risk-date').value = result.date;
            hot.loadData(result.entries);
        } else {
            alert("No data from yesterday");
        }
    } catch (error) {
        console.error('Error copying to today:', error);
        alert('Failed to copy data: ' + error.message);
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

function handleSubmit() {
    const pmId = getCurrentPmId();
    const records = hot.getSourceData();
    const selectedDate = document.getElementById('risk-date').value;

    console.log('Submit:', {
        pmId: pmId,
        date: selectedDate,
        records
    });
}

window.initPmRiskTable = initPmRiskTable;