function selectOption(option) {
    if (option === "verify") {
        window.location.href = "verify.html";
    } else if (option === "signing") {
        window.location.href = "signing.html";
    } else if (option === "get-quals") {
        window.location.href = "get_quals.html";
    }
}


function verify(event) {
    event.preventDefault(); // Prevent the default form submission

    var fileInput = document.getElementById("fileInput");
    var resultDiv = document.getElementById("result");

    var file = fileInput.files[0];

    if (!file) {
        resultDiv.innerHTML = "Please select a file.";
        return;
    }

    var formData = new FormData();
    formData.append("file", file);

    // Use fetch to send the file to the server
    fetch('http://127.0.0.1:8001/verify', {
        method: 'POST',
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Handle the JSON data returned by the server
            console.log(data);
            // Update the resultDiv with the verification result
            resultDiv.innerHTML = "Verification Result: " + data.result;

        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to verify file. Please try again.');
        });
}

function getQualifications() {
    // Get input values
    var studentId = document.getElementById("studentId").value;
    var school = document.getElementById("school").value;
    var firstName = document.getElementById("firstName").value;
    var lastName = document.getElementById("lastName").value;
    var qualCode = document.getElementById("qualCode").value;

    // Validate inputs (you can add more validation as needed)
    if (!studentId || !school || !firstName || !lastName || !qualCode) {
        alert("Please fill in all the fields.");
        return;
    }
    // Display the result (you can customize this part)
    var requestData = {
        student_id: parseInt(studentId),
        school: school,
        first_name: firstName,
        last_name: lastName,
        qual_code: parseInt(qualCode)
    };

    fetch('http://127.0.0.1:8001/get_quals', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Decode base64 to binary
            var pdfContentBinary = atob(data.pdf_content_base64);

            // Convert binary to Blob
            var pdfBlob = new Blob([new Uint8Array([...pdfContentBinary].map(char => char.charCodeAt(0)))], { type: 'application/pdf' });

            // Create a Blob URL and create a link element to trigger the download
            var blobUrl = URL.createObjectURL(pdfBlob);
            var link = document.createElement('a');
            link.href = blobUrl;
            link.download = 'qualifications.pdf'; // Set the desired file name
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(blobUrl); // Clean up the Blob URL
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to retrieve qualifications. Please try again.');
        });
}



function login(event) {
    event.preventDefault();
    var email = document.getElementById("loginEmail").value;
    var pass = document.getElementById("loginPassword").value;
    var requestData = {
        email_address : email,
        password : pass
    };
    
    fetch('http://127.0.0.1:8001/token', {
        method: 'POST',
        body: JSON.stringify(requestData),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Invalid credentials');
            }
            return response.json();
        })
        .then(data => {
            console.log('API Response:', data);
            alert("Successfull log in!")
            // Bootstrap raise popups
            setTimeout(function () {
                showFileSigningForm();  // Fix: Correct the function call
            }, 2000);

        })
        .catch(error => {
            // Bootstrap raise popups
            console.error('Error:', error.message);
            alert('Failed to log in. Please try again.');
        });
}


function signup(event) {
    event.preventDefault();
    var formData = new FormData();
    var institutionName = document.getElementById("institutionName").value;
    var authority = document.getElementById("authority").value;
    var signupEmail = document.getElementById("signupEmail").value;
    var password = document.getElementById("signupPassword").value;
    var Data_request = {
        institutionName: institutionName,
        authority: authority,
        signupEmail: signupEmail,
        password: password
    };
    fetch('http://127.0.0.1:8001/auth', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(Data_request)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.error}`);
            }d
        })
        .then(data => {
            console.log('API Response:', data);
            // Boostrap rasise popups

            // If the response is successful, alert and redirect
            var contentBinary = atob(data.Private_key);
            var pemBlob = new Blob([new Uint8Array([...contentBinary].map(char => char.charCodeAt(0)))], { type: 'application/x-pem-file' });

            var blobUrl = URL.createObjectURL(pemBlob);
            var link = document.createElement('a');
            link.href = blobUrl;
            link.download = 'private_key.pem'; // Set the desired file name
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(blobUrl); // Clean up the Blob URL

            alert(data.Status);
            // Redirect to login page after a delay (e.g., 2000 milliseconds or 2 seconds)
            setTimeout(function () {
                showLoginForm(); // Replace 'path_to_login_page' with the actual path
            }, 2000);
        })
        .catch(error => {
            // Boostrap rasise popups
            console.error('Error:', error);
            alert("Fail to sign up. Please try again!");
        });
}
function showLoginForm() {
    hideAllForms();
    document.getElementById("loginForm").style.display = "block";
}
function showSignupForm() {
    hideAllForms();
    document.getElementById("signupForm").style.display = "block";
}

function showFileSigningForm() {
    hideAllForms();
    document.getElementById("fileSigningForm").style.display = "block";
}

function hideAllForms() {
    document.getElementById("loginForm").style.display = "none";
    document.getElementById("signupForm").style.display = "none";
    document.getElementById("fileSigningForm").style.display = "none";
}

