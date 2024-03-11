

// delete item function
function confirmDelete(event) {
    var r = confirm(deleteConfirmationMessage);
    if (r == true) {
      // User clicked OK, proceed with deletion
      return true;
    } else {
      // User clicked Cancel, prevent default action (deletion)
      event.preventDefault();
      return false;
    }
  }


// delete user function
document.addEventListener("DOMContentLoaded", function() {
    // Event listener needed to check that button is loaded. Without it is not working here

    var deleteButton = document.getElementById("deleteButton");
    if (deleteButton) {
        deleteButton.addEventListener("click", confirmAndRedirect);
    }

    // Define the confirmAndRedirect function
    function confirmAndRedirect() {
        if (confirm(deleteUserConfirmationMessage)) {
            // Redirect to the DeleteView URL
            window.location.href = deleteUserUrl;
        }
    }
});