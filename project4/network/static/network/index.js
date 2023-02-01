document.addEventListener("DOMContentLoaded", function() {
    // Define profile of user
    let user = document.querySelector("#profile").innerHTML;

    // Adding events to follow/unfollow buttons
    document.querySelector("#follow").addEventListener('click', () => follow(user));
    document.querySelector("#unfollow").addEventListener('click', () => unfollow(user));

})


function follow(user) {
    console.log(user)
    fetch(`/profile/${user}/subscribe`, {
        method: 'POST',
        body: JSON.stringify({
            follower: user
        })
    })
    window.location.reload();
}

function unfollow(user) {
    fetch(`/profile/${user}/unsubscribe`, {
        method: 'POST',
        body: JSON.stringify({
            unfollower: user
        })
    })
    window.location.reload();
}