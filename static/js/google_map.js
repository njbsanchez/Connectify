function initMap() {
    
    const meCoords = {
        lat: 37.5873838,
        lng: -122.3538637
    }

    const map = new google.maps.Map($('#map')[0], {
      center: meCoords,
      scrollwheel: true,
      zoomControl: true,
      panControl: false,
      streetViewControl: false,
      zoom: 12,
      mapId:'7470855a38d590e8'
    });
    
    $.get('/api/usersinfo', (users) => {
        console.log(users);
        const meMarker = new google.maps.Marker({
            position: meCoords,
            title: `My Location`,

            icon: {
            url: '/static/img/arrow.png',
            scaledSize: new google.maps.Size(250, 250)
            },
            map: map, 
        });
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
        });
      }
    }).fail(() => {
        alert((`failed.
      `));
    });
  }
  