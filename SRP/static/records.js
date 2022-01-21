function toggleTable () {
  let selected_table = document.getElementById("table").value;
  let sectors = (document.getElementById("sector_table"));
  let aircraft = (document.getElementById("aircraft_table"));
    if (selected_table == "sectors") {
      sectors.style.display = "block";
      aircraft.style.display = "none";
    }
    else if (selected_table == "aircraft") {
      aircraft.style.display = "block";
      sectors.style.display = "none";
    }
  }


$(document).ready(function () {
  var sectorTable = $('#sector').DataTable({
    ajax: "/api/sector_records",
    serverSide: true,
    scrollX: true,
    scrollY: "55vh",
    bStateSave: true,
    fixedHeader: true,
    dom: "<'row'<'col-sm-12 col-md-4'l><'col-sm-12 col-md-4 tableSelect'><'col-sm-12 col-md-4'f>>" +
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
    columns: [
      {data: "flight_id", visible: false},
      {data: "ac"},
      {data: "callsign"},
      {data: "p1"},
      {data: "p2"},
      {data: "crew"},
      {data: "airport_dep"},
      {data: "airport_des"},
      {data: "srp"},
      {data: "date"},
      {data: "task", visible: false},
      {data: "task_desc", orderable: false, searchable: false, visible: false},
      {data: "fuel_bfwd", orderable: false, searchable: false, visible: false},
      {data: "depfuel_uplift_exp", orderable: false, searchable: false, visible: false},
      {data: "depfuel_uplift_act", orderable: false, searchable: false, visible: false},
      {data: "depfuel_total", orderable: false, searchable: false, visible: false},
      {data: "oil_uplift_l", orderable: false, searchable: false, visible: false},
      {data: "oil_uplift_r", orderable: false, searchable: false, visible: false},
      {data: "oil_dep_l", orderable: false, searchable: false, visible: false},
      {data: "oil_dep_r", orderable: false, searchable: false, visible: false},
      {data: "tks_preflight", orderable: false, searchable: false, visible: false},
      {data: "deantiice_type", orderable: false, searchable: false, visible: false},
      {data: "deantiice_temp", orderable: false, searchable: false, visible: false},
      {data: "deantiice_time", orderable: false, searchable: false, visible: false},
      {data: "deantiice_mix", orderable: false, searchable: false, visible: false},
      {data: "holdovertime", orderable: false, searchable: false, visible: false},
      {data: "takeoff_mass", orderable: false, searchable: false},
      {data: "preflight_signature", visible: false},
      {data: "preflight_callsign", visible: false},
      {data: "landfuel_main_l", orderable: false, searchable: false, visible: false},
      {data: "landfuel_main_r", orderable: false, searchable: false, visible: false},
      {data: "landfuel_aux_l", orderable: false, searchable: false, visible: false},
      {data: "landfuel_aux_r", orderable: false, searchable: false, visible: false},
      {data: "landfuel_other_l", orderable: false, searchable: false, visible: false},
      {data: "landfuel_other_r", orderable: false, searchable: false, visible: false},
      {data: "tks_postflight", orderable: false, searchable: false, visible: false},
      {data: "blockoff", orderable: false, searchable: false},
      {data: "takeoff", orderable: false, searchable: false},
      {data: "landing", orderable: false, searchable: false},
      {data: "blockon", orderable: false, searchable: false},
      {data: "landing_day", orderable: false, searchable: false, visible: false},
      {data: "landing_night", orderable: false, searchable: false, visible: false},
      {data: "postflight_signature", visible: false},
      {data: "postflight_callsign", visible: false}
      ],
  });

  $(".tableSelect").append($("#tableSelect"))

  $("input").on("click", function () {
    var column = sectorTable.column( $(this).attr('data-column') );
    if ($(this).is(":checked")) {
      column.visible(true);
    } else {
      column.visible(false);
      }
  } )
})


//    var vis = function () {
//      var column = sectorTable.column( $(this).attr('data-column') );
//      if (column.visible(true)) {
//        $(this).is(":checked")
//      } else {
//        $(this).is(":!checked");
//        }
//    }


//    function setVis() {
//    let col = $( document.getElementById("flight_id") ).data( "name" )
////    var col = sectorTable.column( $(this ).attr( "data-name" ));
//    console.log(col)
//    bool = document.getElementById(col).checked
//    return bool
//    }
//console.log(setVis())


$(document).ready(function () {
  $('#aircraft').DataTable({
    ajax: "/api/aircraft_records",
    severSide: true,
    scrollX: true,
    scrollY: "55vh",
    bStateSave: true,
    dom: "<'row'<'col-sm-12 col-md-4'l><'col-sm-12 col-md-4 tableSelect'><'col-sm-12 col-md-4'f>>" +
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
    fixedHeader: true,
    columns: [
      {data: "aircraft_id", visible: false},
      {data: "registration"},
      {data: "defect", orderable: false},
      {data: "servicetime", orderable: false, searchable: false},
      {data: "hours", searchable: false},
      {data: "landing_day_total", searchable: false},
      {data: "landing_night_total", searchable: false},
      {data: "status"},
      {data: "fuel", orderable: false, searchable: false},
      {data: "oil_l", orderable: false, searchable: false},
      {data: "oil_r", orderable: false, searchable: false},
      {data: "tks", orderable: false, searchable: false},
      {data: "srp"},
      {data: "callsign"},
      {data: "location"},
      {data: "cycles", searchable: false}
      ],
    });
    $(".tableSelect").append($("#tableSelect"))
})
