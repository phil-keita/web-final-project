window.addEventListener("DOMContentLoaded", function() {
    loadComments();

    const commentButton = document.getElementById("add-button");
    commentButton.addEventListener("click", postComment);
});

async function loadComments() {
    const postid = document.getElementById("post-id").getAttribute("postid");
    const getComments = `/explore/${postid}/commentjsondump/`;
    console.log("GOT HERE JUST FINE")
    fetch(getComments)
        .then(validateJSON)
        .then(data => {
            for (const comment of data) {
                insertComment(comment);
            }
        });
    console.log("TESTING")
}

function insertComment(comment) {
    const container = document.getElementById("comment-section");
    const div = document.createElement("div");
    div.classList.add("comment");

    const username = document.createElement("h4");
    username.innerText = comment.userinfo.username;

    const rating = document.createElement("h4");
    rating.innerText = comment.rating + " Stars";

    const text = document.createElement("p");
    text.innerText = comment.text;
    const hr = document.createElement("hr");

    div.append(username, rating, text, hr);
    container.appendChild(div);
}

async function postComment() {
    const postid = document.getElementById("post-id").getAttribute("postid");
    const postComment = `/explore/${postid}/addcomment/`;
    const text = document.getElementById("comment-value").value; //TEXT FIELD
    const rating = document.getElementById("rating-value").value; //RATING FIELD

    fetch(postComment, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "rating": rating,
            "text": text
        })
    })
    window.location.reload()
}

 function validateJSON(response) {
    if (response.ok) {
        return response.json();
    } else {
        return Promise.reject(response);
    }
}