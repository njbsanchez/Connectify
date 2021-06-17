"use strict";

const $ = document.querySelector

function initMap() {
  const centerPoint = {
    lat: 37,
    lng: -122};

  const basicMap = new google.maps.Map(
    document.querySelector('#map')[0],
    {
      center: centerPoint,
      zoom: 5
    }
  );
  
  const userInfo = new google.maps.InfoWindow();


  $.get('/api/usersinfo', (users_json) => {
    for (const user of users_json) {        //defines content of the infowindow
      const userInfoContent = (`
        <div class="window-content">
          <div class="user-thumbnail">
            <img
              src="/static/img/user_icon.jpg"
              alt="groovy_user"
            />
          </div>

          <ul class="user-info">
            <li><b>Listener Name: </b>${user.name}</li>
            <li><b>Listener Spotify ID: </b>${user.s_id}</li>
            <li><b>Recent Activity </b>${user.recent_activity}</li>
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
          url: '/static/img/polar.svg',
          scaledSize: new google.maps.Size(50, 50)
        },
        map: map,
      });
    }
}).fail(() => {
  alert((`failed.`));
});
}