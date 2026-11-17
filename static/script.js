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

    const formData = new FormData(form);

    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        throw new Error("Server error: " + response.status);
    }

    const absences = await response.json();

    const lines = absences.map((count, i) => `Period ${i + 1}: ${count}`);
    document.getElementById("results").textContent = lines.join("\n");

    const big_div = document.getElementsByClassName("start")[0];
    big_div.style.display = 'none';

    const upload_div = document.getElementsByClassName("uploaded")[0];
    upload_div.style.display = 'block';
    
});
