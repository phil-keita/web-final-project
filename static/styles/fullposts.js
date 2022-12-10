document.addEventListener("DOMContentLoaded", async () => {
    loadAllPosts();
});

async function loadAllPosts() {
    const userid = document.getElementById("usernum").getAttribute("data")
    const infoDir = `/profile/${userid}/jsondump/`;
    const postContainer = document.getElementById("post-div");

    fetch(infoDir)
        .then(validateJSON)
        .then(data => {
            for (const post of data.posts) {
                if (!(typeof post == "undefined")) {
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
                    title.innerText = post.post_name;
                    title.setAttribute("href", `/explore/${post.id}/`);
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
                    ingredientParagraph.innerText = post.ingredients;
                    cardBody.append(ingredientParagraph);
                    const stepsParagraph = document.createElement("p");
                    stepsParagraph.setAttribute("class", "card-text");
                    stepsParagraph.innerText = post.recipe;
                    cardBody.append(stepsParagraph, document.createElement("br"));
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