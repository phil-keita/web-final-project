document.addEventListener("DOMContentLoaded", async () => {
    loadPosts();

    const searchBar = document.getElementById("input");
    searchBar.addEventListener("keyup", (event) => {
        if (event.key === "Enter") {
            searchBarResponse();
        }
    });
    const searchButton = document.getElementById("search-button");
    searchButton.addEventListener("click", searchBarResponse);
});

async function loadPosts() {
    const infoDir = "/explore/postjsondump/";
    const insertElement = document.getElementById("allpost-feed");
    const searchQuery = document.getElementById("get-search-query").getAttribute("data");

    fetch(infoDir)
        .then(validateJSON)
        .then(data => {
            for (const post of data) {
                console.log(searchQuery)
                if ((post.recipe.toUpperCase()).includes(searchQuery.toUpperCase()) || (post.post_name.toUpperCase()).includes(searchQuery.toUpperCase())) {
                    insertPost(post);
                }
                //Insert each post's info here
                //insertElement is the div which each post will be added (I gave it a unique ID)
                //Make sure to put the title, username, rating, and a sample of the recipe in the AJAX preview
                //Have it so clicking on the post preview will link to /explore/<post_id>/ (Ask me if you have trouble)
            }
        })
        .catch(error => {console.log(`Error occurred - ${error}`)})
}

function insertPost(post){
    const postContainer = document.getElementById("allpost-feed");
    //card
    const card = document.createElement('div');
    card.setAttribute("class", "card pb-2");
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
    const title = document.createElement('h5');
    title.setAttribute('class', 'card-title');
    title.innerText = post.post_name;
    cardBody.append(title, document.createElement("hr"));
    //Ingredients
    const ingredientTitle = document.createElement("h6");
    ingredientTitle.setAttribute('class', 'card-title');
    ingredientTitle.innerText = "ingredients";
    cardBody.append(ingredientTitle);
    const ingredientParagraph = document.createElement("p");
    ingredientParagraph.setAttribute("class", "card-text");
    cardBody.append(ingredientParagraph);
    const ingredientList = document.createElement("ul");
}

function searchBarResponse() {
    const searchBar = document.getElementById("input").value;
    window.location = "/explore?search=" + searchBar;
}

function validateJSON(response) {
    if (response.ok) {
        return response.json();
    } else {
        return Promise.reject(response);
    }
}