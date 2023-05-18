$(document).ready(function() {
  var interval;
  var previousPercentage;
  var samePercentageCount = 0;
  var errorThreshold = 10; // Number of seconds to consider as an error

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
    $("#progress-bar").css("width", "0%");
    $("#progress-text").text("0%");

  });
  $('.close-button2').click(function() {
    $('.error-screen').hide();
    $("#progress-bar").css("width", "0%");
    $("#progress-text").text("0%");

  });

  $('#search-form').submit(function(event) {
    event.preventDefault();
    var movieName = $('#search-bar').val();
    getMovieData(movieName);
  });

  function stopPing() {
    clearInterval(interval);
  }

  function getMovieData(movieName) {
    $('#floating-box').show();

    $.ajax({
      url: "/getMovie",
      type: "POST",
      data: { movieName: movieName },
      success: function (response) {
        if (response.status === "ok") {
          interval = setInterval(function () {
            $.ajax({
              url: "/ping",
              type: "GET",
              success: function (pingResponse) {
                $("#text").text(pingResponse.message);
                simulateProgress(pingResponse.percentage);
                $("#percentage").text(pingResponse.percentage + "%");

                if (pingResponse.percentage === previousPercentage) {
                  samePercentageCount++;
                } else {
                  samePercentageCount = 0;
                  previousPercentage = pingResponse.percentage;
                }

                if (pingResponse.status === "ok" && pingResponse.percentage === 100) {
                  stopPing();
                  setTimeout(function() {
                    $("#floating-box").hide();
                    $(".success-screen").show();
                    $("#accuracy").text(pingResponse.accuracy + "%");

                    if (pingResponse.sentiment === "Positive") {
                      $("#sentiment").css("color", "green");
                      $("#sentiment").text(pingResponse.sentiment);
                    } else {
                      $("#sentiment").css("color", "red");
                      $("#sentiment").text(pingResponse.sentiment);
                    }
                  }, 2000);
                }

                if (pingResponse.status === "bad") {
                  $(".success-screen").show();
                }

                if (samePercentageCount >= errorThreshold) {
                  $("#floating-box").hide();
                  $(".error-screen").show();
                  stopPing();
                }
              },
            });
          }, 1000);
        }
      },
    });
  }

  function simulateProgress(percentage) {
    const progressBarWidth = percentage + "%";
    $("#progress-bar").css("width", progressBarWidth);
    $("#progress-text").text(percentage + "%");

    if (percentage <= 25) {
      $("#progress-bar").css("background-color", "red");
    } else if (percentage <= 50) {
      $("#progress-bar").css("background-color", "yellow");
    } else if (percentage <= 75) {
      $("#progress-bar").css("background-color", "orange");
    } else {
      $("#progress-bar").css("background-color", "green");
    }
  }
});
