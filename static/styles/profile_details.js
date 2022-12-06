document.addEventListener("DOMContentLoaded", async () => {
    loadPostPreview();
    loadCommentPreview();
});

async function loadPostPreview() {
    const userid = document.getElementById("usernum").getAttribute("data")
    const infoDir = `/profile/${userid}/jsondump/`;
    const postDiv = document.getElementById("post-div");

    fetch(infoDir)
        .then(validateJSON)
        .then(data => {
            for (let i=0; i<4; i++) {
                if (!(typeof data.posts[i] == "undefined")) {
                    const hr = document.createElement("hr");
                    const title = document.createElement("h2");
                    title.innerText = `${data.posts[i].post_name}`;
                
                    const preview = document.createElement("p");
                    const text = `${data.posts[i].recipe}`.substring(0,50) + "...";
                    preview.innerText = text;
                    postDiv.append(hr, title, preview);
                }
            }
            const hr = document.createElement("hr");
            postDiv.appendChild(hr);
        })
        .catch(error => {console.log(`Error occurred: ${error}`)})
}

async function loadCommentPreview() {
    const userid = document.getElementById("usernum").getAttribute("data")
    const infoDir = `/profile/${userid}/jsondump/`;
    const commentDiv = document.getElementById("comment-div");

    fetch(infoDir)
        .then(validateJSON)
        .then(data => {
            for (let i=0; i<4; i++) {
                if (!(typeof data.comments[i] == "undefined")) {
                    const hr = document.createElement("hr");
                    const title = document.createElement("h2");
                    title.innerText = `${data.comments[i].postinfo.post_name}`;
                
                    const preview = document.createElement("p");
                    const text = `${data.comments[i].text}`.substring(1,50) + "...";
                    preview.innerText = text;
        
                    const rating = document.createElement("p");
                    rating.innerText = `${data.comments[i].rating}`;
                    commentDiv.append(hr, title, preview, rating);
                }
            }
            const hr = document.createElement("hr");
            commentDiv.appendChild(hr);
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