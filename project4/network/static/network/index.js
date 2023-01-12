document.addEventListener("DOMContentLoaded", function() {
    const user = document.querySelector("#user").innerHTML;
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