// JavaScript for fetching and drawing charts using Chart.js
$(document).ready(function() {
    // Fetch spending data via AJAX
    $.get("/api/spending_data", function(data) {
        const labels = data.map(item => item.category);
        const amounts = data.map(item => item.amount);

        // Create a bar chart
        const ctx = document.getElementById("spendingChart").getContext("2d");
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Spending by Category",
                    data: amounts,
                    backgroundColor: "rgba(54, 162, 235, 0.2)",
                    borderColor: "rgba(54, 162, 235, 1)",
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });
});