import spotipy
from spotipy.oauth2 import SpotifyOAuth

<dl>
  {% for key, val in spotify.current_user().items() %}
    <dt>{{ key }}</dt>
    <dd>
      <pre>
        {{ val }}
      </pre>
    </dd>
  {% endfor %}
</dl>