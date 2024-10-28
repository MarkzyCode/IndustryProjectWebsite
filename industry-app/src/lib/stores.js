import { writable } from 'svelte/store';

export let currentLocations = writable([]);
export let currentImage = writable();