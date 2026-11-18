const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-upload');
const dropText = document.getElementById('drop-text');

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
    });
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    });
});

dropZone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        dropText.textContent = files[0].name;
        if (fileInput.files.length > 1) {
            dropText.textContent += " & " + (fileInput.files.length - 1) + " more file"
        } else if (fileInput.files.length > 2) {
            dropText.textContent += " & " + (fileInput.files.length - 1) + " more files"
        }
    }
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        dropText.textContent = fileInput.files[0].name;
        if (fileInput.files.length == 2) {
            dropText.textContent += " & " + (fileInput.files.length - 1) + " more file"
        } else if (fileInput.files.length > 2) {
            dropText.textContent += " & " + (fileInput.files.length - 1) + " more files"
        }
    }
});


const form = document.getElementById("submit-form");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const start_div = document.getElementsByClassName("start")[0];
    start_div.style.display = 'none';

    const upload_div = document.getElementsByClassName("uploaded")[0];
    upload_div.style.display = 'block';

    const bar = document.getElementById("progress-bar");
    const results = document.getElementById("results");

    results.textContent = "";
    const timer = startPsuedoProgress(bar, estimateMs(fileInput.files.length));
    const formData = new FormData(form);

    const backButton = document.getElementsByClassName("back")[0];
    backButton.style.display = "none"

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Server error: " + response.status);
        }

        const result_json = await response.json();

        const absences = result_json["absences"]
        const tardies = result_json["tardies"]
        
        bar.value = 100;
        const lines = absences.map((count, i) => `period ${i + 1}: ${count} absences (${tardies[i]} tardies)`);
        document.getElementById("results").textContent = lines.join("\n");

        backButton.style.display = "block"
    } catch (err) {
        console.error(err);
        bar.value = 0;
        document.getElementById("results").textContent = "Something went wrong. Try again.";
        backButton.style.display = "block"
    } finally {
        clearInterval(timer);
    }
});


function estimateMs(fileCount) {
    const batches = Math.ceil(fileCount / 3);
    return batches * 12000;
}

function startPsuedoProgress(bar, estimate) {
    const start = Date.now();
    bar.value = 0;
    return setInterval(() => {
        const elapsed = Date.now() - start;
        bar.value = 90 * (1 - Math.exp(-3 * elapsed / estimate));
    }, 100);
}


function goBack() {
    const start_div = document.getElementsByClassName("start")[0];
    start_div.style.display = 'block';

    const upload_div = document.getElementsByClassName("uploaded")[0];
    upload_div.style.display = 'none';
}


// const selectedRadio = document.querySelector('input[name="type"]:checked');

// pass the selected radio val to the python file and then like pass that as function?
