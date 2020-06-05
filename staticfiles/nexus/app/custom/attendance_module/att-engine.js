$(function() {

    var csrftoken = Cookies.get('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    
    $('#calendar').fullCalendar({
        plugins: [ 'interaction' ],
        selectable: true,
        dayClick: function(date, jsEvent, view) {
            //alert('Clicked on: ' + date.format());
            // change the day's background color just for fun
            
            
            //$('#salary-summary span').text('today is ' + date.format());
            date_clicked = date.format();
            $.ajax({
                type : 'POST',
                url :  "{% url 'attd-register-attd' %}",
                data : {'date_clicked': date_clicked},
                success : function(response){
                //reset the form after successful submit
                    console.log('success')
                    console.log(response.css)
                    $('#date-summary').text(response.data)
                    $('#date-hours_worked').text(response.hours_worked)
                    if (response.hours_worked < 11) {
                        
                    }
                    $(this).css(response.css);
                },
                error : function(response){
                    console.log(response)
                }
            });
        },
        unselect: function( jsEvent, view ) {
            $('#date-summary').text('cleared')
            $('#date-hours_worked').text('')
        }
    })
});