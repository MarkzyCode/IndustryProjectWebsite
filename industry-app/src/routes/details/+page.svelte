<script>
    import Banner from "$lib/banner.svelte";
    import Footer from "$lib/footer.svelte";
    import { onMount } from 'svelte';

    // @ts-ignore
    let L;
    // @ts-ignore
    let map;
    let markerLocations = [
        [-3.388123333333333, 39.971043333333334]
    ];

    onMount(async () => {
        // @ts-ignore
        const leaflet = await import('leaflet');
        L = leaflet.default;

        map = L.map('map').setView([-3.388123333333333, 39.971043333333334], 4);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        markerLocations.forEach(location => {
            // @ts-ignore
            L.marker(location).addTo(map);
        });
    });
</script>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
   integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
   crossorigin=""/>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dive deeper into your wildlife experience | TRAC </title>
    <link rel="stylesheet" href="./src/styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
        crossorigin=""/>
</head>

<body>
    <div>
        <Banner></Banner>
    </div>

    <br>

    <h1>Welcome to details</h1>


    <br><br>

    <Footer></Footer>
</body>