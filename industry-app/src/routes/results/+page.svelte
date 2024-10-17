<script>
    // @ts-nocheck

    import Banner from "$lib/banner.svelte";
    import Footer from "$lib/footer.svelte";
    import { onMount, tick } from "svelte";
    import { PUBLIC_BLOB_URL, PUBLIC_BLOB_TOKEN } from '$env/static/public';
    import { writable } from 'svelte/store';
    import { currentLocations } from '$lib/stores';
    import Map from "$lib/map.svelte";

    let currentTurtleIndex = 0;
    let turtles = {};
    let selectedTurtle = writable({});
    let markerLocations = {};
    let loading = true;

    // Will need to be converted to a POST request to an azure function/server side for added security
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
            const Orientation = turtleData.orientation;
            const Comment = turtleData.comment;

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
                date: Date,
                orientation: Orientation,
                comment: Comment
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
            turtle.orientation = details.orientation;
            turtle.comment = details.comment;
            return turtle;
        }));

        turtles = updatedResponse;
        selectedTurtle.set(turtles[currentTurtleIndex]);
        loading = false;
        await tick();
        currentLocations.set(markerLocations[turtles[currentTurtleIndex].turtleID]);
    }

    onMount(() => {
        LoadTurtles();
    })

    function nextTurtle() {
        if (turtles.length > 0) {
            currentTurtleIndex = (currentTurtleIndex + 1) % turtles.length;
            selectedTurtle.set(turtles[currentTurtleIndex]);
            currentLocations.set(markerLocations[turtles[currentTurtleIndex].turtleID]);
        }
    }

    function previousTurtle() {
        if (turtles.length > 0) {
            currentTurtleIndex = (currentTurtleIndex - 1 + turtles.length) % turtles.length;
            selectedTurtle.set(turtles[currentTurtleIndex]);
            currentLocations.set(markerLocations[turtles[currentTurtleIndex].turtleID]);
        }
    }

    function getTurtleDetails(turtle) {
        // window.location.href = `results/${turtle.turtleID}`;
    }
</script>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Explore & Discover your results instantly | TRAC </title>
    <link rel="stylesheet" href="./src/styles.css">
</head>

{#if loading}
    <div class="loading__spinner"></div>
{:else}
    <body>
        <div>
            <Banner></Banner>
        </div>

        <div class="horizontal__block"> 
            <div class="results__side">


                <div class="image__preview">
                    <button class="next__button1" on:click={previousTurtle}>&lt;</button>
                    <img src={$selectedTurtle.imageURL} alt="Turtle"/>
                    <button class="next__button2" on:click={nextTurtle}>&gt;</button>
                </div>

                <div class="total__count">{currentTurtleIndex + 1}/{turtles.length}</div>

                <div class="details__panel">

                    <ol>
                        <li>
                            <div class="input__with__placeholders--secondary"> 
                                <label for="TurtleID" class="form__placeholder">Turtle ID : </label>
                                <input class="input__style" type="text" value="{$selectedTurtle.turtleID}" readonly placeholder="[No Value Found]">
                            </div>
                        </li>
                        <li>
                            <div class="input__with__placeholders--secondary">
                                <label for="Orientation" class="form__placeholder">Orientation : </label>
                                <input class="input__style" type="text" value="{$selectedTurtle.orientation}" readonly placeholder="[No Value Found]">
                            </div>
                        </li>
                        <li>
                            <div class="input__with__placeholders--secondary">
                                <label for="Date-Captured" class="form__placeholder">Date Captured : </label>
                                <input class="input__style" type="text" value="{$selectedTurtle.date}" readonly placeholder="[No Value Found]">
                            </div>
                        </li>
                        <li>
                            <div class="input__with__placeholders--secondary">
                                <label for="Confidence" class="form__placeholder">Confidence : </label>
                                <input class="input__style" type="text" value="{$selectedTurtle.matchConfidence}" readonly placeholder="[No Value Found]">
                            </div>
                        </li>
                        <li>
                            <div class="input__with__placeholders--secondary">
                                <label for="Comment" class="form__placeholder">Comment : </label>
                                <textarea class="input__style" type="text" id="Com" name="Com" value="{$selectedTurtle.comment}" readonly placeholder="[No Value Found]"></textarea>
                            </div>
                        </li>
                    </ol>
                </div>
            </div>

            <div class="map__side">
                <div class="map__panel">
                    <Map></Map>
                </div>

                <div class="map__description">
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

        <div class="button__block">
            <button class="form__button" on:click={() => getTurtleDetails(selectedTurtle)}>More Details</button>
            <button class="form__button" on:click={() => window.location.href = '/'}>New Upload</button>
        </div>

        <Footer></Footer>

    </body>
{/if}