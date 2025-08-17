function clearForm() {
    // Clear sequence input
    document.querySelector("textarea[name='sequence']").value = "";
    // Also clear results
    clearResults();
}

function clearResults() {
    // Reset values inside the results table
    let ids = [
        "mw", "pi", "aa-count", "aa-percent", "atomic",
        "extinction", "half-life", "instability", "aliphatic", "gravy"
    ];

    ids.forEach(id => {
        let cell = document.getElementById(id);
        if (cell) cell.textContent = ""; // Clear cell content
    });
}
