<script>
    // @ts-nocheck

    import Banner from "$lib/banner.svelte";
    import Footer from "$lib/footer.svelte";
    import { onMount } from "svelte";

    let currentTurtleIndex = 0;
    let turtles = {};
    let selectedTurtle;

    // Call AI API to get turtle data
    async function LoadTurtles() {
        let response = null;
        try {
            response = await fetch('data-api/rest/turtles'); // Change this to the correct API endpoint
            response = await response.json();
            console.log(response.value);

            turtles = response.value;
        } catch (error) {
            console.error('Error fetching turtles:', error);
        }
        document.querySelector('.loader').style.display = 'none';
        document.getElementById("myDiv").style.display = "block";

        await response.then(data => {
            document.getElementById('test').innerHTML = 'received response';
            // let turtleList = document.createElement('ol');
            // turtleList.id = 'turtleList';
            // document.getElementById('myDiv').appendChild(turtleList);

            // for (let i = 0; i < response.value.length; i++) {
            //     let turtle = response.value[i];
            //     let turtleItem = document.createElement('li');
            //     turtleItem.id = turtle.turtleID;
            //     turtleList.appendChild(turtleItem);

            //     let turtleImage = document.createElement('img');
            //     turtleImage.src = turtle.imageURL;
            //     turtleItem.appendChild(turtleImage);

            //     let matchConfidence = document.createElement('p');
            //     matchConfidence.innerHTML = `Match Confidence: ${turtle.matchConfidence}`;
            //     turtleItem.appendChild(matchConfidence);

            //     let moreDetailsButton = document.createElement('button');
            //     moreDetailsButton.id = turtle.turtleID;
            //     moreDetailsButton.name = turtle.turtleID;
            //     moreDetailsButton.innerHTML = 'More Details';
            //     moreDetailsButton.onclick = function() {
            //         getTurtleDetails(turtle);
            //     }
            //     turtleItem.appendChild(moreDetailsButton);
            // }
        });
    }

    onMount(() => {
        LoadTurtles()
    })

    function nextTurtle() {
        turtles.subscribe(turtleList => {
            currentTurtleIndex = (currentTurtleIndex + 1) % turtleList.length;
            selectedTurtle.set(turtleList[currentTurtleIndex]);
        });
    }

    function previousTurtle() {
        turtles.subscribe(turtleList => {
            currentTurtleIndex = (currentTurtleIndex - 1 + turtleList.length) % turtleList.length;
            selectedTurtle.set(turtleList[currentTurtleIndex]);
        });
    }

    function getTurtleDetails(turtle) {
        window.location.href = `results/${turtle.turtleID}`;
    }

</script>

<link rel="stylesheet" type="text/css" href="./src/styles.css"/>

<Banner></Banner>

<br>

<div class="loader"></div>

<!-- <div id="myDiv">
    <h1 id="test">hi</h1>
    <ol>
        {#if turtles}
            {#each turtles as turtle}
                <li>
                    <img src="">
                    <p>Match Confidence: {turtle.matchConfidence}</p>
                    <button id={turtle.turtleID} name={turtle.turtleID} on:click={getTurtleDetails(turtle)}>More Details</button><br>
                </li>
            {/each}
        {/if}
    </ol>
</div>

<br><br>

<Footer></Footer> -->

<div class="container">
    <div class="preview-panel">
        <button class="nav-button" on:click={previousTurtle}>&lt;</button>
        <div class="image-preview">
            <!-- <img src={selectedTurtle.imageURL || 'default-image.png'} alt="Turtle" /> -->
            <div class="image-info">1/5</div>
        </div>
        <button class="nav-button" on:click={nextTurtle}>&gt;</button>
    </div>

    <div class="details-panel">
        <div>
            <label>Confidence:</label>
            <!-- <input type="text" value="{selectedTurtle.confidence || 'N/A'}" readonly /> -->
        </div>
        <div>
            <label>Longitude:</label>
            <!-- <input type="text" value="{selectedTurtle.longitude || 'N/A'}" readonly /> -->
        </div>
        <div>
            <label>Latitude:</label>
            <!-- <input type="text" value="{selectedTurtle.latitude || 'N/A'}" readonly /> -->
        </div>
        <div>
            <label>Date:</label>
            <!-- <input type="text" value="{selectedTurtle.date || 'N/A'}" readonly /> -->
        </div>
    </div>

    <div class="map-panel">
    </div>
</div>

<div class="actions">
    <button class="details-button" on:click={() => getTurtleDetails(selectedTurtle)}>More Details</button>
    <button class="new-upload-button">New Upload</button>
</div>

<Footer></Footer>

<style>
    /* Container styling for layout */
    .container {
        display: flex;
        justify-content: space-between;
        padding: 20px;
        gap: 20px;
    }

    .preview-panel {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .image-preview {
        position: relative;
    }

    .image-preview img {
        width: 250px;
        height: 250px;
        object-fit: cover;
    }

    .image-info {
        position: absolute;
        bottom: 5px;
        left: 5px;
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        padding: 2px 5px;
        font-size: 14px;
    }

    .status-banner {
        position: absolute;
        bottom: 5px;
        right: 5px;
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        padding: 2px 5px;
        font-size: 14px;
    }

    .nav-button {
        background-color: #ddd;
        border: none;
        font-size: 20px;
        padding: 5px;
        cursor: pointer;
    }

    .details-panel {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .details-panel div {
        display: flex;
        justify-content: space-between;
    }

    .details-panel input {
        width: 150px;
        border: 1px solid #ccc;
        padding: 5px;
    }

    .map-panel {
        width: 300px;
        height: 300px;
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