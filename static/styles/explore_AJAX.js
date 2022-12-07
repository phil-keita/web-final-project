document.addEventListener("DOMContentLoaded", async () => {
    loadPosts();
});

async function loadPosts() {
    const infoDir = "/explore/postjsondump/";
    const insertElement = document.getElementById("allpost-feed")

    fetch(infoDir)
        .then(validateJSON)
        .then(data => {
            for (const post of data) {
                //Insert each post's info here
                //insertElement is the div which each post will be added (I gave it a unique ID)
                //Make sure to put the title, username, rating, and a sample of the recipe in the AJAX preview
                //Have it so clicking on the post preview will link to /explore/<post_id>/ (Ask me if you have trouble)
            }
        })
        .catch(error => {console.log(`Error occurred - ${error}`)})
}

function validateJSON(response) {
    if (response.ok) {
        return response.json();
    } else {
        return Promise.reject(response);
    }
}