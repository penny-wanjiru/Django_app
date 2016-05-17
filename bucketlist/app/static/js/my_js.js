$(".btn-edit").on("click", function(event) {
  var dataUrl = $(this).data("url");
  $("#updateBucketList").attr('action', dataUrl);
});