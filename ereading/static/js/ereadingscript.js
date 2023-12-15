// Dashboard Admin
async function getEreadingsAdmin() {
    return fetch('get-json/').then((res) => res.json());
}

async function refreshEreadingsAdmin() {
    let ereadings = await getEreadingsAdmin();
    let htmlString = ``;

    ereadings.forEach((ereading) => {
        let dateObject = new Date(ereading.fields.last_updated);
        let formattedDate = dateObject.toLocaleDateString(); 
        let formattedTime = dateObject.toLocaleTimeString();

        if (ereading.fields.state == 0) {
            htmlString += `
                <div class="col mb-4">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center" style="background-color: #CCFFFF">
                            <span><strong>Added by:</strong> ${ereading.fields.created_by}</span>
                        </div>
    
                        <div class="card-body text-center">   
                            <p class="card-text"><strong>Title: </strong>${ereading.fields.title}</p> 
                            <p class="card-text"><strong>Author: </strong>${ereading.fields.author}</p>
                            <p class="card-text"><strong>Desc: </strong>${ereading.fields.description}</p>
                            <p class="card-text"><strong>Link: </strong><a href="${ereading.fields.link}" target="_blank">${ereading.fields.link}</a></p>
                        </div>

                        <div class="mb-2" aria-label="Item Actions">
                            <button class="btn btn-success btn-sm" onclick="acceptEreading(${ereading.pk})">Accept</button>
                            <button class="btn btn-danger btn-sm" onclick="rejectEreading(${ereading.pk})">Reject</button>
                        </div>

                        <div class="card-footer text-center">
                            <small class="text-muted">Last Updated: </strong>${formattedDate} | ${formattedTime}</small>
                        </div>
                    </div>
                </div>
            `;
        } 
    });
    document.getElementById("ereadings-display").innerHTML = htmlString;
}
refreshEreadingsAdmin();

async function acceptEreading(id) {
    let form = new FormData();
    form.append("id", id);

    await fetch('accept-ereading/', {
        method: "POST",
        body: form,
    }).then(refreshEreadingsAdmin);
}

async function rejectEreading(id) {
    let form = new FormData();
    form.append("id", id);

    await fetch('reject-ereading/', {
        method: "POST",
        body: form,
    }).then(refreshEreadingsAdmin);
}

// Dashboard User
// JavaScript untuk menerapkan filter katalog buku.
document.getElementById('selectedGenre').addEventListener('input', function() {
    var selectedGenre = this.value;
    var htmlDictBooks = document.getElementById('dict-books');
    var dictBooks = JSON.parse(htmlDictBooks.dataset.myValue);

    selectedBook.value = '';
    bookOptions.innerHTML = '';

    if (selectedGenre == 'All') {
        for (var book in dictBooks) {
            var option = document.createElement('option');
            option.value = book;
            bookOptions.appendChild(option);
            }
        selectedBook.style.display = 'block';

    } else {
        if (selectedGenre) {
            for (var book in dictBooks) {
                if (dictBooks[book].includes(selectedGenre)) {
                    var option = document.createElement('option');
                    option.value = book;
                    bookOptions.appendChild(option);
                }
            }
            selectedBook.style.display = 'block';

        } else {
            selectedBook.style.display = 'none';
        }
    }
});

async function getEreadings() {
    return fetch(`get-json/`).then((res) => res.json());
}

async function refreshEreadings() {
    let ereadings = await getEreadings();
    let htmlString = ``;

    ereadings.forEach((ereading) => {
        let dateObject = new Date(ereading.fields.last_updated);
        let formattedDate = dateObject.toLocaleDateString(); 
        let formattedTime = dateObject.toLocaleTimeString();

        if (ereading.fields.state == 0) {
            htmlString += `
                <div class="col mb-4">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center" style="background-color: #CCFFFF">
                            <span><strong>Title: </strong>${ereading.fields.title}</span>
                        </div>
    
                        <div class="card-body text-center">   
                            <p class="card-text"><strong>Status:</strong> Bukumu sedang diperiksa oleh admin.</p>
                        </div>

                        <div class="card-footer text-center">
                            <small class="text-muted">Last Updated: </strong>${formattedDate} | ${formattedTime}</small>
                        </div>
                    </div>
                </div>
            `;
        
        } else if (ereading.fields.state == 1) {
            htmlString += `
                <div class="col mb-4">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center" style="background-color: #CCFFFF">
                            <span><strong>Title: </strong>${ereading.fields.title}</span>    
                            <button class="btn btn-danger btn-sm" onclick="deleteEreading(${ereading.pk})">Delete</button>
                        </div>
    
                        <div class="card-body text-center">    
                            <p class="card-text"><strong>Author: </strong>${ereading.fields.author}</p>
                            <p class="card-text"><strong>Desc: </strong>${ereading.fields.description}</p>
                            <p class="card-text"><strong>Link: </strong><a href="${ereading.fields.link}" target="_blank">${ereading.fields.link}</a></p>
                        </div>

                        <div class="card-footer text-center">
                            <small class="text-muted">Last Updated: </strong>${formattedDate} | ${formattedTime}</small>
                        </div>
                    </div>
                </div>
            `;
        } else if (ereading.fields.state == 2) {
            htmlString += `
                <div class="col mb-4">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center" style="background-color: #CCFFFF">
                            <span><strong>Title: </strong>${ereading.fields.title}</span>   
                            <button class="btn btn-danger btn-sm" onclick="deleteEreading(${ereading.pk})">Delete</button>
                        </div>
    
                        <div class="card-body text-center">    
                            <p class="card-text"><strong>Status:</strong> Bukumu ditolak karena tidak memenuhi ketentuan yang berlaku.</p>
                        </div>

                        <div class="card-footer text-center">
                            <small class="text-muted">Last Updated: </strong>${formattedDate} | ${formattedTime}</small>
                        </div>
                    </div>
                </div>
            `;
        }
    });
    document.getElementById("ereadings-display").innerHTML = htmlString;
}
refreshEreadings();

function addEreading() {
    var formElement = document.getElementById("form");
    var formData = new FormData(formElement);

    var data = {};
    formData.forEach(function(value, key){
        data[key] = value;
    });

    fetch('add-ereading/', {
        method: "POST",
        body: JSON.stringify(data),
    })
    .then(response => {
    if (!response.ok) {
        throw new Error('Buku tidak dapat ditambahkan! Pastikan setiap field sudah diisi dan sesuai dengan contoh!');
    }})
    .then(refreshEreadings) // Ereading akan ditampilkan jika data yang diisikan dalam form sudah valid.
    .catch(error => {
        alert(error.message);
    });

    document.getElementById("form").reset()
    return false
}
document.getElementById("button_add").onclick = addEreading

async function deleteEreading(id) {
    let form = new FormData();
    form.append("id", id);

    await fetch('delete-ereading/', {
        method: "POST",
        body: form,
    }).then(refreshEreadings);
}