document.addEventListener("DOMContentLoaded", async () => {
    loadAllComments();
});

async function loadAllComments() {
    const userid = document.getElementById("usernum").getAttribute("data")
    const infoDir = `/profile/${userid}/jsondump/`;

    fetch(infoDir)
        .then(validateJSON)
        .then(data => {
            for (const comment of data.comments) {
                if (!(typeof comment == "undefined")) {
                    const postContainer = document.getElementById("comment-div");

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

                    //Title of the post
                    const titlehead = document.createElement('h5');
                    const title = document.createElement("a");
                    titlehead.setAttribute('class', 'card-title');
                    title.innerText = comment.postinfo.post_name + " by " + comment.postinfo.userinfo.username;
                    title.setAttribute("href", `/explore/${comment.postinfo.id}/`);
                    title.setAttribute("class", "username");
                    titlehead.appendChild(title);
                    cardBody.append(titlehead, document.createElement("hr"));

                    //Text
                    const commParagraph = document.createElement("p");
                    commParagraph.setAttribute("class", "card-text");
                    if (comment.text.length > 50) {
                        commParagraph.innerText = comment.text.slice(0,50) + "...";
                    }
                    else {
                        commParagraph.innerText = comment.text;
                    }
                    cardBody.append(commParagraph, document.createElement("br"));

                    //Rating
                    const rating = document.createElement("p");
                    rating.setAttribute("class", "card-text");
                    rating.innerText = "Voted " + comment.rating + " Stars";
                    cardBody.append(rating, document.createElement("br"));
                }
            }
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