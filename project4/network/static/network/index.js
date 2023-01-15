document.addEventListener("DOMContentLoaded", function() {
    let user = document.querySelector("#profile").innerHTML;
    document.querySelector("#follow").addEventListener('click', () => follow(user));
    document.querySelector("#unfollow").addEventListener('click', () => unfollow(user));

})

function follow(user) {
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