import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
		fallback: 'index.html' // Necessary for SPA routing (single-page application)
		}),
		prerender: {
		entries: ['*'] // Prerender all pages in the app
		}
	}
};

export default config;