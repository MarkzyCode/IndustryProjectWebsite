<script>
    import { onMount} from 'svelte';
    import { currentLocations } from '$lib/stores';

    let map;
    let L;

    onMount(async () => {
        if (typeof window !== 'undefined') {
            const leaflet = await import('leaflet');
            L = leaflet.default;

            map = L.map('map').setView([0,0], 4);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            setTimeout(() => {
                map.invalidateSize();
            }, 0);

            currentLocations.subscribe(value => {
                map.setView(value[0], 4);

                map.eachLayer((layer) => {
                    if (layer instanceof L.Marker) {
                        map.removeLayer(layer);
                    }
                });
                
                value.forEach(location => {
                    L.marker(location).addTo(map);
                });
            });
        }
    });
</script>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
    crossorigin=""/>

<div id="map"></div>