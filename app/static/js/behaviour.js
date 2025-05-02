//This jquery function change the color of the navigation item when it was clicked
$(function() {
    $('.nav-item .nav-link').on('click', function () {
        if ($(this).parent('.nav-item').hasClass('skip')) {
            return; // Skip the click event if the link has the 'skip' class
        }
    });
});

//Map show state's name when mouse hover
document.addEventListener("DOMContentLoaded", () => {
    const tooltip = document.querySelector('.tooltip');
    const svg = document.querySelector('#australia-map');
    const states = document.querySelectorAll('.land'); // Updated class to 'land'
    const resetButton = document.querySelector('#resetZoom');

    // Original viewBox values
    const originalViewBox = '0 0 450 450';

    // Function to zoom in on a specific state
    function zoomInState(state) {
        const bbox = state.getBBox(); // Get the bounding box of the state

        // Get the center of the bounding box to center the zoom on the clicked state
        let stateCenterX = bbox.x + bbox.width / 2;
        let stateCenterY = bbox.y + bbox.height / 2;

        // Adjust the center for Tasmania (AU-TAS) to ensure it is centered correctly
        if (state.id === "AU-TAS") {
            stateCenterX -= 40; // move 30 units to the right
            stateCenterY -= 55; // move 50 units downward
        }

        // Calculate the new viewBox values
        const zoomFactor = (state.id !== "AU-TAS") ? 1.5:2; // Adjust this to control the zoom level
        const newWidth = 450 / zoomFactor; // 800 is the original width
        const newHeight = 450 / zoomFactor; // 600 is the original height

        // Calculate the viewBox to center around the clicked state
        const viewBoxX = stateCenterX - newWidth / 2;
        const viewBoxY = stateCenterY - newHeight / 2;

        // Update the SVG's viewBox to zoom in on the state without changing the container size
        svg.setAttribute('viewBox', `${viewBoxX} ${viewBoxY} ${newWidth} ${newHeight}`);
    }

    // AJAX request to get the state information
    function loadStateContent(state) {
        const stateID = state.id;           // e.g., "WA"
        const allStateInfos = document.querySelectorAll('#state_uni_info > div');
    
        // Hide all state info blocks
        allStateInfos.forEach(info => {
            info.style.display = 'none';
        });
    
        // Fetch university data from JSON
        fetch('/static/data/universities.json')
            .then(response => response.json())
            .then(data => {
                const stateKey = getStateNameFromID(stateID); // Map ID to state name used in JSON
                const stateData = data[stateKey];
    
                if (stateData) {
                    // Set state image and name
                    // Set the state image source
                    async function setImageSource(stateID) {
                        const extensions = ['jpg', 'webp'];
                        const imageElement = document.getElementById('state_image');
                        if (!imageElement) {
                            console.error('state_image element not found');
                            return;
                        }
                        for (let ext of extensions) {
                            const path = `/static/image/${stateID}.${ext}`;
                            try {
                                const response = await fetch(path, { method: 'HEAD' });
                                if (response.ok) {
                                    imageElement.src = path; // Set the src attribute of the image
                                    return; // Exit the loop once the valid image is found
                                }
                            } catch (e) {
                                console.error(`Error fetching image ${path}:`, e);
                                continue; // Ignore errors and try the next extension
                            }
                        }
                        console.warn('No valid image found for', stateID);
                    }
                    
                    setImageSource(stateID); // Retry with the next extension
    
                    // Generate state intro and city living cost list
                    let html = `<h2 class="header_font"><strong>${stateKey}</strong></h2>
                    <p class="text_font" style="text-align: justify; font-size:0.8rem">${stateData.intro}</p>`;

                    html += `
                    <div class="table-responsive" style="overflow-x: auto; max-width: 100%; margin-top: 20px;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                        <tr class="header_font" style="background-color: #76c87d; color: white; text-align: center;">
                            <th style="border: 1px solid #ddd; padding: 8px; font-size: 1rem;">City</th>
                            <th style="border: 1px solid #ddd; padding: 8px; font-size: 1rem;">Family of Four<br>Estimated Monthly Cost</th>
                            <th style="border: 1px solid #ddd; padding: 8px; font-size: 1rem;">Single Person<br>Estimated Monthly Cost</th>
                            <th style="border: 1px solid #ddd; padding: 8px; font-size: 1rem;">More Info</th>
                        </tr>
                        </thead>
                        <tbody>
                    `;

                    for (const [city, dataArray] of Object.entries(stateData.cities)) {
                    dataArray.forEach(data => {
                        html += `
                        <tr>
                            <td class="text_font" style="border: 1px solid #ddd; padding: 8px; font-size: 0.85rem;">${city}</td>
                            <td class="text_font" style="border: 1px solid #ddd; padding: 8px; font-size: 0.85rem;">${data.family_of_four}</td>
                            <td class="text_font" style="border: 1px solid #ddd; padding: 8px; font-size: 0.85rem;">${data.single_person}</td>
                            <td class="text_font" style="border: 1px solid #ddd; padding: 8px; font-size: 0.85rem;">
                            <a class="uni_link" href="${data.details}" target="_blank">View Details</a>
                            </td>
                        </tr>
                        `;
                    });
                    }

                    const baseCity = Object.keys(stateData.cities)[0]; // assuming you store the selected city somewhere
                    const comparisonData = data.comparisons?.[baseCity];
                    html += '</tbody></table></div>';

                    html += `<h2 class="header_font" style="margin-top: 20px;"><strong>Comparison</strong></h2>`;

                    html += `
                    <div class="table-responsive" style="overflow-x: auto; max-width: 100%; margin-top: 10px;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                        <tr class="header_font" style="background-color: #76c87d; color: white; text-align: center;">
                            <th style="border: 1px solid #ddd; padding: 8px; font-size: 1rem;">City</th>
                            <th style="border: 1px solid #ddd; padding: 8px; font-size: 1rem;">Expense in ${baseCity} is</th>
                        </tr>
                        </thead>
                        <tbody>
                    `;

                    if (comparisonData) {
                        for (const [comparedCity, text] of Object.entries(comparisonData)) {
                            let color = "#808080"; // default for "nearly the same"
                            let symbol = "➖";

                            if (text.includes("more")) {
                                symbol = "▲";
                                color = "#e74c3c"; // red
                            } else if (text.includes("less")) {
                                symbol = "▼";
                                color = "#76c87d"; // green
                            }

                            html += `
                                <tr>
                                    <td class="text_font" style="border: 1px solid #ddd; padding: 8px; font-size: 0.85rem;">
                                        ${comparedCity}
                                    </td>
                                    <td class="text_font" style="border: 1px solid #ddd; padding: 8px; font-size: 0.85rem; color: ${color};">
                                        ${symbol} ${text}
                                    </td>
                                </tr>
                            `;
                        }
                    }

                    html += '</tbody></table></div>';

                    document.getElementById('state_info').innerHTML = html; // Update the state info container with the generated HTML

                    // Show the state info container
                    const stateInfo = document.querySelectorAll('#state_uni_info > div');
                    stateInfo.forEach(div => {
                        div.style.display = 'flex'; // or 'block' depending on your layout needs
                    });
                }
            })
            .catch(error => {
                console.error('Error loading state data:', error);
            });
    }
    
    // Function to map state ID to the key used in the JSON file
    function getStateNameFromID(stateID) {
        const stateMap = {
            "WA": "Western Australia",
            "NT": "Northern Territory",
            "SA": "South Australia",
            "QLD": "Queensland",
            "NSW": "New South Wales",
            "VIC": "Victoria",
            "TAS": "Tasmania",
            "ACT": "Australian Capital Territory",
            // Add more mappings as needed
        };
        return stateMap[stateID] || stateID; // Default to stateID if not found
    }

    // Add hover events for the tooltip
    states.forEach(state => {
        state.addEventListener('mouseenter', (e) => {
            const name = state.getAttribute('title');
            tooltip.innerHTML = name;
            tooltip.style.opacity = 1;
            tooltip.style.display = 'block';
        });

        state.addEventListener('mousemove', (e) => {
            tooltip.style.left = (e.pageX + 10) + 'px';
            tooltip.style.top = (e.pageY + 10) + 'px';
        });

        state.addEventListener('mouseleave', () => {
                tooltip.style.opacity = 0;
                tooltip.style.display = 'none';
        });

      // Zoom in on state when clicked
        state.addEventListener('click', () => {
            zoomInState(state);
            states.forEach(s => {
                if (s !== state) {
                    s.style.opacity = 0.1; // Dim other states
                    s.style.fill = ''; // Reset fill color for other states
                }
            });
        state.style.fill = '#76c87d'; // fill the clicked state with a different color
        state.style.opacity = 1; // Keep the clicked state fully visible

        document.querySelector('#state_uni_info').style.display = 'block';

        loadStateContent(state); // Load state content
      });
    });

    // Reset zoom on button click
    resetButton.addEventListener('click', () => {
        svg.style.transition = 'viewBox 1s ease-in-out';
        svg.setAttribute('viewBox', originalViewBox);
        states.forEach(state => {
            state.style.opacity = 1; // Reset opacity for all states
            state.style.fill = ''; // Reset fill color for all states
        });
    });
});
