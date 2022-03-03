function updateName(e){
    if (e.value.length >= 1){
        document.getElementById("welcome-message").innerText = "Welcome, " + e.value + "!"
    } else{
        document.getElementById("welcome-message").innerText = "Welcome!"
    }
}

// console.log("hello");


// const registerForm = document.getElementById('register-form')
// console.log("register form: ");
// for (const [key, value] of Object.entries(registerForm)){
//     console.log(`${key}: ${value}`);
// }

// const first_name = document.getElementById('first_name')
// const last_name = document.getElementById('last_name')
// const username = document.getElementById('username')
// const email = document.getElementById('email')
// const password = document.getElementById('password')
// const confirm_password = document.getElementById('confirm_password')

// const first_name_small = document.getElementById('first-name-small')
// const last_name_small = document.getElementById('last-name-small')
// const username_small = document.getElementById('username-small')
// const email_small = document.getElementById('email-small')
// const password_small = document.getElementById('password-small')
// const confirm_password_small = document.getElementById('confirm-password-small')

// const isLonger = (length, min) => length < min ? false : true;
// const isValidEmail = (email) => {
//     const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
//     return re.test(email);
// }

// registerForm.onsubmit = function(e) {
// const formData = new FormData(registerForm)
// console.log(formData);
//     console.log(formData.entries())
//     console.log("add event function call LOL!")
//     e.preventDefault();
//     let is_valid = true;
//     if(!isLonger(first_name.value.length, 2)){
//         first_name_small.innerText = "First name must be 2 or more characters"
//         is_valid = false
//         first_name.value = "";
//     }
//     if(!isLonger(last_name.value.length, 2)){
//         last_name_small.innerText = "Last name must be 2 or more characters"
//         is_valid = false;
//         last_name.value = "";
//     }
//     if(!isLonger(username.value.length, 4)){
//         username_small.innerText = "Username must be 4 or more characters"
//         is_valid = false;
//         username.value = "";
//     }
//     if(!isValidEmail(email.value)){
//         email_small.innerText = "Invalid email address"
//         is_valid = false;
//         email.value = "";
//     }
//     if(!isLonger(password.value, 6)){
//         password_small.innerText = "Password must be 6 or more characters"
//         is_valid = false;
//         password.value = ""
//     }
//     if(password.value != confirm_password.value){
//         confirm_password_small.innerText = "Passwords must match"
//         is_valid = false;
//         confirm_password.value = "";
//     }
//     if(is_valid){
//         fetch("http://localhost:5000/register_form", {method: 'POST', body: formData})
//         .then( response => response.json() )
//         .then( data => console.log(data) )
//         window.location.href="http://localhost:5000/home"
//     }

// }