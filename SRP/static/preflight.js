let upliftAct = document.getElementById("uplift_act");
let fuelBfwd = document.getElementById("fuel_bfwd");
let depFuel = document.getElementById("departure_fuel");


function updateUpliftExp() {
  document.getElementById("uplift_exp").value = upliftAct.value;
}


function updateDepFuel() {
  document.getElementById("departure_fuel").value = +upliftAct.value + +fuelBfwd.value;
}


function updateUpliftAct() {
  document.getElementById("uplift_act").value = +depFuel.value - +fuelBfwd.value;
}

$("#preflightConfirmCb").change (function() {
  $("#preflightConfirmBtn").attr("disabled", !this.checked)
});

$('#preflightSubmit').on('click', function(){
  let date = new Date($('#date').val());
  let day = date.getDate().toString().padStart(2, 0);
  let month = (date.getMonth() + 1).toString().padStart(2, 0);
  let year = date.getFullYear();
  $("#date_input").text([year, month, day].join('-'));
  if ($("#departure").val()!="") {
    $("#departure_input").text($("#departure").val().toUpperCase()).css("color", "initial");
  } else {
    $("#departure_input").text("This data is required").css("color", "red");
    };
  if ($("#destination").val()!="") {
    $("#destination_input").text($("#destination").val().toUpperCase()).css("color", "initial");
  } else {
    $("#destination_input").text("This data is required").css("color", "red");
    };
  if ($("#pic").val()!="") {
    $("#pic_input").text($("#pic").val().toUpperCase()).css("color", "initial");
  } else {
    $("#pic_input").text("This data is required").css("color", "red");
    };
  if ($("#pilot2").val()!="") {
    $("#p2_input").text($("#pilot2").val().toUpperCase());
  } else {
    $("#p2_input").text("---");
    };
  if ($("#crew").val()!="") {
    $("#crew_input").text($("#crew").val().toUpperCase());
  } else {
    $("#crew_input").text("---");
    };
  if ($("#pax").val()!="") {
    $("#pax_input").text($("#pax").val().toUpperCase());
  } else {
    $("#pax_input").text("---");
    };
  if ($("#tom").val()!="") {
    $("#tom_input").text($("#tom").val().toUpperCase()).css("color", "initial");
  } else {
    $("#tom_input").text("This data is required").css("color", "red");
    };
  if ($("#dep_oil_l").val()!="") {
    $("#oil_l_input").text($("#dep_oil_l").val().toUpperCase()).css("color", "initial");
  } else {
    $("#oil_l_input").text("This data is required").css("color", "red");
    };
  if ($("#dep_oil_r").val()!="") {
    $("#oil_r_input").text($("#dep_oil_r").val().toUpperCase()).css("color", "initial");
  } else {
    $("#oil_r_input").text("This data is required").css("color", "red");
    };

  if ($("#tks_to").val()!="") {
    $("#tks_input").text($("#tks_to").val().toUpperCase());
  } else {
    $("#tks_input").text("---");
    };
});

function getPreflight () {
  let preflight_signee = $("#preflight_signee").text();
  let ac = $("#ac").text();
  let active_preflight_regs = document.getElementById("active_preflight_regs").getElementsByTagName("li");
  let preflight_count = Object.values(active_preflight_regs).length;
  let preflight_regs = [];
  for (let i=0; i<preflight_count; ++i) {
    preflight_regs.push((active_preflight_regs)[i].innerText);
  }
  if ((preflight_signee != "") && ($.inArray(ac, preflight_regs) > -1)) {
    let preflightModal = new bootstrap.Modal($("#getPreflight"));
    preflightModal.show();
  }
};
$(document).ready(function () {
  getPreflight();
})

$("#preflight_aircraft").change(getPreflight);


$(document).ready(function () {
  setPreflight();
})
function setPreflight () {
  let ac = $("#preflight_aircraft").val();
  $(".selected_aircraft").text(ac);
  $(".preflight_route").attr("href", ac);
}
$("#preflight_aircraft").change(setPreflight);
