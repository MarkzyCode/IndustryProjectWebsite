<script>
    // @ts-nocheck

    import Banner from "$lib/banner.svelte";
    import Footer from "$lib/footer.svelte";
    import { onMount, tick } from "svelte";
    import { PUBLIC_BLOB_URL, PUBLIC_BLOB_TOKEN, PUBLIC_BLOB_URL2} from '$env/static/public';
    import { writable } from 'svelte/store';
    import { currentLocations, currentImage } from '$lib/stores';
    import Map from "$lib/map.svelte";

    let currentTurtleIndex = 0;
    let turtles = {};
    let selectedTurtle = writable({});
    let markerLocations = {};
    let loading = true;
    let filename = '';

    // Will need to be converted to a POST request to an azure function/server side for added security
    async function getDetails(turtleID) {
        try {
            const imageDataResponse = await fetch(`data-api/rest/Image?$filter=turtleID eq ${turtleID}`);
            let data = await imageDataResponse.json();
            if (!imageDataResponse.ok) {
                throw new Error(`Failed to fetch image data: ${imageDataResponse.statusText}`);
            }
            console.log(data);
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

            const fileName = `${turtleData.secondaryImageID}.JPG`;
            console.log(fileName);
            const Long = 39.971043333333334;
            const Lat = -3.388123333333333;
            const Date = turtleData.captured;
            const Orientation = turtleData.orientation;
            const Comment = turtleData.comment;
            markerLocations[turtleData.turtleID].push([Long, Lat])

            const url = `${PUBLIC_BLOB_URL2}${fileName}${PUBLIC_BLOB_TOKEN}`; // Token and URL variables shouldn't be in the front end

            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'x-ms-blob-type': 'BlockBlob', // Required header for Azure Blob Storage
                }
            });
            if (!response.ok) {
                throw new Error(`Failed to fetch image: ${response.statusText}`);
            }

            const imageBlob = await response.blob();
            const imageURL = URL.createObjectURL(imageBlob);
            console.log(imageURL);
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

    async function fetchTurtleIDs(result) {
        // Create an array to hold promises for each fetch request
        const turtleIDs = []; // Initialize an array to hold the turtle IDs
        try {
            // Fetch all class indices from the API
            const imageDataResponse = await fetch(`data-api/rest/classIndices`);
            const classData = await imageDataResponse.json();

            // Check if class data is returned and handle it accordingly
            if (!classData || !classData.value) {
                console.error("No class data found.");
                return turtleIDs; // Return the empty array
            }

            // Fetch all turtle data at once
            const turtleResponse = await fetch(`data-api/rest/turtles`);
            const turtleData = await turtleResponse.json();

            // Check if turtle data is returned and handle it accordingly
            if (!turtleData || !turtleData.value) {
                console.error("No turtle data found.");
                return turtleIDs; // Return the empty array
            }

            // Loop through prediction values
            for (let i = 1; i <= 5; i++) {
                const predictionValue = result[`prediction${i}`];

                // Find the matching entry for the current prediction
                const matchingEntry = classData.value.find(entry => entry.value === predictionValue); // Adjust 'value' to your actual field name

                if (matchingEntry) {
                    const secondaryTurtleID = matchingEntry.id; // Adjust property names as needed
                    console.log(`Matching ID for prediction${i}: ${secondaryTurtleID}`);

                    // Filter the turtle data for matching secondaryTurtleID
                    const matchedTurtles = turtleData.value.filter(turtle => turtle.secondaryTurtleID === secondaryTurtleID);

                    // Add matched turtleIDs to the results
                    matchedTurtles.forEach(turtle => {
                        turtleIDs.push(turtle.turtleID); // Collect turtle IDs in the array
                        console.log(`TurtleID for secondaryTurtleID ${secondaryTurtleID}: ${turtle.turtleID}`);
                    });

                    // If no turtles were found for this secondaryTurtleID
                    if (matchedTurtles.length === 0) {
                        console.log(`No turtles found for secondaryTurtleID ${secondaryTurtleID}`);
                    }
                } else {
                    console.log(`No entry found for prediction${i} value ${predictionValue}`);
                }
            }

            // Return the array of turtle IDs
            return turtleIDs; // Return the collected turtle IDs
        } catch (error) {
            console.log("Error fetching data from database:", error.message);
            return turtleIDs; // Return the empty array in case of an error
        }
    }


    // Call AI API to get turtle data
    async function LoadTurtles() {
        let response = null;
        let result = null;
        
        console.log(filename);
        try {
            const proxyUrl = 'http://localhost:3000/api/score';
            const data = {"filename": filename}
            
            const response = await fetch(proxyUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('Error calling endpoint');
            }

            result = await response.json();
            result = JSON.parse(result)
            console.log(result);
            
        } catch (error) {
             console.error('Error fetching turtles:', error);
        }

        const turtleIDs = await fetchTurtleIDs(result);
        console.log(turtleIDs);
         // change all this once AI API is ready
        response = [
            {turtleID: turtleIDs[0], matchConfidence: result.probability1},
            {turtleID: turtleIDs[1], matchConfidence: result.probability2},
            {turtleID: turtleIDs[2], matchConfidence: result.probability3},
            {turtleID: turtleIDs[3], matchConfidence: result.probability4},
            {turtleID: turtleIDs[4], matchConfidence: result.probability5}
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
        await tick();
        currentLocations.set(markerLocations[turtles[currentTurtleIndex].turtleID]);
        loading = false;
    }

    onMount(() => {
        const urlParams = new URLSearchParams(window.location.search);
        filename = urlParams.get('filename');
        console.log("Filename from query parameter:", filename);
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

    function autoResize(event) {
    const textarea = event.target;
    textarea.style.height = '30px'; // Reset height
    textarea.style.height = `${textarea.scrollHeight}px`; // Adjust height based on content
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
                                <textarea class="input__style" type="text" id="Com" name="Com" value="{$selectedTurtle.comment}" on:input={autoResize} readonly placeholder="[No Value Found]"></textarea>
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