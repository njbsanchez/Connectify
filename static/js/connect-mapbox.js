"use strict";


mapboxgl.accessToken = 'pk.eyJ1Ijoibmpic2FuY2hleiIsImEiOiJja3Eya3lpcjgwZXFvMm5waXF3eTZ5eXl5In0.DuyLrqfvB0uRBCosbixFLQ';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/dark-v10',
    center: [37, -122],
    zoom: 3
});
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
        `
      map.on('load', function () {
          // Add a new source from our GeoJSON data and
          // set the 'cluster' option to true. GL-JS will
          // add the point_count property to your source data.
          map.addSource('earthquakes', {
              type: 'json',
              // Point to GeoJSON data. This example visualizes all M1.0+ earthquakes
              // from 12/22/15 to 1/21/16 as logged by USGS' Earthquake hazards program.
              data: users,
              cluster: true,
              clusterMaxZoom: 14, // Max zoom to cluster points on
              clusterRadius: 50 // Radius of each cluster when clustering points (defaults to 50)
          });
          );
    map.addLayer({
        id: 'clusters',
        type: 'circle',
        source: 'earthquakes',
        filter: ['has', 'point_count'],
        paint: {
            // Use step expressions (https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions-step)
            // with three steps to implement three types of circles:
            //   * Blue, 20px circles when point count is less than 100
            //   * Yellow, 30px circles when point count is between 100 and 750
            //   * Pink, 40px circles when point count is greater than or equal to 750
            'circle-color': [
                'step',
                ['get', 'point_count'],
                '#51bbd6',
                100,
                '#f1f075',
                750,
                '#f28cb1'
            ],
            'circle-radius': [
                'step',
                ['get', 'point_count'],
                20,
                100,
                30,
                750,
                40
            ]
        }
    });

    map.addLayer({
        id: 'cluster-count',
        type: 'symbol',
        source: 'earthquakes',
        filter: ['has', 'point_count'],
        layout: {
            'text-field': '{point_count_abbreviated}',
            'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
            'text-size': 12
        }
    });

    map.addLayer({
        id: 'unclustered-point',
        type: 'circle',
        source: 'earthquakes',
        filter: ['!', ['has', 'point_count']],
        paint: {
            'circle-color': '#11b4da',
            'circle-radius': 4,
            'circle-stroke-width': 1,
            'circle-stroke-color': '#fff'
        }
    });

    // inspect a cluster on click
    map.on('click', 'clusters', function (e) {
        var features = map.queryRenderedFeatures(e.point, {
            layers: ['clusters']
        });
        var clusterId = features[0].properties.cluster_id;
        map.getSource('earthquakes').getClusterExpansionZoom(
            clusterId,
            function (err, zoom) {
                if (err) return;

                map.easeTo({
                    center: features[0].geometry.coordinates,
                    zoom: zoom
                });
            }
        );
    });

    // When a click event occurs on a feature in
    // the unclustered-point layer, open a popup at
    // the location of the feature, with
    // description HTML from its properties.
    map.on('click', 'unclustered-point', function (e) {
        var coordinates = e.features[0].geometry.coordinates.slice();
        var mag = e.features[0].properties.mag;
        var tsunami;

        if (e.features[0].properties.tsunami === 1) {
            tsunami = 'yes';
        } else {
            tsunami = 'no';
        }

        // Ensure that if the map is zoomed out such that
        // multiple copies of the feature are visible, the
        // popup appears over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        new mapboxgl.Popup()
            .setLngLat(coordinates)
            .setHTML(
                'magnitude: ' + mag + '<br>Was there a tsunami?: ' + tsunami
            )
            .addTo(map);
    });

    map.on('mouseenter', 'clusters', function () {
        map.getCanvas().style.cursor = 'pointer';
    });
    map.on('mouseleave', 'clusters', function () {
        map.getCanvas().style.cursor = '';
    });
});
























// ------------

// const $ = document.querySelector

// function initMap() {
//   const basicMap = new google.maps.Map(document.querySelector('#map'), {
//     center: {
//       lat: 37,
//       lng: -122
//     },
//     scrollwheel: false,
//     zoomControl: true,
//     panControl: false,
//     streetViewControl: false,
//     styles: MAPSTYLES,
//     zoom: 5,
//     mapTypeId: google.maps.MapTypeId.TERRAIN
//   });
  
//   const userInfo = new google.maps.InfoWindow();

//   $('/api/usersinfo', (users) => {
//     for (const user of users) {        //defines content of the infowindow
//       const userInfoContent = (`
//         <div class="window-content">
//           <div class="user-thumbnail">
//             <img
//               src="/static/img/user_icon.jpg"
//               alt="groovy_user"
//             />
//           </div>

//           <ul class="user-info">
//             <li><b>Listener Name: </b>${user.name}</li>
//             <li><b>Listener Spotify ID: </b>${user.s_id}</li>
//             <li><b>Recent Activity </b>${user.recent_activity}</li>
//             <li><b>Location: </b>${user.latitude}, ${user.longitude}</li>
//           </ul>
//         </div>
//       `);

//       // const userMarker = new google.maps.Marker({
//       //   position: {
//       //     lat: user.latitude,
//       //     lng: user.longitude,
//       //   },
//       //   title: `Listener Name: ${user.name}`,
//       //   icon: {
//       //     url: '/static/img/user_icon.svg',
//       //     scaledSize: new google.maps.Size(50, 50)
//       //   },
//       //   map: map,
//       // });

//       // userMarker.addListener('click', () => {
//       //   userInfo.close();
//       //   userInfo.setContent(userInfoContent);
//       //   userInfo.open(map, userMarker);
//       // });
//     }
// }).fail(() => {
//     alert((`failed.
//   `));
// });
// }



// {% comment %} {%block title %}Connectify{% endblock %}

// {% block head %}
//   <link rel="stylesheet" href="/static/css/maps.css">
//   <link rel="stylesheet" href="/static/css/users.css">

//   <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
//   <script src="/static/js/mapStyles.js"></script>
//   <script src="/static/js/connect.js"></script>
//   <script
//     async defer
//     src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDBZz8jsm-G3NivDaxa8PwlDRfZhIyJ4Q8&callback=initMap">
//   </script>
// {% endblock %}

// {% block body %}
  
//   <main>
//     <section class="map">
//       <div id="map"></div>
//     </section>
//   </main>
// {% endblock %} {% endcomment %}