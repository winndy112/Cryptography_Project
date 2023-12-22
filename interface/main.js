function selectOption(option) {
    if (option === "verify") {
        window.location.href = "verify.html";
    } else if (option === "signing") {
        window.location.href = "signing.html";
    } else if (option === "get-quals") {
        window.location.href = "get_quals.html";
    }
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
    
    var requestData = {
        student_id: parseInt(studentId),
        school: school,
        first_name: firstName,
        last_name: lastName,
        qual_code: parseInt(qualCode)
    };

    fetch('http://192.168.2.134:8001/get_quals', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Status ${response.status}: ${response.statusText}`);
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
            alert('Failed to retrieve qualifications! ' + error.message);
        });
}



function login(event) {
    event.preventDefault();
    var email = document.getElementById("loginEmail").value;
    var pass = document.getElementById("loginPassword").value;
    
    if (!email || !pass) {
        alert("Please fill in all the fields.");
        return;
    }
    var requestData = {
        email_address: email,
        password: pass
    };

    fetch('http://192.168.2.134:8001/token', {
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
            // lưu token để kiểm tra khi kí
            localStorage.setItem('accessToken', data.access_token);
            alert("Successfull log in!")
            // đăng nhập thành công thì cho phép kí
            showFileSigningForm()
        })
        .catch(error => {
            // console.error('Error:', error.message);
            console.error('Error:', error);
            alert("Fail to log in: " + error.message); 
        });
}


function signup(event) {
    event.preventDefault();
    var institutionName = document.getElementById("institutionName").value;
    var authority = document.getElementById("authority").value;
    var signupEmail = document.getElementById("signupEmail").value;
    var password = document.getElementById("signupPassword").value;
    if (!institutionName || !authority || !signupEmail || !password) {
        alert("Please fill in all the fields.");
        return;
    }
    var Data_request = {
        institutionName: institutionName,
        authority: authority,
        signupEmail: signupEmail,
        password: password
    };

    fetch('http://192.168.2.134:8001/auth', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(Data_request)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`ERROR! Status ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('API Response:', data);

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
            
            console.error('Error:', error);
            alert("Fail to sign up! " + error.message);
        });
}

function getAccessToken() {
    // Retrieve the token from localStorage
    return localStorage.getItem('accessToken');
}

function signFile(event) {
    event.preventDefault();
    var school = document.getElementById("school").value;
    var firstName = document.getElementById("firstName").value;
    var lastName = document.getElementById("lastName").value;
    var inputFile = document.getElementById("inputFile").files[0];
    var privateKey = document.getElementById("privateKey").files[0];
    var resDiv = document.getElementById("result");
    var ins = document.getElementById("Nhà phát hành");
    // check input từ user
    if (!school || !firstName || !lastName ) {
        resDiv.innerHTML = "Please fill in all the fields.";
        return;
    }
    if (!inputFile || !privateKey) {
        resDiv.innerHTML = "Please select a file.";
        return;
    }
    
    const reader = new FileReader();
    
    reader.onload = function (e) {
        var inputFileBase64 = e.target.result.split(",")[1];
        reader.onload = function (e) {
            var privateKeyBase64 = e.target.result.split(",")[1];

            // Create a JSON object with the form data and file contents
            var jsonData = {
                school: school,
                firstName: firstName,
                lastName: lastName,
                inputFile: inputFileBase64,
                privateKey: privateKeyBase64,
            };
            console.log("JSON Data:", jsonData);
            fetch('http://192.168.2.134:8001/sign_file', {
                method: 'POST',
                body: JSON.stringify(jsonData),
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + getAccessToken(),
                },
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(responseData => {
                    const pdfContentBase64 = responseData.pdf_content;

                    // Decode base64 and create a Blob
                    const binaryData = atob(pdfContentBase64);
                    const arrayBuffer = new ArrayBuffer(binaryData.length);
                    const uint8Array = new Uint8Array(arrayBuffer);

                    for (let i = 0; i < binaryData.length; i++) {
                        uint8Array[i] = binaryData.charCodeAt(i);
                    }

                    const blob = new Blob([uint8Array], { type: 'application/pdf' });

                    // Create a download link and trigger the download
                    const downloadLink = document.createElement('a');
                    downloadLink.href = URL.createObjectURL(blob);
                    downloadLink.download = 'signed_file.pdf';
                    downloadLink.click();
                    resDiv.innerHTML = "Kí thành công cho sinh viên có ID " + responseData.id_sv;
                                        
                    ins.innerHTML = "Được kí bởi " + responseData.nguoiKi +" thuộc nhà phát hành: " + responseData.nhaPhatHanh;
                    
                })
                .catch(error => {
                    console.error('Error:', error);
                    // console.error('Error signing file:', error);
                    alert("Failed to sign file! " + error.message);
                });
        };

        reader.readAsDataURL(privateKey);
    };

    reader.readAsDataURL(inputFile);
}



function verify(event) {
    event.preventDefault(); // Prevent the default form submission

    var file = document.getElementById("fileInput").files[0];
    var resultDiv = document.getElementById("result");

    if (!file) {
        resultDiv.innerHTML = "Please select a file.";
        return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
        var fileContentBase64 = e.target.result.split(",")[1];
        var requestData = {
            file: fileContentBase64,
        };
        fetch('http://192.168.2.134:8001/verify', {
            method: 'POST',
            body: JSON.stringify(requestData),
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Status ${response.status} : ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                
                console.log(data);
                if (data.root_ca == false) {
                    resultDiv.innerHTML = "Xác thực chữ kí  thất bại của Root CA";
                }
                else {
                    
                    resultDiv.innerHTML = "Xác thực thành công chữ kí của Root CA: " + data.root_ca_name +
                                        "<br> Xác thực thành công!" +
                                        "<br> Văn bằng được kí bởi: " + data.authority_person +
                                        "<br> Nhà cung cấp: " + data.institution_name 

                }
                

            })
            .catch(error => {
                console.error('Error:', error);
                alert("Fail to verify! " + error.message); 
            });
    };
    reader.readAsDataURL(file);
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

