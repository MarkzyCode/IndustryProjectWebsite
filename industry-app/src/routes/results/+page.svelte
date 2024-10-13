<script>
    // @ts-nocheck

    import Banner from "$lib/banner.svelte";
    import Footer from "$lib/footer.svelte";
    import { onMount } from "svelte";
    import { PUBLIC_BLOB_URL, PUBLIC_BLOB_TOKEN } from '$env/static/public';
    import { writable } from 'svelte/store';
    import { DivIcon } from "leaflet";

    let currentTurtleIndex = 0;
    let turtles = {};
    let selectedTurtle = writable({});
    let L;
    let map;
    let markerLocations = {};

    // Will need to be converted to a POST request to an azure function for added security
    async function getDetails(turtleID) {
        try {
            const imageDataResponse = await fetch(`data-api/rest/Image`)
            let data = await imageDataResponse.json();

            const turtleData = data.value.find(turtle => turtle.turtleID === turtleID);
            if (!turtleData) {
                console.log(`No image found for turtleID ${turtleID}`);
            }

            if (!markerLocations[turtleData.turtleID]) {
                markerLocations[turtleData.turtleID] = [];
            }

            

            // turtleData.forEach(location => {
                // markerLocations[location.turtleID].push([location.latitude, location.longitude])
            // });

            markerLocations[turtleData.turtleID].push([turtleData.latitude, turtleData.longitude])
            const fileName = turtleData.image;
            const Long = turtleData.longitude;
            const Lat = turtleData.latitude;
            const Date = turtleData.captured;

            const url = `${PUBLIC_BLOB_URL}${fileName}${PUBLIC_BLOB_TOKEN}`; // Token and URL variables shouldn't be in the front end

            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'x-ms-blob-type': 'BlockBlob', // Required header for Azure Blob Storage
                }
            });

            const imageBlob = await response.blob();
            const imageURL = URL.createObjectURL(imageBlob);

            const returnResponse = {
                imageURL: imageURL,
                longitude: Long,
                latitude: Lat,
                date: Date
            }

            return returnResponse;
        } catch (error) {
            console.error('Error querying the database:', error);
            throw new Error('Failed to get the last image name');
        }
    };

    // Call AI API to get turtle data
    async function LoadTurtles() {
        let response = null;
        // try {
        //     response = await fetch('data-api/rest/turtles'); // Change this to the correct API endpoint
        //     response = await response.json();
        //     console.log(response.value);

        //     turtles = response.value;
        // } catch (error) {
        //     console.error('Error fetching turtles:', error);
        // }
        
        await setTimeout(10000); // change all this once AI API is ready
        response = [
            {turtleID: 404, matchConfidence: 0.9}, 
            {turtleID: 405, matchConfidence: 0.8}, 
        ];

        const updatedResponse = await Promise.all(response.map(async (turtle) => {
            let details = await getDetails(turtle.turtleID); 
            turtle.imageURL = details.imageURL;
            turtle.longitude = details.longitude;
            turtle.latitude = details.latitude;
            turtle.date = details.date;
            return turtle;
        }));

        turtles = updatedResponse;
        selectedTurtle.set(turtles[currentTurtleIndex]);
        loadMap(turtles[currentTurtleIndex].turtleID);

    }

    function loadMap(turtle) {
        if (map) {
            map.remove();
        }
        map = L.map('map').setView(markerLocations[turtle][0], 4);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        markerLocations[turtle].forEach(location => {
            L.marker(location).addTo(map);
        });
    }

    onMount(async() => {
        const leaflet = await import('leaflet');
        L = leaflet.default;

        LoadTurtles()
    })

    function nextTurtle() {
        if (turtles.length > 0) {
            currentTurtleIndex = (currentTurtleIndex + 1) % turtles.length;
            selectedTurtle.set(turtles[currentTurtleIndex]);
            loadMap(turtles[currentTurtleIndex].turtleID);
        }
    }

    function previousTurtle() {
        if (turtles.length > 0) {
            currentTurtleIndex = (currentTurtleIndex - 1 + turtles.length) % turtles.length;
            selectedTurtle.set(turtles[currentTurtleIndex]);
            loadMap(turtles[currentTurtleIndex].turtleID);
        }
    }

    function getTurtleDetails(turtle) {
        window.location.href = `results/${turtle.turtleID}`;
    }

    let loading = true;

    onMount(() => {
        setTimeout(() => {
            loading = false;
        }, 1500); // 1.5 seconds
    });

</script>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TRAC Application</title>
    <link rel="stylesheet" href="./src/styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
        crossorigin=""/>
</head>

{#if loading}
    <div class="loading__spinner"></div>
{:else}
    <body>
        <div>
            <Banner></Banner>
        </div>

        <div class="horizontal-block"> 
            <div class="left-side">
                <div class="preview-panel">
                    <button class="nav-button" on:click={previousTurtle}>&lt;</button>
                    <div class="image-preview">
                        <img src={$selectedTurtle.imageURL} alt="Turtle" />
                    </div>
                    <button class="nav-button" on:click={nextTurtle}>&gt;</button>
                </div>

                <div class="image-info">{currentTurtleIndex + 1}/{turtles.length}</div>

                <div class="details-panel">

                    <ol>
                        <li>
                            <div class="input__with__placeholders--secondary">
                                <label for="TurtleID" class="form__placeholder">Turtle ID: </label>
                                <input class="input__style" type="text" value="{$selectedTurtle.turtleID}" readonly placeholder="[No Value Found]">
                            </div>
                        </li>
                        <li>
                            <div class="input__with__placeholders--secondary">
                                <label for="Orientation" class="form__placeholder">Orientation: </label>
                                <input class="input__style" type="text" value="{$selectedTurtle.orientation}" readonly placeholder="[No Value Found]">
                            </div>
                        </li>
                        <li>
                            <div class="input__with__placeholders--secondary">
                                <label for="Date-Captured" class="form__placeholder">Date Captured: </label>
                                <input class="input__style" type="text" value="{$selectedTurtle.date}" readonly placeholder="[No Value Found]">
                            </div>
                        </li>
                        <li>
                            <div class="input__with__placeholders--secondary">
                                <label for="Confidence" class="form__placeholder">Confidence: </label>
                                <input class="input__style" type="text" value="{$selectedTurtle.matchConfidence}" readonly placeholder="[No Value Found]">
                            </div>
                        </li>
                        <li>
                            <div class="input__with__placeholders--secondary">
                                <label for="Comment" class="form__placeholder">Comment: </label>
                                <textarea class="input__style" type="text" id="Com" name="Com" value="{$selectedTurtle.comment}" readonly placeholder="[No Value Found]"></textarea>
                            </div>
                        </li>
                    </ol>
                </div>
            </div>

            <div class="map-side">
                <div class="map-panel">
                    <div id="map"></div>
                </div>

                <div class="map-description">
                    <p class="map__title">Showing selected location: (location__name)</p>
                    <ol>
                        <li>
                            <div class="input__with__placeholders--secondary">
                                <label for="Longitude" class="form__placeholder">Longitude : </label>
                                <input class="input__style" type="text" value="{$selectedTurtle.longitude}" readonly placeholder="[No Value Found]">
                            </div>
                        </li>
                        <li>
                            <div class="input__with__placeholders--secondary">
                                <label for="Latitude" class="form__placeholder">Latitude : </label>
                                <input class="input__style" type="text" value="{$selectedTurtle.latitude}" readonly placeholder="[No Value Found]">
                            </div>
                        </li>
                    </ol>
                </div>
            </div>
        </div>

        <div class="actions">
            <button class="details-button" on:click={() => getTurtleDetails(selectedTurtle)}>More Details</button>
            <button class="new-upload-button" on:click={() => window.location.href = '/'}>New Upload</button>
        </div>

        <Footer></Footer>
    </body>

    

{/if}

<style>

    .map__title {
        font-size: 16px;
        font-weight: bold;
        font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
        font-style: italic;
        color: gray;
    }

    .horizontal-block {
        display: flex;
        justify-content: center;
        height: 100vh;
    }

    .left-side, .map-side {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 150px;
        margin-top: 40px;
        margin-bottom: auto;
    }

    .left-side {
        background-color: #ddd;
        margin-bottom: 20px;
        border-radius: 20px;
        border: 2px dotted #c9c7c7;

    }

    .map-panel {
        width: 400px;
        height: 400px;
        background-color: rgb(73, 73, 73);
        padding: 5px;
    }

    .preview-panel, .details-panel {
        margin: auto 30px;
    }

    .preview-panel {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 20px;

    }

    .details-panel {
        display: flex;
        flex-direction: column;
        gap: 10px;
        width: 90%;
    }

    .map-description {
        background-color: #ddd;
        border-radius: 20px;
        width: 100%;
        padding: 20px;
        margin-top: 40px;
    }

    .image-info {
        background-color: rgb(51, 50, 50);
        display: flex;
        justify-content: center;
        color: rgb(245, 243, 243);
        padding: 2px;
        font-size: 14px;
        width: 40px;
        margin-top: -50px;
        border-radius: 10px;
        z-index: 100;
    }

    .image-preview {
        position: relative;
    }

    .image-preview img {
        width: 320px;
        height: 320px;
        object-fit: cover;
    }
    
    .nav-button {
        background-color: #ddd;
        border: none;
        font-size: 20px;
        padding: 5px;
        cursor: pointer;
    }

    .actions {
        display: flex;
        justify-content: space-evenly;
        margin-top: 20px;
    }

    .details-button, .new-upload-button {
        padding: 10px 20px;
        background-color: #008cba;
        color: white;
        border: none;
        cursor: pointer;
    }

    .details-button:hover, .new-upload-button:hover {
        background-color: #005f75;
    }
</style>
