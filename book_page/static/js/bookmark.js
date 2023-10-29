 //delete bookmark
 function deleteBookmark(idBuku) {
    fetch(`delete-bookmark/${idBuku}`, {
        method: "DELETE",
    })
    return false
}

//RefreshPage
function refreshpage(){
    window.location.href = "bookmark";
}