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
    var qualCode = document.getElementById("qualCode").value;

    // Validate inputs (you can add more validation as needed)
    if (!studentId || !qualCode) {
        alert("Please fill in all the fields.");
        return;
    }

    var requestData = {
        student_id: parseInt(studentId),
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
                throw new Error(`Status ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            var pdfContentBinary = atob(data.pdf_content_base64);
            var publicKey = atob(data.public);
            var pdfBlob = new Blob([new Uint8Array([...pdfContentBinary].map(char => char.charCodeAt(0)))], { type: 'application/pdf' });
            var pubBlob = new Blob([new Uint8Array([...publicKey].map(char => char.charCodeAt(0)))], { type: 'application/pem' });

            // Create download links
            var pdfLink = document.createElement('a');
            pdfLink.href = URL.createObjectURL(pdfBlob);
            pdfLink.download = 'qualifications.pdf';
            document.body.appendChild(pdfLink);

            var pubLink = document.createElement('a');
            pubLink.href = URL.createObjectURL(pubBlob);
            pubLink.download = 'public_key.pem';
            document.body.appendChild(pubLink);

            // Trigger downloads
            pdfLink.click();
            pubLink.click();

            // Remove the links and clean up the Blob URLs
            document.body.removeChild(pdfLink);
            document.body.removeChild(pubLink);
            URL.revokeObjectURL(pdfBlob);
            URL.revokeObjectURL(pubBlob);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to retrieve qualifications! ' + error.message);
        });
}



function createKey(event) {
    event.preventDefault();
    fetch('http://127.0.0.1:8001/create_key', {
        method: 'POST',
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
            alert("Fail to create private key! " + error.message);
        });
}


function signFile(event) {
    event.preventDefault();
    // ins infor 
    var insName = document.getElementById("InstitutionName").value;
    var auth = document.getElementById("AuthorityName").value;
    var mail = document.getElementById("Email").value;
    // student infor
    var school = document.getElementById("school").value;
    var studentName = document.getElementById("studentName").value;

    var inputFile = document.getElementById("inputFile").files[0];
    var privateKey = document.getElementById("privateKey").files[0];
    var resDiv = document.getElementById("result");
    var ins = document.getElementById("Nhà phát hành");
    // check input từ user
    if (!school || !studentName || !insName || !auth || !mail) {
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
                ins: insName,
                authority: auth,
                email: mail,
                school: school,
                studentName: studentName,
                inputFile: inputFileBase64,
                privateKey: privateKeyBase64,
            };
            console.log("JSON Data:", jsonData);
            fetch('http://127.0.0.1:8001/sign_file', {
                method: 'POST',
                body: JSON.stringify(jsonData),
                headers: {
                    'Content-Type': 'application/json',
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

                    ins.innerHTML = "Được kí bởi " + responseData.nguoiKi + " thuộc nhà phát hành: " + responseData.nhaPhatHanh;

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
    event.preventDefault();

    var file = document.getElementById("fileInput").files[0];
    var pubkey = document.getElementById("publicFile").files[0];
    var resultDiv = document.getElementById("result");

    if (!file || !pubkey) {
        resultDiv.innerHTML = "Please select a file.";
        return;
    }

    const fileReader = new FileReader();
    fileReader.onload = function (e) {
        const fileContentBase64 = e.target.result.split(",")[1];

        const pubkeyReader = new FileReader();
        pubkeyReader.onload = function (e) {
            const pubkeyContentBase64 = e.target.result.split(",")[1];

            var requestData = {
                file: fileContentBase64,
                pubKey: pubkeyContentBase64, // Change 'pubkey' to 'pubKey' to match the Pydantic model
            };

            fetch('http://127.0.0.1:8001/verify', {
                method: 'POST',
                body: JSON.stringify(requestData),
                headers: {
                    'Content-Type': 'application/json',
                },
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
                    resultDiv.innerHTML = "Xác thực chữ kí thất bại của Root CA";
                } else {
                    if (data.result == true) {
                        resultDiv.innerHTML = "Xác thực thành công chữ kí của Root CA: " + data.root_ca_name +
                        "<br> Xác thực thành công!" +
                        "<br> Văn bằng được kí bởi: " + data.authority_person +
                        "<br> Nhà cung cấp: " + data.institution_name;
                    }
                    else {
                        resultDiv.innerHTML= " Xác thực văn bằng thất bại!" + " Lí do: " +data.reason;
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("Fail to verify! " + error.message);
            });
        };

        pubkeyReader.readAsDataURL(pubkey);
    };

    fileReader.readAsDataURL(file);
}


function showCreateForm() {
    hideAllForms();
    document.getElementById("createKey").style.display = "block";
}

function showSigningForm() {
    hideAllForms();
    document.getElementById("fileSigningForm").style.display = "block";
}

function hideAllForms() {
    document.getElementById("navigations").style.display = "none";
    document.getElementById("createKey").style.display = "none";
    document.getElementById("fileSigningForm").style.display = "none";
}