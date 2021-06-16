"use strict";

$('#submit').on('submit', (evt) => {
    evt.preventDefault();
  
    const locationCoords = {
      'lat': $('#latitude').val(),
      'long': $('#longitude').val()
    };
  
    $.post('/update-coords', locationCoords, (res) => {
      alert(res);
    });
  });