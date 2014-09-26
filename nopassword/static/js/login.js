$(document).ready(function () {

    $('#id_username').typeahead({
        name: 'username',
        remote: '/accounts/users.json',
        template: [
            '<h3>{{username}}</h3>',
            '<p>{{full_name}}</p>'
        ].join(''),
        engine: Hogan
    });
});