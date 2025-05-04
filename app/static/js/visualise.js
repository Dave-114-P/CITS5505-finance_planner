// JavaScript for fetching and drawing charts using Chart.js
$(document).ready(function () {
    // Fetch spending data for the bar chart
    $.get("/api/spending_data", function (data) {
        const labels = data.map(item => item.category);
        const amounts = data.map(item => item.amount);

        // Create a bar chart
        const ctxBar = document.getElementById("spendingChart").getContext("2d");
        new Chart(ctxBar, {
            type: "bar",
            data: {
                labels: labels, // Dynamically handles available categories
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

    // Fetch spending data for the pie chart (current month breakdown)
    $.get("/api/monthly_spending_breakdown", function (data) {
        if (data.length === 0) {
            // No data available for the current month
            document.getElementById("monthlySpendingChartContainer").style.display = "none";
            document.getElementById("monthlySpendingNoData").style.display = "block";
        } else {
            const labels = data.map(item => item.category);
            const amounts = data.map(item => item.amount);

            // Dynamically calculate total and percentages
            const total = amounts.reduce((sum, amount) => sum + amount, 0); // Total spending
            const percentages = amounts.map(amount => ((amount / total) * 100).toFixed(2)); // Percentage for each category

            // Create a pie chart
            const ctxPie = document.getElementById("monthlySpendingChart").getContext("2d");
            new Chart(ctxPie, {
                type: "pie",
                data: {
                    labels: labels, // Dynamically handles available categories
                    datasets: [{
                        label: "Spending Breakdown (Current Month)",
                        data: amounts,
                        backgroundColor: [
                            "rgba(255, 99, 132, 0.2)",
                            "rgba(54, 162, 235, 0.2)",
                            "rgba(255, 206, 86, 0.2)",
                            "rgba(75, 192, 192, 0.2)",
                            "rgba(153, 102, 255, 0.2)",
                            "rgba(255, 159, 64, 0.2)",
                            "rgba(199, 245, 66, 0.2)"
                        ],
                        borderColor: [
                            "rgba(255, 99, 132, 1)",
                            "rgba(54, 162, 235, 1)",
                            "rgba(255, 206, 86, 1)",
                            "rgba(75, 192, 192, 1)",
                            "rgba(153, 102, 255, 1)",
                            "rgba(255, 159, 64, 1)",
                            "rgba(199, 245, 66, 1)"
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    const category = context.label || '';
                                    const amount = context.raw || 0;
                                    const percentage = percentages[context.dataIndex] || '0.00';
                                    return `${category}: $${amount} (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });
        }
    });

    // Fetch spending data for the line chart (last 30 days)
    $.get("/api/spending_last_30_days", function (data) {
        if (data.length === 0) {
            // No data available for the last 30 days
            document.getElementById("last30DaysChartContainer").style.display = "none";
            document.getElementById("last30DaysNoData").style.display = "block";
        } else {
            const dates = data.map(item => item.date);
            const amounts = data.map(item => item.amount);

            // Check if data has less than 30 days, and handle gracefully
            if (dates.length === 0) {
                dates.push("No Data");
                amounts.push(0);
            }

            // Create a line chart
            const ctxLine = document.getElementById("last30DaysChart").getContext("2d");
            new Chart(ctxLine, {
                type: "line",
                data: {
                    labels: dates, // Dynamically handles available dates
                    datasets: [{
                        label: "Spending Over the Last 30 Days",
                        data: amounts,
                        fill: false,
                        borderColor: "rgba(75, 192, 192, 1)",
                        tension: 0.1
                    }]
                },
                options: {
                    scales: {
                        x: {
                            type: "category", // Set to category to handle fewer than 30 days
                            time: {
                                unit: "day"
                            }
                        },
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    });
});