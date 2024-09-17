<script>
    // @ts-nocheck

    import Banner from '$lib/banner.svelte';
    import Footer from '$lib/footer.svelte';
    import * as exifr from 'exifr';
    import { onMount } from 'svelte';
    import { readable } from 'svelte/store';
    // import { redirect } from '@sveltejs/kit'

    let files;
    let submitting = false;
    let images = [];
    let locationData = { lat: '', lon: '' };
    let capturedDate = '';
    let categories = [];
    let orientation;
    let categoryValues = {};
    let comment;

    async function LoadCategories() {
        try {
            let response = await fetch('data-api/rest/categories');
            response = await response.json();
            console.log(response.value);

            categories = response.value;
        } catch (error) {
            console.error('Error fetching categories:', error);
        }
    }

    onMount(() => {
        LoadCategories();
    })

    $: if (files) {
        console.log(files);
        const reader = new FileReader();
        const file = files[0];

        reader.onload = async function(e) {
            const img = new Image();

            img.onload = async function() {
                const width = img.width;
                const height = img.height;
                console.log(`Image dimensions: ${width}x${height}`);

                try {
                    const metadata = await exifr.parse(file, { gps: true });
                    if (metadata && metadata.latitude && metadata.longitude) {
                        locationData = { lat: metadata.latitude, lon: metadata.longitude };
                        console.log(`Location: Latitude ${metadata.latitude}, Longitude ${metadata.longitude}`);
                    } else {
                        locationData = { lat: '', lon: '' };
                        console.log('No GPS data found');
                    }

                    if (metadata.DateTimeOriginal) {
                        capturedDate = new Date(metadata.DateTimeOriginal).toISOString().split('T')[0];
                        console.log(`Captured Date: ${capturedDate}`);
                    } else {
                        capturedDate = '';
                        console.log('No capture date found');
                    }
                } catch (error) {
                    console.error('Error parsing EXIF data:', error);
                }

                images.push(img.src);
            };

            img.src = e.target.result;
        };

        reader.readAsDataURL(file);
    }

    async function submitData() {
        try {
            let pic = new Blob([files], { type: 'image/jpeg' });

            const promises = Object.keys(categoryValues).map(async category => {
                const response = await fetch('data-api/rest/information', {
                    method: 'POST',
                    body: JSON.stringify({ 
                        userID: null, 
                        turtleID: null, 
                        categoryID: category, 
                        value: categoryValues[category]
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`Server responded with ${response.status}: ${errorText}`);
                }
            })

            await Promise.all(promises);

            // const blob = await fetch(images[0]).then(response => response.blob());  const reader = new FileReader();
            // reader.onloadend = () => resolve(reader.result.split(',')[1]); // Strip the metadata

            const imageResponse = await fetch('data-api/rest/Image', {
                method: 'POST',
                body: JSON.stringify({ 
                    userID: null, 
                    turtleID: null, 
                    secondaryImageID: null, 
                    image: picBase64, 
                    matchConfidence: null, 
                    longitude: locationData.lon, 
                    latitude: locationData.lat, 
                    orientation: orientation, 
                    captured: capturedDate 
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            await imageResponse.json();

            console.log("uploaded");
            window.location.href = '/results';
        } catch (error) {
            console.error('Error submitting data:', error);
        }
    }

    function onSubmit(event) {
        event.preventDefault();  // Prevent form from doing its default submission

        if (!submitting) {
            submitting = true;
            submitData();
        }
    }
</script>

<Banner></Banner>

<br>

<form id="photo" on:submit={onSubmit}>

    {#if files}
        <div class="image-container">
            {#each Array.from(files) as file}
                <img class="image" src={URL.createObjectURL(file)} alt="Uploaded image">
            {/each}
        </div>
    {/if}
    <label for="picture">Upload a picture:</label>
    <input accept="image/png, image/jpeg" bind:files id="picture" name="picture" type="file" required />
    <br>
    <ol>
        <li>
            <label for="Lat">Latitude: </label>
            <input type="text" id="Lat" name="Lat" bind:value={locationData.lat} required><br>
        </li>
        <li>
            <label for="Lat">Longitude: </label>
            <input type="text" id="Lon" name="Lon" bind:value={locationData.lon} required><br>
        </li>
        <li>
            <label for="Cap">Captured Date: </label>
            <input type="date" id="Cap" name="Cap" bind:value={capturedDate} required><br>
        </li>
        <li>
            <label for="Ori">Orientation: </label>
            <input type="text" id="Ori" bind:value={orientation} name="Ori" placeholder="Top, Left, or Right"><br>
        </li>
        {#if categories}
            {#each categories as category}
                <li>
                    <label for="{category.categoryID}">{category.category}: </label>
                    <input type="text" id="{category.categoryID}" bind:value={categoryValues[category.categoryID]} name={category.category} placeholder="{category.description}"><br>
                </li>
            {/each}
        {/if}
        <li>
            <label for="Com">Comment: </label>
            <input type="text" id="Com" bind:value={comment} name="Com" placeholder="Any extra information?"><br>
        </li>
    </ol>
    <br>
    <button type="submit" disabled={submitting}>Upload</button>
</form>

<br><br>

<Footer></Footer>