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

        let tickerLink = `<span class="ticker-link" id="${data[i][0]}">${data[i][0]}</span>`

        data[i][0] = tickerLink
        
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
        "pageLength": 50,
        "initComplete": function (settings, json) {  
            $("#csv-data").wrap("<div style='overflow:auto; width:100%;position:relative;'></div>");
        },
    });

}

$(document).ready( function () {

    localStorage.clear()

    loadTable("https://raw.githubusercontent.com/janash/reddit_stocks/data/website_data/overall_top50.csv")

    buttons = document.getElementsByClassName('btn-outline-reddit')
    localStorage.setItem("subreddit", "overall")

    // Gather all subreddit names
    let subreddits = []

    // Define button behavior
    for (let i=0; i<buttons.length; i++) {
        
        if (i>0) {
            subreddits.push(buttons[i].id)
        }

        buttons[i].onclick = function() {
            loadTable(`https://raw.githubusercontent.com/janash/reddit_stocks/data/website_data/${this.id}_top50.csv`)
            
            // remove active class from all buttons
            for (j=0; j<buttons.length; j++) {
                buttons[j].classList.remove("active")
            }

            // add active class for button of interest
            this.classList.add("active")
            localStorage.setItem("subreddit", `${this.id}`)

            // Add ticker click behavior again
           
            let tickers = document.getElementsByClassName("ticker-link")

            for (let i=0; i<tickers.length; i++) {
                tickers[i].onclick = function() {
                    localStorage.setItem("ticker", this.id);
                    window.location = "comments.html";
                }
            }
        };

        localStorage.setItem("subreddits", subreddits)
    };

    // Define ticker link behavior
    let tickers = document.getElementsByClassName("ticker-link")

    for (let i=0; i<tickers.length; i++) {
        tickers[i].onclick = function() {
            localStorage.setItem("ticker", this.id);
            window.location = "comments.html";
        }
    }

});
