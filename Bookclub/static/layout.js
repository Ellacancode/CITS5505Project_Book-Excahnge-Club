        // Function to scroll to the top smoothly
        function topFunction() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }

        // ajax get weather api
        $(document).ready(function() {
        $.ajax({
            url: 'https://wttr.in/Perth?format=j1',
            method: 'GET',
            success: function(data) {
                // Parse and display the weather information
                var weatherInfo = `
                    <p>Temperature: ${data.current_condition[0].temp_C}°C</p>
                `;
                $('#weather-info').html(weatherInfo);
            },
        });
    });