function myFunction() {
  alert("Hello! I am an alert box!");
}

let modal = new bootstrap.Modal($("#getPostflight"), {
  keyboard: false
});
let user = "martijn";

$("#getPostflightBtn").on("click", function () {
  if (user == "martijn") {
    console.log("user is martijn");
    modal.hide();
//    $("#getPostflight").hide();
  } else {
    console.log("user not found!");
    modal.show();
//    $("#getPostflight").show();
  }
})