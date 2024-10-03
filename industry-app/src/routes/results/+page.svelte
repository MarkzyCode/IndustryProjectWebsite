<script>
    // @ts-nocheck

    import Banner from "$lib/banner.svelte";
    import Footer from "$lib/footer.svelte";
    import { onMount } from "svelte";
    import { PUBLIC_BLOB_URL, PUBLIC_BLOB_TOKEN } from '$env/static/public';
    import { writable } from 'svelte/store';

    let currentTurtleIndex = 0;
    let turtles = {};
    let selectedTurtle = writable({});

    // Will need to be converted to a POST request to an azure function for added security
    async function getDetails(turtleID) {
        try {
            const imageDataResponse = await fetch(`data-api/rest/Image`)
            let data = await imageDataResponse.json();

            const turtleData = data.value.find(turtle => turtle.turtleID === turtleID);
            if (!turtleData) {
                throw new Error(`No image found for turtleID ${turtleID}`);
            }

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
        
        await setTimeout(5000); // change all this once AI API is ready
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

        document.querySelector('.loader').style.display = 'none';
        document.querySelector('.loaded').style.display = "block";
    }

    onMount(() => {
        LoadTurtles()
    })

    function nextTurtle() {
        if (turtles.length > 0) {
            currentTurtleIndex = (currentTurtleIndex + 1) % turtles.length;
            selectedTurtle.set(turtles[currentTurtleIndex]);
        }
    }

    function previousTurtle() {
        if (turtles.length > 0) {
            currentTurtleIndex = (currentTurtleIndex - 1 + turtles.length) % turtles.length;
            selectedTurtle.set(turtles[currentTurtleIndex]);
        }
    }

    function getTurtleDetails(turtle) {
        window.location.href = `results/${turtle.turtleID}`;
    }

</script>

<link rel="stylesheet" type="text/css" href="./src/styles.css"/>

<Banner></Banner>

<br>

<div class="loader"></div>

<div class="loaded">
    <div class="container">
        <div class="preview-panel">
            <button class="nav-button" on:click={previousTurtle}>&lt;</button>
            <div class="image-preview">
                <img src={$selectedTurtle.imageURL} alt="Turtle" />
                <div class="image-info">{currentTurtleIndex + 1}/{turtles.length}</div>
            </div>
            <button class="nav-button" on:click={nextTurtle}>&gt;</button>
        </div>

        <div class="details-panel">
            <div>
                <label>Turtle ID:</label>
                <input type="text" value="{$selectedTurtle.turtleID}" readonly />
            </div>
            <div>
                <label>Confidence:</label>
                <input type="text" value="{$selectedTurtle.matchConfidence}" readonly />
            </div>
            <div>
                <label>Longitude:</label>
                <input type="text" value="{$selectedTurtle.longitude}" readonly />
            </div>
            <div>
                <label>Latitude:</label>
                <input type="text" value="{$selectedTurtle.latitude}" readonly />
            </div>
            <div>
                <label>Date:</label>
                <input type="text" value="{$selectedTurtle.date}" readonly />
            </div>
        </div>

        <div class="map-panel">
        </div>
    </div>

    <div class="actions">
        <button class="details-button" on:click={() => getTurtleDetails(selectedTurtle)}>More Details</button>
        <button class="new-upload-button">New Upload</button>
    </div>
</div>

<Footer></Footer>