function updateName(e){
    if (e.value.length >= 1){
        document.getElementById("welcome-message").innerText = "Welcome, " + e.value + "!"
    } else{
        document.getElementById("welcome-message").innerText = "Welcome!"
    }
}