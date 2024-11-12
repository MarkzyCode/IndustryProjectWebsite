import { writable } from 'svelte/store';

// We use this store to send the current locations to the map component
export let currentLocations = writable([]);