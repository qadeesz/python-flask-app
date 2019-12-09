
$(document).ready(function () {

    const api_url =  'http://127.0.0.1:5000'
    $('.randomPassword').val(randomString());

    // $('#addPersonBtn').on('click', function(){
    //     $('.randomPassword').val(randomString());
    //     console.log(randomString())
    // });


    $('#editModal').on('shown.bs.modal', function (event) {

        clickBtn = $(event.relatedTarget)
        if (clickBtn.data('action') == 'add') {
            $('.randomPassword').val(randomString());
        }

        if (clickBtn.data('action') == 'edit') {
            var row = clickBtn.data('row');
            console.log(row);
            var modal = $(this)
        //    setTimeout(function(){
        //     modal.find('input#username').val(row.username)
        //     modal.find('input#email').val(row.email)
        //     modal.find('input#role').val(row.role)
        //    },1000)
        }

    })



    //SEARCH USER RESULT
    // if(window.location.pathname == '/admin'){
    //     load_data();
    // }

    // function load_data(query) {
    //     $.ajax({
    //         url: api_url+"/search",
    //         method: "POST",
    //         data: { query: query },
    //         success: function (data) {
    //             $('#result').html(data);
    //         }
    //     });
    // }

    // $('#search').keyup(function () {
    //     var search = $(this).val();
    //     if (search != '') {
    //         load_data(search);
    //     }
    //     else {
    //         load_data();
    //     }
    // });


});


function editRow(row) {
    console.log(row)
}

function randomString() {
    return Math.random().toString(36).substring(7);
}