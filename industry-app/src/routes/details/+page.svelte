<script>
    import Banner from "$lib/banner.svelte";
    import Footer from "$lib/footer.svelte";
    import { onMount } from 'svelte';

    let L;
    let map;
    let markerLocations = [
        [-3.388123333333333, 39.971043333333334]
    ];

    onMount(async () => {
        const leaflet = await import('leaflet');
        L = leaflet.default;

        map = L.map('map').setView([-3.388123333333333, 39.971043333333334], 4);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        markerLocations.forEach(location => {
            L.marker(location).addTo(map);
        });
    });
</script>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
   integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
   crossorigin=""/>

<Banner></Banner>

<br>

<h1>Welcome to details</h1>


<br><br>

<Footer></Footer>