require(['jquery', "goog!maps,3.exp,other_params:sensor=false"], function($){
    $('.gmap').each(function(idx, el){

        new google.maps.Map(el, {
            center: new google.maps.LatLng($(el).data('latitude'),
                                         $(el).data('longitude')),
            zoom: $(el).data('zoomlevel')
        });

    });
});
