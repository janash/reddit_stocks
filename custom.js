function load_file(file_url, data_type){
    var return_data = []
    $.ajax({
        url: file_url,
        async: false,
        dataType: data_type,
        success: function (data) {
            return_data = data
        }
    });
    return return_data
    }

function loadTable(href) {
    try {
        table.destroy();
        $('#csv-data tr').remove();
        $('#csv-data thead').remove();
        $('#csv-data tbody').remove();
    } catch {
        // Do nothing.
    }

    var csvData = load_file(href, 'text')
    var separated = $.csv.toArrays(csvData)

    var headers = [];
    for (var j=0; j<separated[0].length; j++) {
        headers.push( {'title': separated[0][j]} )
    }

    var data = separated.slice(1,)

    for (let i=0; i<data.length; i++) {
        
        let num = parseFloat(data[i][1])

        if ( Math.sign(num) == 1 ) {
            data[i][1] = `<button type="button" class="btn btn-success">${num.toFixed(3)} </btn>`
        }

        if ( Math.sign(num) == -1 ) {
            data[i][1] = `<button type="button" class="btn btn-danger">${num.toFixed(3)} </btn>`
        }

    }
    
    table = $('#csv-data').DataTable({
        "responsive": true,
        "aaData": data,
        "columns": headers,
        "initComplete": function (settings, json) {  
            $("#csv-data").wrap("<div style='overflow:auto; width:100%;position:relative;'></div>");
        },
    });

}

$(document).ready( function () {
    loadTable("https://raw.githubusercontent.com/janash/reddit_stocks/data/website_data/overall_top50.csv")

    buttons = document.getElementsByClassName('btn-outline-reddit')

    for (i=0; i<buttons.length; i++) {
        buttons[i].onclick = function() {
            loadTable(`https://raw.githubusercontent.com/janash/reddit_stocks/data/website_data/${this.id}_top50.csv`)
            
            // remove active class from all buttons
            for (j=0; j<buttons.length; j++) {
                buttons[j].classList.remove("active")
            }

            // add active class for button of interest
            this.classList.add("active")
        };
    }

});
