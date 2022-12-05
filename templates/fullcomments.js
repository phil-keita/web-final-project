document.addEventListener("DOMContentLoaded", async () => {
    loadAllComments();
});

async function loadAllComments() {
    const comments = document.getElementById("getscript").getAttribute("comments");
    const commentDiv = document.getElementById("comment-div");

    for (const comment of comments) {
        const hr = document.createElement("hr");
        const title = document.createElement("h2");
        title.innerText = `${comment.post_id}`;
    
        const preview = document.createElement("p");
        const text = `${comment.text}`.substring(1,50) + "...";
        preview.innerText = text;

        const rating = document.createElement("p");
        rating.innerText = `${comment.rating}`;
        commentDiv.append(hr, title, preview, rating);
    }
    const hr = document.createElement("hr");
    commentDiv.appendChild("hr");
}