window.addEventListener("DOMContentLoaded", function() {
    loadComments();

    const commentButton = document.getElementById("button");
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
    const postContainer = document.getElementById("comment-section");

    //card
    const card = document.createElement('div');
    card.setAttribute("class", "card pb-2");
    card.setAttribute("id", "post");
    postContainer.append(card, document.createElement("br"));
    
    //header
    const header = document.createElement('div');
    header.setAttribute('class', "row pt-3");
    header.setAttribute('style', "margin-left: 5px;");
    card.append(header);

    //Card Body
    const cardBody = document.createElement("div");
    cardBody.setAttribute('class', 'card-body');
    cardBody.setAttribute('id', 'post-content');
    card.append(cardBody);

    //Username of commenter
    const usernameDiv = document.createElement("div");
    usernameDiv.setAttribute('class','col pt-2');
    header.append(usernameDiv);
    const link = document.createElement('a');
    link.setAttribute('href', `/profile/${comment.user_id}/`);
    link.setAttribute('class', "username");
    link.innerHTML = comment.userinfo.username;
    usernameDiv.append(link);

    //Text
    const commParagraph = document.createElement("p");
    commParagraph.setAttribute("class", "card-text");
    commParagraph.innerText = comment.text;
    cardBody.append(commParagraph);

    //Rating
    const rating = document.createElement("p");
    rating.setAttribute("class", "card-text");
    rating.innerText = "Voted " + comment.rating + " Stars";
    cardBody.append(rating);
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