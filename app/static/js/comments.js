Comments = window.Comments || {};
(function (exports, $) {

    function displayNoComments() {
        noComments = $('<h3>', {
            'text': 'No comments have been posted yet.'
        });
        $('h4#comment-form').before(noComments);
    }

    /* Template string for rendering a comment. */
    var commentTemplate = (
    '<div class="media">' +
    '<a class="pull-left" href="{url}">' +
    '<img class="media-object" src="{gravatar}" />' +
    '</a>' +
    '<div class="media-body">' +
    '<h4 class="media-heading">{created_timestamp}</h4>{body}' +
    '</div></div>'
    );

    function renderComment(comment) {
        var createdDate = new Date(comment.created_timestamp).
            toDateString();
        return (commentTemplate
            .replace('{url}', comment.url)
            .replace('{gravatar}', comment.gravatar)
            .replace('{created_timestamp}', createdDate)
            .replace('{body}', comment.body));
    }

    function displayComments(comments) {
        $.each(comments, function (idx, comment) {
            var commentMarkup = renderComment(comment);
            $('h4#comment-form').before($(commentMarkup));
        });
    }

    function load(entryId) {
        var filters = [{
            'name': 'entry_id',
            'op': 'eq',
            'val': entryId
        }];
        var serializedQuery = JSON.stringify({'filters': filters});
        $.get('/api/comment', {'q': serializedQuery}, function (data) {
            if (data['num_results'] === 0) {
                displayNoComments();
            } else {
                displayComments(data['objects']);
            }
        });
    }


    /* Template string for rendering success or error messages. */
    var alertMarkup = (
    '<div class="alert alert-{class} alert-dismissable">' +
    '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
    '<strong>{title}</strong> {body}</div>');
    /* Create an alert element. */
    function makeAlert(alertClass, title, body) {
        var alertCopy = (alertMarkup
            .replace('{class}', alertClass)
            .replace('{title}', title)
            .replace('{body}', body));
        return $(alertCopy);
    }

    /* Retrieve the values from the form fields and return as an
     object. */
    function getFormData(form) {
        return {
            'name': form.find('input#name').val(),
            'email': form.find('input#email').val(),
            'url': form.find('input#url').val(),
            'body': form.find('textarea#body').val(),
            'entry_id': form.find('input[name=entry_id]').val()
        }
    }

    function bindHandler() {
        /* When the comment form is submitted, serialize the form data
         as JSON
         and POST it to the API. */
        $('form#comment-form').on('submit', function () {
            var form = $(this);
            var formData = getFormData(form);
            var request = $.ajax({
                url: form.attr('action'),
                type: 'POST',
                data: JSON.stringify(formData),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json'
            });
            request.success(function (data) {
                alertDiv = makeAlert('success', 'Success', 'your comment was posted.');
                form.before(alertDiv);
                form[0].reset();
            });
            request.fail(function () {
                alertDiv = makeAlert('danger', 'Error', 'your comment was not posted.');
                form.before(alertDiv);
            });
            return false;
        });
    }

    exports.load = load;
    exports.bindHandler = bindHandler;
})(Comments, jQuery);
