//Handling Login
document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

    let response = await fetch('https://securelabapi.onrender.com/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `username=${username}&password=${password}`
    });

    let result = await response.json();
    
    if (response.ok) {
        document.getElementById('message').textContent = 'Login Successful';
    } else {
        if (result.error === 'Invalid Credentials') {
            document.getElementById('message').textContent = 'Invalid Credentials. Please try again.';
        } else if (result.error === 'Invalid Credentials') {
            document.getElementById('message').textContent = 'Invalid Credentials. Please try again.';
        } else if(result.error === 'Try again after 1 minute'){
            document.getElementById('message').textContent = 'Try again after 1 minute';
        }
        else {
            document.getElementById('message').textContent = 'Failed to authenticate. Please try again later.';
        }
    }
});


