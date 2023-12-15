 //delete bookmark
 function deleteBookmark(idBuku) {
    fetch(`../../delete-bookmark/${idBuku}/`, {
        method: "DELETE",
    })
}

//RefreshPage
function refreshpage(){
    window.location.href = "bookmark";
}