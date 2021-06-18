"use strict";

const $ = document.querySelector

function initMap() {
  const basicMap = new google.maps.Map(document.querySelector('#map'), {
    center: {
      lat: 37,
      lng: -122
    },
    scrollwheel: false,
    zoomControl: true,
    panControl: false,
    streetViewControl: false,
    styles: MAPSTYLES,
    zoom: 5,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  });
  
  const userInfo = new google.maps.InfoWindow();

  $('/api/usersinfo', (users) => {
    for (const user of users) {        //defines content of the infowindow
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
            <li><b>Location: </b>${user.latitude}, ${user.longitude}</li>
          </ul>
        </div>
      `);

      // const userMarker = new google.maps.Marker({
      //   position: {
      //     lat: user.latitude,
      //     lng: user.longitude,
      //   },
      //   title: `Listener Name: ${user.name}`,
      //   icon: {
      //     url: '/static/img/user_icon.svg',
      //     scaledSize: new google.maps.Size(50, 50)
      //   },
      //   map: map,
      // });

      // userMarker.addListener('click', () => {
      //   userInfo.close();
      //   userInfo.setContent(userInfoContent);
      //   userInfo.open(map, userMarker);
      // });
    }
}).fail(() => {
    alert((`failed.
  `));
});
}
