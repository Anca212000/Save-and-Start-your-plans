$(document).ready(function () {
  $("body").hide().fadeIn(1000);
  $(".loginBox").hide().fadeIn(1500).show();
});

$(document).ready(function () {
  $("#plusTask").click(function () {
    $(".toggleAddTask").slideDown().show();
  });
});

$(document).ready(function () {
  $("#buttCancelTask").click(function () {
    $(".toggleAddTask").slideUp();
  });
});

$(document).ready(function () {
  $("#repetitively").click(function () {
    $(".repetType").slideDown().show("slow");
    $(".onetimeType").fadeOut().hide();
    $(".specificdaysType").fadeOut().hide();
  });
});

$(document).ready(function () {
  $("#onetime").click(function () {
    $(".onetimeType").slideDown().show("slow");

    $(".repetType").fadeOut().hide();
    $(".specificdaysType").fadeOut().hide();
  });
});

$(document).ready(function () {
  $("#specificdays").click(function () {
    $(".specificdaysType").slideDown().show("slow");

    $(".repetType").fadeOut().hide();
    $(".onetimeType").fadeOut().hide();
  });
});

// $(document).ready(function () {
//   $("#editTask").click(function () {
//     $(".deleteMessage").slideDown().show("slow");
//   });
// });
// $(document).ready(function () {
//   $("#no").click(function () {
//     $(".deleteMessage").slideUp();
//   });
// });
