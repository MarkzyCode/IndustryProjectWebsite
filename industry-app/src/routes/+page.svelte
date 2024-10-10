<script>
    // @ts-nocheck

    import Banner from '$lib/banner.svelte';
    import Footer from '$lib/footer.svelte';
    import * as exifr from 'exifr';
    import { onMount } from 'svelte';
    import { PUBLIC_BLOB_URL, PUBLIC_BLOB_TOKEN } from '$env/static/public';
    // import { page } from '$app/stores';
    // import { readable } from 'svelte/store';

    export let data;
    let { categories } = data;

    let files;
    let submitting = false;
    let images = [];
    let locationData = { lat: '', lon: '' };
    let capturedDate = '';
    let orientation;
    let categoryValues = {};
    let comment;

    $: if (files) {
        const reader = new FileReader();
        const file = files[0];

        reader.onload = async function(e) {
            const img = new Image();

            img.onload = async function() {
                try {
                    const metadata = await exifr.parse(file, { gps: true });
                    if (metadata && metadata.latitude && metadata.longitude) {
                        locationData = { lat: metadata.latitude, lon: metadata.longitude };
                    } else {
                        locationData = { lat: '', lon: '' };
                        console.log('No GPS data found');
                    }

                    if (metadata.DateTimeOriginal) {
                        capturedDate = new Date(metadata.DateTimeOriginal).toISOString().split('T')[0];
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

    // Will need to be converted to a POST request to an azure function for added security
    async function uploadImage(file) {
        const url = `${PUBLIC_BLOB_URL}${file.name}${PUBLIC_BLOB_TOKEN}`; // Token and URL variables shouldn't be in the front end

        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'x-ms-blob-type': 'BlockBlob', // Required header for Azure Blob Storage
                'Content-Type': file.type, // Set the content type to the file's MIME type
            },
            body: file
        });
    };

    async function submitData() {
        try {
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

            const imageResponse = await uploadImage(files[0]);

            const imageDataResponse = await fetch('data-api/rest/Image', {
                method: 'POST',
                body: JSON.stringify({ 
                    userID: null, 
                    turtleID: null, 
                    secondaryImageID: null, 
                    image: files[0].name,  
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
            if (!imageDataResponse.ok) {
                const errorText = await imageDataResponse.text();
                throw new Error(`Server responded with ${imageDataResponse.status}: ${errorText}`);
            }

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

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TRAC Application</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
</head>

<body>

    <Banner></Banner>
    
    <div class="container--center">
        <div class="container__title">
            <span data-text="Turtle Recognition,"></span>
            <span data-text="Awareness"></span>
            <span data-text="and Conservation"></span>
        </div>

        <h1 class="container__subheading">Easily identify and <b class="bold1">track turtles with cutting-edge AI technology</b>. 
            Simply upload your file below to get started!</h1> 

    </div>

    
        <div class="form--allignment">
            <form id="photo" on:submit={onSubmit}>
        
                <div class="form__header">
                    <i class="fa-solid fa-cloud-arrow-up" id="cloud"></i>
                    <label for="picture" class="form__title">Upload Turtle Image <span class="asterisk__red">*</span></label>
                </div>
                
                <div class="custom__upload">
                    <input accept="image/png, image/jpeg" bind:files id="picture" name="picture" type="file" required class="file__input"/>

                    {#if !files}  <!-- Check if files are not present -->
                        <i class="fa-solid fa-arrow-up-from-bracket" id="upload__icon"></i>
                        <label for="picture" class="custom__upload__label">
                            Drop Items here or <span class="upload__keyword">browse files</span>
                        </label>
                    {/if}

                    {#if files}
                        <div class="image__container">
                            {#each Array.from(files) as file}
                                <img class="custom__upload__image" src={URL.createObjectURL(file)} alt="Uploaded image">
                            {/each}
                        </div>
                    {/if}
                </div> 

                <div class="under__upload">
                    <label for="file-size" class="file__size">up to 25mb</label>
                    <p class="movelower__dot">&#x2022;</p>
                    <input accept="image/png, image/jpeg" bind:files id="picture" name="picture" type="file" required class="movelower__input"/>
                </div>
                
                <ol>
                    <li>
                        <div class="form__input__container--primary">
                            <input type="text" id="Lat" name="Lat" bind:value={locationData.lat} required placeholder="">
                            <label for="Lat" class="form__placeholder">Latitude: </label> 
                        </div>
                    </li>
                    <li>
                        <div class="form__input__container--primary">
                            <input type="text" id="Lon" name="Lon" bind:value={locationData.lon} required placeholder="">
                            <label for="Lat" class="form__placeholder">Longitude: </label>
                        </div>
                    </li>
                    <li>
                        <div class="form__input__container--primary">
                            <input type="date" id="Cap" name="Cap" bind:value={capturedDate} required placeholder="">
                            <label for="Cap" class="form__placeholder">Captured Date: </label>
                        </div>
                    </li>
                    <li>
                        <div class="input__with__placeholders--secondary">
                            <label for="Ori" class="form__placeholder">Orientation: </label>
                            <input type="text" id="Ori" name="Ori" bind:value={orientation} required placeholder="Top, Left, or Right">
                        </div>
                    </li>
                    {#if categories}
                        {#each categories as category}
                            <li>
                                <div class="input__with__placeholders--secondary">   
                                    <label for="{category.categoryID}" class="form__placeholder">{category.category}: </label>
                                    <input type="text" id="{category.categoryID}" bind:value={categoryValues[category.categoryID]} name={category.category} placeholder="{category.description}">
                                </div>
                            </li>
                        {/each}
                    {/if}
                    <li>
                        <div class="input__with__placeholders--secondary">
                            <label for="Com" class="form__placeholder">Comment: </label>
                            <input type="text" id="Com" bind:value={comment} name="Com" placeholder="Provide details about the subject...">
                        </div>
                    </li>
                </ol>
                <button type="submit" class="form__button" disabled={submitting}>Upload</button>
            </form>
        </div>
    
    <Footer></Footer>

</body>
