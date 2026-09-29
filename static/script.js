async function checkEmail() {

    const subject = document.getElementById("subject").value;
    const body = document.getElementById("body").value;

    const result = document.getElementById("result");
    const error = document.getElementById("error");

    result.classList.add("hidden");
    error.classList.add("hidden");

    // Check whether user entered anything
    if (subject.trim() === "" && body.trim() === "") {
        error.innerText = "Please enter an email subject or message.";
        error.classList.remove("hidden");
        return;
    }

    try {

        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                subject: subject,
                body: body
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        // Display result
        document.getElementById("resultTitle").innerText =
            data.result;

        document.getElementById("resultDescription").innerText =
            data.description;

        document.getElementById("confidence").innerText =
            data.confidence + "%";


        const icon = document.getElementById("resultIcon");


        if (data.result === "SPAM") {

            icon.innerText = "⚠️";

            icon.style.background = "#dc2626";

        } else {

            icon.innerText = "✓";

            icon.style.background = "#16a34a";
        }


        result.classList.remove("hidden");

    }

    catch (err) {

        error.innerText =
            "Something went wrong: " + err.message;

        error.classList.remove("hidden");
    }
}