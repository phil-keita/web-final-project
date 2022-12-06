document.addEventListener("DOMContentLoaded", async () => {
    loadAllComments();
});

async function loadAllComment() {
    const userid = document.getElementById("usernum").getAttribute("data")
    const infoDir = `/profile/${userid}/jsondump/`;
    const commentDiv = document.getElementById("comment-div");

    fetch(infoDir)
        .then(validateJSON)
        .then(data => {
            for (const comment of data.comments) {
                if (!(typeof comment == "undefined")) {
                    const hr = document.createElement("hr");
                    const title = document.createElement("h2");
                    title.innerText = `${comment.postinfo.post_name}`;
                
                    const preview = document.createElement("p");
                    const text = `${comment.text}`.substring(1,50) + "...";
                    preview.innerText = text;
        
                    const rating = document.createElement("p");
                    rating.innerText = `${comment.rating}`;
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