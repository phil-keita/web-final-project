document.addEventListener("DOMContentLoaded", async () => {
    loadAllPosts();
});

async function loadAllPosts() {
    const posts = document.getElementById("getscript").getAttribute("posts");
    const postDiv = document.getElementById("post-div");

    for (const post of posts) {
        const hr = document.createElement("hr");
        const title = document.createElement("h2");
        title.innerText = `${post.post_name}`;
        
        const preview = document.createElement("p");
        const text = `${post.recipe}`.substring(1,50) + "...";
        preview.innerText = text;
        postDiv.append(hr, title, preview);
    }
    const hr = document.createElement("hr");
    postDiv.appendChild("hr");
}