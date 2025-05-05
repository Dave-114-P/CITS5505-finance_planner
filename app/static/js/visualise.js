// JavaScript for fetching and drawing charts using Chart.js
$(document).ready(function () {
    // Fetch spending data for the bar chart
    $.get("/api/spending_data", function (data) {
        if (data.length === 0) {
            // No data available for the last 30 days
            document.getElementById("last30DaysBarChartContainer").style.display = "none";
            document.getElementById("last30DaysNoBarData").style.display = "block";
        } else {
            // Step 1: Aggregate the data by category
            const aggregatedData = data.reduce((acc, item) => {
                if (!acc[item.category]) {
                    acc[item.category] = 0; // Initialize the category with 0
                }
                acc[item.category] += item.amount; // Accumulate the amount
                return acc;
            }, {});
    
            // Step 2: Extract labels and amounts from the aggregated data
            const labels = Object.keys(aggregatedData); // Categories
            const amounts = Object.values(aggregatedData); // Total amounts per category
    
            // Step 3: Define a color palette for the bars
            const colors = [
                "rgba(255, 99, 132, 0.2)",
                "rgba(54, 162, 235, 0.2)",
                "rgba(255, 206, 86, 0.2)",
                "rgba(75, 192, 192, 0.2)",
                "rgba(153, 102, 255, 0.2)",
                "rgba(255, 159, 64, 0.2)",
                "rgba(199, 245, 66, 0.2)"
            ];
            const borderColors = [
                "rgba(255, 99, 132, 1)",
                "rgba(54, 162, 235, 1)",
                "rgba(255, 206, 86, 1)",
                "rgba(75, 192, 192, 1)",
                "rgba(153, 102, 255, 1)",
                "rgba(255, 159, 64, 1)",
                "rgba(199, 245, 66, 1)"
            ];
    
            // Dynamically assign colors based on the dataset size
            const backgroundColors = colors.slice(0, labels.length);
            const borderColorsDynamic = borderColors.slice(0, labels.length);
    
            // Step 4: Create a bar chart
            const ctxBar = document.getElementById("spendingChart").getContext("2d");
            new Chart(ctxBar, {
                type: "bar",
                data: {
                    labels: labels, // Categories
                    datasets: [{
                        data: amounts, // Total amounts per category
                        backgroundColor: backgroundColors,
                        borderColor: borderColorsDynamic,
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false, // Ensures responsiveness
                    scales: {
                        x: {
                            ticks: {
                                autoSkip: true, // Automatically skips labels if too crowded
                                maxRotation: 45, // Maximum rotation for labels
                                minRotation: 0  // Minimum rotation for labels
                            }
                        },
                        y: {
                            beginAtZero: true,
                            min: 10, // Set the minimum value for the y-axis
                            suggestedMax: Math.max(...amounts) + 20, // Dynamically suggest a max value slightly above the largest bar
                            ticks: {
                                stepSize: 10 // Controls the interval between ticks
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false // Ensures the user does not see a legend
                        },
                        tooltip: {
                            callbacks: {
                                // Show full category name in tooltip
                                label: function (tooltipItem) {
                                    return `${labels[tooltipItem.dataIndex]}: ${tooltipItem.raw}`;
                                }
                            }
                        }
                    }
                }
            });
        }
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

            // Adjust the size of the canvas element to make the pie chart smaller
            const canvas = document.getElementById("monthlySpendingChart");
            canvas.style.width = "100vh"; // Set width
            canvas.style.height = "50vh"; // Set height

            // Create a pie chart
            const ctxPie = canvas.getContext("2d");
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
                    responsive: true, // Ensures the chart resizes dynamically
                    maintainAspectRatio: true, // Keeps the chart aspect ratio intact
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
                        }, legend: {
                            position: "top", // Ensure the legend is at the top of the chart
                            align: "center", // Center-align the legend horizontally
                            labels: {
                                boxWidth: 20, // Reduce the size of the legend boxes
                                font: {
                                    size: 12 // Use a smaller font size for legend labels
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
                    responsive: true, // Ensures the chart resizes dynamically
                    maintainAspectRatio: false, // Ensures it uses the full width of its container
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