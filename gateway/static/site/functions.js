/* 
 * Global functions
 * 
 */ 

(function ($) {

  function SetWidget(widget) {
    $(this).sortable({
      connectWith: this
    });

    $( widget ).addClass( "ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" ).find( ".widget-header" )
      .addClass( "ui-widget-header ui-corner-all" )
      .prepend( "<span class='ui-icon ui-icon-minusthick'></span>")
      .end()
      .find( ".widget-content" );
    $( ".widget-header .ui-icon" ).click(function() {
          $( this ).toggleClass( "ui-icon-minusthick" ).
              toggleClass( "ui-icon-plusthick" );
          $( this ).parents( ".widget:first" ).
              find( ".widget-content" ).toggle();
    });
 
}

    $.fn.setWidget = SetWidget;

})(jQuery); 
  
