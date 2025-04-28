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

        const allStateInfos = document.querySelectorAll('#state_uni_info > div');
        allStateInfos.forEach(info => {
            info.style.display = 'none';
        });

        const stateName = state.id;
        const stateInfo = document.querySelector(`.${stateName}`);
        if (stateInfo) {
            stateInfo.style.display = 'flex';
        }
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
