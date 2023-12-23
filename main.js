console.log("Welcome to console.")

// Based on https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Fetching_data
function ask_server() {
    fetch("/reload").then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.text();
    }).then((text) => {
        if (text === "True") {
            location.reload()
        }
    }).catch((_) => {
        close();
    });

    setTimeout(ask_server, 100)
}

ask_server()
