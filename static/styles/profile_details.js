document.addEventListener("DOMContentLoaded", async () => {
    loadPostPreview();
    loadCommentPreview();
});

async function loadPostPreview() {
    const userid = document.getElementById("usernum").getAttribute("data")
    const infoDir = `/profile/${userid}/jsondump/`;

    fetch(infoDir)
        .then(validateJSON)
        .then(data => {
            for (let i=0; i<4; i++) {
                if (!(typeof data.posts[i] == "undefined")) {
                    const postContainer = document.getElementById("post-div");
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

                    //Title
                    const titlehead = document.createElement('h5');
                    const title = document.createElement("a");
                    titlehead.setAttribute('class', 'card-title');
                    title.innerText = data.posts[i].post_name;
                    title.setAttribute("href", `/explore/${data.posts[i].id}/`);
                    title.setAttribute("class", "username");
                    titlehead.appendChild(title);
                    cardBody.append(titlehead, document.createElement("hr"));

                    //Ingredients
                    const ingredientTitle = document.createElement("h6");
                    ingredientTitle.setAttribute('class', 'card-title');
                    ingredientTitle.innerText = "ingredients";
                    cardBody.append(ingredientTitle);
                    const ingredientParagraph = document.createElement("p");
                    ingredientParagraph.setAttribute("class", "card-text");
                    ingredientParagraph.innerText = data.posts[i].ingredients;
                    cardBody.append(ingredientParagraph);
                    const stepsParagraph = document.createElement("p");
                    stepsParagraph.setAttribute("class", "card-text");
                    stepsParagraph.innerText = data.posts[i].recipe;
                    cardBody.append(stepsParagraph, document.createElement("br"));
                }
            }
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
                    title.innerText = data.comments[i].postinfo.post_name + " by " + data.comments[i].postinfo.userinfo.username;
                    title.setAttribute("href", `/explore/${data.comments[i].postinfo.id}/`);
                    title.setAttribute("class", "username");
                    titlehead.appendChild(title);
                    cardBody.append(titlehead, document.createElement("hr"));

                    //Text
                    const commParagraph = document.createElement("p");
                    commParagraph.setAttribute("class", "card-text");
                    if (data.comments[i].text.length > 50) {
                        commParagraph.innerText = data.comments[i].text.slice(0,50) + "...";
                    }
                    else {
                        commParagraph.innerText = data.comments[i].text;
                    }
                    cardBody.append(commParagraph, document.createElement("br"));

                    //Rating
                    const rating = document.createElement("p");
                    rating.setAttribute("class", "card-text");
                    rating.innerText = "Voted " + data.comments[i].rating + " Stars";
                    cardBody.append(rating, document.createElement("br"));
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