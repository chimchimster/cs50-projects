document.addEventListener("DOMContentLoaded", function() {
    let user = document.querySelector("#profile").innerHTML;
    document.querySelector("#follow").addEventListener('click', () => follow(user));

})

function follow(user) {
    fetch(`/profile/${user}/subscribe`, {
        method: 'POST',
        body: JSON.stringify({
            follower: user
        })
    })
}