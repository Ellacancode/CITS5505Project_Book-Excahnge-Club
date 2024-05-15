        // Function to scroll to the top smoothly
        function topFunction() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }

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
                if(data.current_condition[0].temp_C <= 10){
                    var weatherInfo = `
                    <p>Temperature: <strong>${data.current_condition[0].temp_C}°C</strong> too cold, stay home and read books.</p >
                    `;
                    $('#weather-info').html(weatherInfo);
                }else if(data.current_condition[0].temp_C <= 28){
                    var weatherInfo = `
                    <p>Temperature: <strong>${data.current_condition[0].temp_C}°C</strong> prefect weather to read books.</p >
                    `;
                    $('#weather-info').html(weatherInfo);
                }else{
                    var weatherInfo = `
                    <p>Temperature: <strong>${data.current_condition[0].temp_C}°C</strong> turn on the air conditoner and read books.</p >
                    `;
                    $('#weather-info').html(weatherInfo);
                }
                
            },
        });
    });