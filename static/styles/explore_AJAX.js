document.addEventListener("DOMContentLoaded", async () => {
    loadPosts();

    const searchButton = document.getElementById("search-button");
    searchButton.addEventListener("click", searchBarResponse);
});

async function loadPosts() {
    const infoDir = "/explore/postjsondump/";
    const searchQuery = document.getElementById("get-search-query").getAttribute("data");

    fetch(infoDir)
        .then(validateJSON)
        .then(data => {
            if (data.length != 0) {
                for (const post of data) {
                    console.log(searchQuery)
                    if ((post.recipe.toUpperCase()).includes(searchQuery.toUpperCase()) || (post.post_name.toUpperCase()).includes(searchQuery.toUpperCase())) {
                        insertPost(post);
                    }
                }
            }
            else {
                const postContainer = document.getElementById("allpost-feed");
                const para = document.createElement("p");
                para.innerText = "No posts found with that tag.";

                const card = document.createElement('div');
                card.setAttribute("class", "card pb-2");
                card.setAttribute("id", "post");
                postContainer.append(card, document.createElement("br"));
            }
                //Insert each post's info here
                //insertElement is the div which each post will be added (I gave it a unique ID)
                //Make sure to put the title, username, rating, and a sample of the recipe in the AJAX preview
                //Have it so clicking on the post preview will link to /explore/<post_id>/ (Ask me if you have trouble)
        })
        .catch(error => {console.log(`Error occurred - ${error}`)})
}

function insertPost(post){
    const postContainer = document.getElementById("allpost-feed");
    //card
    const card = document.createElement('div');
    card.setAttribute("class", "card pb-5");
    card.setAttribute("id", "post");
    postContainer.append(card);
    
    
    //header
    const header = document.createElement('div');
    header.setAttribute('class', "row pt-3");
    header.setAttribute('style', "margin-left: 5px;");
    card.append(header);
    //profile pic
    const profileDiv = document.createElement("div");
    profileDiv.setAttribute('class',"col-1");
    header.append(profileDiv);
    const img = document.createElement("img");
    img.setAttribute('id',"profile-pic");
    img.setAttribute("src", "/static/styles/images/profile_pic.jpg");
    profileDiv.append(img);

    //username display
    const usernameDiv = document.createElement("div");
    usernameDiv.setAttribute('class','col pt-2');
    header.append(usernameDiv);
    const link = document.createElement('a');
    link.setAttribute('href', `/profile/${post.user_id}/`);
    link.setAttribute('class', "username");
    link.innerHTML = post.userinfo.username;
    usernameDiv.append(link);
    
    //Image
    const image = document.createElement('img');
    image.setAttribute("src", "/static/styles/images/lasagna.jpg");
    image.setAttribute("id", "carousel");
    image.setAttribute("class", "d-block pt-3");
    card.append(image);

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
    const postRating = document.createElement("h6");
    postRating.innerText = post.rating + " Stars";
    cardBody.append(titlehead, document.createElement("hr"), postRating, document.createElement("hr"));

    //Ingredients
    const ingredientTitle = document.createElement("h6");
    ingredientTitle.setAttribute('class', 'card-title');
    ingredientTitle.innerText = "ingredients";
    cardBody.append(ingredientTitle);
    const ingredientParagraph = document.createElement("p");
    ingredientParagraph.setAttribute("class", "card-text");
    ingredientParagraph.innerText = post.ingredients;
    cardBody.append(ingredientParagraph);

    const stepsTitle = document.createElement("h6");
    stepsTitle.setAttribute('class', 'card-title');
    stepsTitle.innerText = "Steps";
    cardBody.append(stepsTitle);
    const stepsParagraph = document.createElement("p");
    stepsParagraph.setAttribute("class", "card-text");
    stepsParagraph.innerText = post.recipe;
    cardBody.append(stepsParagraph);
}

function searchBarResponse() {
    const searchBar = document.getElementById("input").value;
    window.location = "/explore/?search=" + searchBar;
}

function validateJSON(response) {
    if (response.ok) {
        return response.json();
    } else {
        return Promise.reject(response);
    }
}