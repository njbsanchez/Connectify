"use strict";


navigator.geolocation.getCurrentPosition(
  // Handle success
  (pos) => {
    $.post(
      '/api/user/location',
      {latitude: pos.coords.latitude, longitude: pos.coords.longitude},
      (res) => {
        console.log(res);
      });
    const meLocation = new google.maps.Marker({
      position: {
        lat: latitude,
        lng: longitude,
      },
      title: `My Location`,
      icon: {
        url: '/static/img/arrow.png',
        scaledSize: new google.maps.Size(150, 150)
      },
      map: map, 
    });
  },
  
  // Handle error
  (err) => {
    
  },
  // Options that get passed to browser
  {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0
  }
);

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

function initMap() {
  const map = new google.maps.Map($('#map')[0], {
    center: {
      lat: 37.5873838,
      lng: -122.3538637
    },
    scrollwheel: true,
    zoomControl: true,
    panControl: false,
    streetViewControl: false,
    zoom: 12,
    mapId:'7470855a38d590e8'
  });
  
  const userInfo = new google.maps.InfoWindow();

  $.get('/api/usersinfo', (users) => {
    console.log(users);
    for (const user of users) {        //defines content of the infowindow
      const userInfoContent = (`
        <div class="window-content">
          <div class="user-thumbnail">
            <img
              src="/static/img/logo_user.jpg"
              alt="groovy_user"
            />
          </div>
          <ul class="user-info">
            <li><b>Listener Name: </b>${user.name}</li>
            <li><b>Listener Spotify ID: </b>${user.s_id}</li>
            <li><b>Recent Activity </b>${user.recent_activity}</li>
            <li><b>Link to Profile: </b> <a href="/users/${user.user_id}">Link to Profile</a></li>
          </ul>
        </div>
      `);

      const userMarker = new google.maps.Marker({
        position: {
          lat: user.latitude,
          lng: user.longitude,
        },
        title: `Listener Name: ${user.name}`,
        icon: {
          url: '/static/img/logo_user.png',
          scaledSize: new google.maps.Size(150, 150)
        },
        map: map, 
      });

      userMarker.addListener('click', () => {
        userInfo.close();
        userInfo.setContent(userInfoContent);
        userInfo.open(map, userMarker);
        opendiv();
      });

    }
  }).fail(() => {
      alert((`failed.
    `));
  });
}
