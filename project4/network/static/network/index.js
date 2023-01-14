document.addEventListener("DOMContentLoaded", function() {
    let user = document.querySelector("#profile").innerHTML;
    console.log(user);
    document.querySelector("#follow").onsubmit = follow(user);
})

function follow(user) {
    fetch(`/profile/${user}`, {
        method: 'POST',
        body: JSON.stringify({
            follower: user
        })
    })
}