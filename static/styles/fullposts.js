document.addEventListener("DOMContentLoaded", async () => {
    loadAllPosts();
});

async function loadAllPosts() {
    const userid = document.getElementById("usernum").getAttribute("data")
    const infoDir = `/profile/${userid}/jsondump/`;
    const postDiv = document.getElementById("post-div");

    fetch(infoDir)
        .then(validateJSON)
        .then(data => {
            for (const post of data.posts) {
                if (!(typeof post == "undefined")) {
                    const hr = document.createElement("hr");
                    const title = document.createElement("h2");
                    title.innerText = `${post.post_name}`;
                
                    const preview = document.createElement("p");
                    const text = `${post.recipe}`.substring(0,50) + "...";
                    preview.innerText = text;
                    postDiv.append(hr, title, preview);
                }
            }
            const hr = document.createElement("hr");
            postDiv.appendChild(hr);
        })
        .catch(error => {console.log(`Error occurred: ${error}`)})
}

function validateJSON(response) {
    if (response.ok) {
        return response.json();
    } else {
        return Promise.reject(response);
    }
}