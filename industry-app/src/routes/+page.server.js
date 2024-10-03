export async function load({ fetch }) {
    let categories = [];

    try {
        let response = await fetch('data-api/rest/categories');
        response = await response.json();
        categories = response.value;
    } catch (error) {
        console.error('Error fetching categories:', error);
    }

    return {
        categories
    };
}