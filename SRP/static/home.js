function getPostflight () {
  let postflightModal = new bootstrap.Modal($("#getPostflight"));
  let user_name_last = document.getElementById("user_name_last").ariaLabel;
  let preflight_items = document.getElementById("preflight_names").getElementsByTagName("li");
  let preflight_count = Object.values(preflight_items).length;
  let preflight_names = [];
  let postflight_ac = $("#postflight_ac").val();
  for (let i=0; i<preflight_count; ++i) {
    preflight_names.push((preflight_items)[i].innerText);
}
  if ($.inArray(user_name_last, preflight_names) > -1) {
    postflightModal.hide();
    $(".postflight_route").attr("href", "postflight/" + postflight_ac);
  } else {
    event.preventDefault();
    postflightModal.show();
  }
};
$(".postflightBtn").click(getPostflight);

function setPostflight () {
  let ac = $("#postflight_aircraft").val();
  $("#selected_aircraft").text(ac);
  $(".postflight_route").attr("href", "postflight/" + ac);
}
$(document).ready(function () {
  setPostflight();
})
$("#postflight_aircraft").change(setPostflight);

$("#cancel").on("click", function(){
  $('.modal').remove();
  $('.modal-backdrop').remove();
});

$(document).ready(function () {
  setPreflight();
})
function setPreflight () {
  let ac = $("#aircraft").val();
  $("#preflightBtn").text(ac);
}
$("#aircraft").change(setPreflight);
