    $(document).ready(function() {
      var interval;
      // Set the progress bar width based on the percentage
      function setProgress(percentage) {
        $('#progress').width(percentage + '%');
        $('.percentage').text(percentage + '%');
      }
    
      // Show the success screen
      function showSuccessScreen(accuracy, sentiment) {
        clearInterval(interval);
        $('.success-screen').show();
        $('.accuracy').text(accuracy + '%');
        if (sentiment === 'positive') {
          $('.sentiment').text('Positive');
          $('.success-header').css('background-color', 'green');
        } else if (sentiment === 'negative') {
          $('.sentiment').text('Negative');
          $('.success-header').css('background-color', 'red');
        }
      }
    

    
      
      
  $('.close-button').click(function() {
        $('.success-screen').hide();
      });
    });
  $(document).ready(function() {
  $('#search-form').submit(function(event) {
    event.preventDefault();
    // Perform search or other actions here
  });

  // Close the success screen
  $('.close-button').click(function() {
    $('.success-screen').hide();
  });
});
// JavaScript code
function stopPing() {
  // Clear the interval using the interval variable
  clearInterval(interval);
}
// Function to send a request to the server
function getMovieData(movieName) {
  // Show the loading screen or the box here
  // Code to unhide the loading screen or box

  // Send AJAX request to the server
  $.ajax({
    url: "/getMovie",
    type: "POST",
    data: { movieName: movieName },
    success: function (response) {
      if (response.status === "ok") {
        // Start pinging for progress updates
        $("#floating-box").show();
        interval=setInterval(function () {
          // Ping the server for progress updates
          $.ajax({
            url: "/ping",
            type: "GET",
            success: function (pingResponse) {
              // Update the loading screen or box with the progress message
              // Code to update the progress message text
              $("#text").text(pingResponse.message);
              simulateProgress(pingResponse.percentage)
              $("#percentage").text(pingResponse.percentage+"%")
              if (pingResponse.status === "ok" && pingResponse.percentage === 100) {
                stopPing();
                $("#floating-box").hide();
                $(".success-screen").show();
              }


              if (pingResponse.status === "bad") {
                // Show the success screen with "bad" message
                // Code to show the success screen with "bad" message
                $(".success-screen").show();
                $("#success-message").text(pingResponse.message);

              }
            },
          });
        }, 1000); // Ping every 1 second
      }
    },
  });
}
function simulateProgress(percentage) {
  // Calculate the progress bar width based on the percentage
  const progressBarWidth = percentage + "%";

  // Update the progress bar width
  $("#progress-bar").css("width", progressBarWidth);

  // Set the width of the progress text
  $("#progress-text").text(progressBarWidth);

  // Update the progress indication color based on the percentage
  if (percentage <= 25) {
    // Set color to red for 0-25% progress
    $("#progress").css("background-color", "red");
  } else if (percentage <= 50) {
    // Set color to yellow for 26-50% progress
    $("#progress").css("background-color", "yellow");
  } else if (percentage <= 75) {
    // Set color to orange for 51-75% progress
    $("#progress").css("background-color", "orange");
  } else {
    // Set color to green for 76-100% progress
    $("#progress").css("background-color", "green");
  }
}

// Add event listener to the "Search" button
$(document).ready(function () {
  $("#search-button").on("click", function (event) {
    event.preventDefault(); // Prevent form submission

    // Get the movie name from the search input field
    var movieName = $("#search-bar").val();

    // Call the function to send the AJAX request
    getMovieData(movieName);
  });
});
