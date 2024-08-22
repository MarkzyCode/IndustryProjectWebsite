<script>
    // @ts-nocheck

    //import { sql, config } from '../functions/databaseEndpoint';

	let files;
    let submitting = false;

	$: if (files) {
		// Note that `files` is of type `FileList`, not an Array:
		// https://developer.mozilla.org/en-US/docs/Web/API/FileList
		console.log(files);

		for (const file of files) {
			console.log(`${file.name}: ${file.size} bytes`);
		}
	}

    // async function submitData() {
    //     try {
    //         const result = await sql
    //             .connect(config)
    //             .then(() => sql.query('INSERT INTO testImage VALUES (' + files + ')'))
    //             .then((result) => result.recordset)
    //             .catch((error) => console.warn('Error querying database: ', error));
    //         console.log(result);
    //     } catch (error) {
    //         console.error('Error submitting data:', error);
    //     } finally {
    //         submitting = false;
    //     }
    // }

    function onSubmit(event) {
        event.preventDefault();  // Prevent form from doing its default submission

        if (!submitting) {
            submitting = true;
            console.log("uploaded");
            // Call the function to submit data
            // submitData();
        }
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
