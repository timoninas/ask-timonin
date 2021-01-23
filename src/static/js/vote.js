$('.js-vote').click(function(ev) {
    console.log("HERE: ")
    ev.preventDefault();
    var $this = $(this),
        action = $this.data('action'),
        pk = $this.data('pk');

     $.ajax('/vote/', {
        method: 'POST',
        data: {
            action: action,
            pk: pk,
        },
     }).done(function(data) {
        console.log("DATA: " + data);
     });
     console.log("HERE: " + action + " " + pk)
});
