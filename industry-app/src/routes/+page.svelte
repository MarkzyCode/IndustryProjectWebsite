<script>
    // @ts-nocheck

    //import { sql, config } from '../functions/databaseEndpoint';

	let files;
    let submitting = false;
    let images;

	$: if (files) {
		// Note that `files` is of type `FileList`, not an Array:
		// https://developer.mozilla.org/en-US/docs/Web/API/FileList
		console.log(files);

		for (const file of files) {
			console.log(`${file.name}: ${file.size} bytes`);
		}
	}

    function convertBlobToBase64(blob) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result.split(',')[1]); // Strip the metadata
            reader.onerror = reject;
            reader.readAsDataURL(blob); // Converts the blob to a Base64 data URL
        });
    }

    function convertBase64ToImage(base64String, mimeType = 'image/jpeg') {
        // Decode the Base64 string back to binary data
        const byteCharacters = atob(base64String);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: mimeType });

        // Create a URL for the Blob
        const imageUrl = URL.createObjectURL(blob);
        
        return imageUrl;
    }

    async function submitData() {
        try {
            const pic = new Blob([files], {type: 'image/jpeg'})
            const picBase64 = await convertBlobToBase64(pic);
            console.log(pic)
            const response = await fetch('data-api/rest/testImage', {
                method: 'POST',
                body: JSON.stringify({ image: picBase64 }),
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            console.log("uploaded");
        } catch (error) {
            console.error('Error submitting data:', error);
        } finally {
            submitting = false;
        }
    }

    async function getData() {
        try {
            var response = await fetch('data-api/rest/testImage');
            var data = response.data
            response = response.json()
            console.log(response);
            images = data.image
            console.log("data retrived");
        } catch (error) {
            console.error('Error retriving data:', error);
        }
    }

    function onSubmit(event) {
        event.preventDefault();  // Prevent form from doing its default submission

        if (!submitting) {
            submitting = true;
            // console.log("uploaded");
            // Call the function to submit data
            submitData();
        }
    }

    function getPic(event) {
        event.preventDefault();  // Prevent form from doing its default submission
        getData()
    }

</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

<p>results <a href="/results">link</a></p>

<form id="photo" on:submit={onSubmit}>
    <label for="picture">Upload a picture:</label>
    <input accept="image/png, image/jpeg" bind:files id="picture" name="picture" type="file" required />
    <br>
    {#if files}
        <h2>Selected files:</h2>
        {#each Array.from(files) as file}
            <p>{file.name} ({file.size} bytes)</p>
        {/each}
    {/if}
    <br>
    <button type="submit" disabled={submitting} >Upload</button>
</form>

<br>

<button id="get-pic" on:click={getPic}>Show Pictures</button>

{#if images}
    {#each Array.from(images) as image}
        <img src= {image}>
    {/each}
{/if}