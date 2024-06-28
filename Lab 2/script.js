document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

    let response = await fetch('https://auth2api.onrender.com/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `username=${username}&password=${password}`
    });

    let result = await response.json();
    
    if (response.ok) {
        document.getElementById('message').textContent = 'Login successful!';
    } else {
        if (result.error === 'Invalid password') {
            document.getElementById('message').textContent = 'Invalid password. Please try again.';
        } else if (result.error === 'Invalid username') {
            document.getElementById('message').textContent = 'Invalid username. Please try again.';
        } else if(result.error === 'ratelimit exceeded'){
            document.getElementById('message').textContent = 'Too Many Request, Try after 1 minute';
        }
        else {
            document.getElementById('message').textContent = 'Failed to authenticate. Please try again later.';
        }
    }
});
