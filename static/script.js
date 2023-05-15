
$("#results").hide();

function allowDrop(ev) {
    ev.preventDefault();
  }

 function drag(ev) {
    const imagebox = ev.target.closest('.imagebox')
    ev.dataTransfer.setData("text", imagebox.id);
  }

 function drop(ev) {
    ev.preventDefault();  1
    var data = ev.dataTransfer.getData("text");
    const element = document.getElementById(data)
    const dropzone = ev.target.closest('.dropzone')
    dropzone.appendChild(element);
  }

 $(document).ready(function() {
  $('.imagebox').each(function() {
    var dataImage = $(this).attr('data-player-name');
    $(this).find('.overlay_text').text(dataImage);
  });
});

$(document).ready(function() {
    // Collect the data-image and data-player-name attributes of all image boxes
    var data = [];
    $('.dropzone').each(function() {
      var dropzone_id = $(this).attr('id');
      $(this).find('.imagebox').each(function() {
        var data_image = $(this).attr('data-image');
        var data_player_name = $(this).attr('data-player-name');
        data.push({
          'data_image': data_image,
          'data_player_name': data_player_name
        });
      });
    });
    });

$(document).ready(function() {
  $('.submit-button').click(function(e) {
    e.preventDefault();

    // Collect the data-image and data-player-name attributes of all image boxes
    var data = [];
    $('.dropzone').each(function() {
      var dropzone_id = $(this).attr('id');
      $(this).find('.imagebox').each(function() {
        var data_image = $(this).attr('data-image');
        var data_player_name = $(this).attr('data-player-name');
        data.push({
          'dropzone_id': dropzone_id,
          'data_image': data_image,
          'data_player_name': data_player_name
        });
      });
    });

    // Send an AJAX request to a Flask route that handles the database insertion
    $.ajax({
      type: 'POST',
      url: '/submit',
      data: JSON.stringify(data),
      contentType: 'application/json',
      success: function(response) {
      },
      error: function(error) {
        console.log(error);
     }
    });

    $("#player-images").hide();
    $(".table-responsive").hide();
    $("#cta").hide();
    $("#results").show();

    generateChart(players);
  });
});


function generateChart() {
  // Extract the age and ppg data from the players array
  var ages = players.map(function(player) {
    return player.age;
  });
  var average_ranking = players.map(function(player) {
    return player.avg_ranking;
  });
   var player_name = players.map(function(player) {
    return player.name;
  });
   var player_ppg = players.map(function(player) {
    return player.ppg;
  });
   var player_id = players.map(function(player) {
    return player.id;
  });
  var player_image = players.map(function(player) {
    return player.image;
  });

  // Extract the necessary data from the players array
  var data = players.map(function(player) {
    return {
      x: player.age,
      y: player.avg_ranking,
        player_id: player.id,
        player_name: player.name,
        player_image: player.image
    };
  });

 var yourImage0 = new Image()
  yourImage0.src = data[0].player_image;
   var yourImage1 = new Image()
  yourImage1.src = data[1].player_image;
   var yourImage2 = new Image()
  yourImage2.src = data[2].player_image;
   var yourImage3 = new Image()
  yourImage3.src = data[3].player_image;
   var yourImage4 = new Image()
  yourImage4.src = data[4].player_image;
   var yourImage5 = new Image()
  yourImage5.src = data[5].player_image;
   var yourImage6 = new Image()
  yourImage6.src = data[6].player_image;
   var yourImage7 = new Image()
  yourImage7.src = data[7].player_image;

   var playername0 = data[0].player_name;
   var playername1 = data[1].player_name;
   var playername2 = data[2].player_name;
   var playername3 = data[3].player_name;
   var playername4 = data[4].player_name;
   var playername5 = data[5].player_name;
   var playername6 = data[6].player_name;
   var playername7 = data[7].player_name;


   var yourImage1 = new Image()
  yourImage1.src = data[1].player_image;
   var yourImage2 = new Image()
  yourImage2.src = data[2].player_image;
   var yourImage3 = new Image()
  yourImage3.src = data[3].player_image;
   var yourImage4 = new Image()
  yourImage4.src = data[4].player_image;
   var yourImage5 = new Image()
  yourImage5.src = data[5].player_image;
   var yourImage6 = new Image()
  yourImage6.src = data[6].player_image;
   var yourImage7 = new Image()
  yourImage7.src = data[7].player_image;


  var imageData = {
    labels: [playername0, playername1, playername2, playername3,playername4, playername5, playername6, playername7],
    datasets: [{
      label: '',
      pointRadius: [10, 10, 10, 10, 10, 10, 10, 10],
      pointHoverRadius: 20,
      pointHitRadius: 20,
      pointStyle: [yourImage0, yourImage1, yourImage2, yourImage3,yourImage4, yourImage5, yourImage6, yourImage7],
      pointBackgroundColor: "rgba(0,191,255)",
      data: data
    }]
  }

// Create a new Chart.js chart
  var ctx = document.getElementById('myChart').getContext('2d');
    var chart = new Chart(ctx, {
    type: 'scatter',
    data: imageData,
      options: {
      maintainAspectRatio: false,
      legend: {
         display: false
      },
      tooltips: {
    titleFontSize: 20, // set the tooltip title font size to 20
  },
      scales: {
        x: {
          type: 'linear',
          min: 18,
          max: 42,
          ticks: {
            stepSize: 1,
          },
          title: {
            display: true,
            labelString: 'Age'
          }
        },
        y: {
        min: 0,
        max: 7,
          ticks: {
            stepSize: 1,
          },
          scaleLabel: {
            display: true,
            labelString: 'Average Rank'
          }
           }
         }
  }
});
  }
