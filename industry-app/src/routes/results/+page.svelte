<script>
    // @ts-nocheck

    import Banner from "$lib/banner.svelte";
    import Footer from "$lib/footer.svelte";
    import { onMount } from "svelte";

    let turtles = {};

    // Call AI API to get turtle data
    async function LoadTurtles() {
        try {
            let response = await fetch('data-api/rest/turtles'); // Change this to the correct API endpoint
            response = await response.json();
            console.log(response.value);

            turtles = response.value;
        } catch (error) {
            console.error('Error fetching turtles:', error);
        }
        document.querySelector('.loader').style.display = 'none';
        document.getElementById("myDiv").style.display = "block";
    }

    onMount(() => {
        LoadTurtles()
    })

    function getTurtleDetails(turtle) {
        window.location.href = `results/${turtle.turtleID}`;
    }

</script>

<link rel="stylesheet" type="text/css" href="./src/styles.css"/>

<Banner></Banner>

<br>

<div class="loader"></div>

<div id="myDiv">
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

<Footer></Footer>