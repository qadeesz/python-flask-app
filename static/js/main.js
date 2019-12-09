
$(document).ready(function () {

    $('.randomPassword').val(randomString());

    // $('#addPersonBtn').on('click', function(){
    //     $('.randomPassword').val(randomString());
    //     console.log(randomString())
    // });


    $('#editModal').on('shown.bs.modal', function (event) {
        
        clickBtn = $(event.relatedTarget)
        if(clickBtn.data('action') == 'add'){
            $('.randomPassword').val(randomString());
        } 
        
        if (clickBtn.data('action') == 'edit'){
            var row = $('#row-'+ clickBtn.data('row') );
            console.log(row);
            var modal = $(this)
            modal.find('input#username').val(row.find('td.username').text())
            // modal.find('.modal-body input').val(recipient)
        }

      })
  
});


    function editRow(row){
        console.log(row)
    }

    function randomString(){
        return Math.random().toString(36).substring(7);
    }