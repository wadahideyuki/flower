$(function(){
  $(".modal").click(function(){
    $(this).fadeOut();
  });
  $(".modal-close").click(function(){
    $(".modal").fadeOut();
  });
  $(".col2-btn span").click(function(){
    var thisCont = $(this).attr("class");
    $(".modal").css({display:"flex"});

    $(".mdlCont").hide();
    $(".mdlCont." + thisCont).show();
    return false;
  });

  $(".modal-inner").click(function(e){
    e.stopPropagation();
  });


  $(".exhibitor-box .tabs h3").click(function(){
    var idx = $(".exhibitor-box .tabs h3").index(this);

    $(".exhibitor-box .tabs h3").removeClass("show");
    $(this).addClass("show");

    $(".exhibitor-box .box").removeClass("show");
    $(".exhibitor-box .box").eq(idx).addClass("show");
    return false;
  });





});