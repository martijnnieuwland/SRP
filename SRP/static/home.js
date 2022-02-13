$(".postflightBtn").on("click", function (event) {
  let postflightModal = new bootstrap.Modal($("#getPostflight"));
  let user_name_last = $("#user_name_last").text();
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
});

function setPostflight () {
  let ac = $("#postflight_aircraft").val();
  $("#selected_aircraft").text(ac);
  $(".postflight_route").attr("href", "postflight/" + ac);
}
$(document).ready(function () {
  setPostflight();
})
$("#postflight_aircraft").change(setPostflight);

console.log($("#postflight_ac").val())
//
//let user_name_last = $("#user_name_last").text()
////console.log(user_name_last)
//let preflight_items = document.getElementById("preflight_names").getElementsByTagName("li");
//let preflight_count = Object.values(preflight_items).length;
//let preflight_names = []
//for (let i=0; i<preflight_count; ++i) {
//  preflight_names.push((preflight_items)[i].innerText);
////  console.log((preflight_items)[i].innerText);
//}
//
////console.log($.inArray(user_name_last, preflight_names) > -1);
