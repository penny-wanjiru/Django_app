$(".btn-edit").on("click", function(event) {
  var dataUrl = $(this).data("url");
  $("#updateBucketList").attr('action', dataUrl);
});

$(".btn-item").on("click", function(event) {
  var dataUrl = $(this).data("url");
  $("#updateitem").attr('action', dataUrl);
});

$(".delete-item").on("click", function(event) {
  event.preventDefault();
  var a = $(this).attr('link');
  swal({
    title: "Are you sure?",
    text: "You will not be able to recover this item!",
    type: "warning",
    showCancelButton: true,
    confirmButtonColor: "#c62828",
    confirmButtonText: "Yes, delete it!",
    cancelButtonText: "No, cancel!",
    closeOnConfirm: false,
    closeOnCancel: false
  },
  function(isConfirm) {
    if (isConfirm) {
      $.get(a);
      swal("Deleted!", "Your item has been deleted.", "success");
    } else {
      swal("Cancelled", "Your item is still safe", "error");
    }
    location.reload();
  });
});

$(".delete-bucket").on("click", function(event) {
  event.preventDefault();
  var a = $(this).attr('links');
  swal({
    title: "Are you sure?",
    text: "You will not be able to recover this item!",
    type: "warning",
    showCancelButton: true,
    confirmButtonColor: "#c62828",
    confirmButtonText: "Yes, delete it!",
    cancelButtonText: "No, cancel!",
    closeOnConfirm: false,
    closeOnCancel: false
  },
  function(isConfirm) {
    if (isConfirm) {
      $.get(a);
      swal("Deleted!", "Your item has been deleted.", "success");
    } else {
      swal("Cancelled", "Your item is still safe", "error");
    }
    location.reload();
  });
});

$(document).ready(function() {
  $('.modal-trigger').leanModal();
  $(".flash-message").fadeOut(4000);
});

function sendCheck(itemId, status) {
  window.location.href += itemId + '/status';
}
