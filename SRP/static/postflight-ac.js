
function postFltBtnText () {
  let ac = $("#preflight_ac").val();
  $("#selected_aircraft").text(ac);
}
$(document).ready(function () {
  postFltBtnText();
})
$("#preflight_ac").change(postFltBtnText);
