$('#myModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var bookId = button.data('book-id');
    var bookTit = button.data('book-title')
    var bookAut = button.data('book-author')
    var bookIsbn = button.data('book-isbn')
    var bookGen = button.data('book-genre')
    var bookSta = button.data('book-status')

    // Update the modal's content
    var modal = $(this);
    modal.find('.modal-body #modal-id').html('<strong>Book ID:</strong>&nbsp; ' + bookId);
    modal.find('.modal-body #modal-tit').html('<strong>Book Title:</strong>&nbsp; ' + bookTit);
    modal.find('.modal-body #modal-aut').html('<strong>Book Author:</strong>&nbsp; ' + bookAut);
    modal.find('.modal-body #modal-isbn').html('<strong>Book Isbn:</strong>&nbsp; ' + bookIsbn);
    modal.find('.modal-body #modal-gen').html('<strong>Book Genre:</strong>&nbsp; ' + bookGen);
    if (bookSta === 'available') {
        modal.find('.modal-body #modal-sta').html('<div style="background-color: green; width: 100px; color: white; border-radius: 20px; text-align: center;">' + bookSta + '</div>');
    } 
    else{
        modal.find('.modal-body #modal-sta').html('<div style="background-color: red; width: 100px; color: white; border-radius: 20px; text-align: center;">' + bookSta + '</div>');
    }
});
