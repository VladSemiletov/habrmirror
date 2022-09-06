$( document ).ready(function() {
    $('.like-form').submit(function(e){
        e.preventDefault()

        const hab_id = $(this).attr('id')

        const likeText = $(`.like-btn${hab_id}`).text()
        const trim = $.trim(likeText)

        const url = $(this).attr('action')

        let result;
        const likes = $(`.like-count${hab_id}`).text()
        const trimCount = parseInt(likes)

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'hab_id': hab_id,
            },
            success: function(response) {
                if(trim === 'Не нравится') {
                    $(`.like-btn${hab_id}`).text('Нравится')
                    result = trimCount - 1
                } else {
                    $(`.like-btn${hab_id}`).text('Не нравится')
                    result = trimCount + 1
                }
                $(`.like-count${hab_id}`).text(result)
            },
            error: function(response) {
                console.log('error', response)
            }
        })
    })
});