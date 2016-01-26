function makeItem(id, type, country, city, address, dress, cost) {
	return '<div class="dance-item" id="%%id%%"><p class="dance-type">%%type%%</p><p class="dance-location">%%country%%, %%city%%, %%address%%</p><p class="dance-dress">Dress Code — <span>%%dress%%</span></p><p class="dance-cost">Cost to Attend — $ <span>%%cost%%</span></p><button type="button" class="btn btn-default" disabled="true">Approved!</button><button type="button" class="btn btn-danger del-bttn">Delete</button></div>'.replace('%%id%%', id).replace('%%type%%', type).replace('%%country%%', country).replace('%%city%%', city).replace('%%address%%', address).replace('%%dress%%', dress).replace('%%cost%%', cost)
}

$(document).on('click', '.approve-bttn', function(){
	var elem = $(this).parent()
	$.getJSON('/dance/approve',
		 {
		 	object_id: $(this).parent().attr('id')
		 }, function(data){
		 	if(data.string == "200 OK"){
				elem.remove()
				hackerList.add( { dancetype: data.type, dancelocation: data.country + ', ' + data.city + ', ' + data.address, dancedress: data.dress, dancecost: data.cost } );
		 	}
		 });
});

$(document).on('click', '.del-bttn', function(){
	var elem = $(this).parent()
	$.getJSON('/dance/delete',
		 {
		 	object_id: $(this).parent().attr('id')
		 }, function(data){
		 	if(data.string == "200 OK"){
		 		var itemId = $(elem).attr('id')
				hackerList.remove('id', itemId);
		 		elem.parent().remove();
		 	}
		 });
});
