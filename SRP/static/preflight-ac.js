
function preFltBtnText () {
  let ac = $("#aircraft").val();
  $(".selected_aircraft").text(ac);
}
$(document).ready(function () {
  preFltBtnText();
})
$("#aircraft").change(preFltBtnText);
