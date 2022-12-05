document.addEventListener("DOMContentLoaded", async () => {
    loadPostPreview();
    loadCommentPreview();
});

async function loadPostPreview() {
    const postDir = "" //GOES TO "/profile/<int:userid>/jsondump/"
    const postDiv = document.getElementById("post-div");

    fetch(postDir)
        .then(posts => {
            for (let i=0; i<4; i++) {
                if (posts[i] !== null) {
                    const hr = document.createElement("hr");
                    const title = document.createElement("h2");
                    title.innerText = `${posts[i].post_name}`;
                
                    const preview = document.createElement("p");
                    const text = `${posts[i].recipe}`.substring(0,50) + "...";
                    preview.innerText = text;
                    postDiv.append(hr, title, preview);
                }
            }
            const hr = document.createElement("hr");
            postDiv.appendChild("hr");
        })
        .catch(error => {console.log(`Error occurred: ${error}`)})
}

async function loadCommentPreview() {
    const comments = document.getElementById("getscript").getAttribute("comments");
    const commentDiv = document.getElementById("comment-div");
    const commentTEST = document.createElement("h1");
    commentTEST.innerText("MADE IT HERE");
    commentDiv.appendChild(commentTEST);

    for (let i=0; i<4; i++) {
        if (comments[i] !== null) {
            const hr = document.createElement("hr");
            const title = document.createElement("h2");
            title.innerText = `${comments[i].post_id}`;
        
            const preview = document.createElement("p");
            const text = `${comments[i].text}`.substring(1,50) + "...";
            preview.innerText = text;

            const rating = document.createElement("p");
            rating.innerText = `${comments[i].rating}`;
            commentDiv.append(hr, title, preview, rating);
        }
    }
    const hr = document.createElement("hr");
    commentDiv.appendChild("hr");
}