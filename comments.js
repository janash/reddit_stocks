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

function tickerArray(csvData, subredditName, ticker) {
    let separated = $.csv.toArrays(csvData)

    let data = separated.slice(1,)

    let tickerComments = []

    for (let i=0; i<data.length; i++) {
        if (data[i][1] == ticker ) {
            data[i].push(subredditName)
            tickerComments.push(data[i])
        }
    }

    return tickerComments
}

$(document).ready( function (){

    // Back button behavior
    document.getElementById("back-button").onclick = function() {

        window.location = "index.html"
    }

    let subreddit = localStorage.getItem("subreddit")
    let ticker = localStorage.getItem("ticker")
    let comments = []

    // Fill in subreddit and ticker names
    document.getElementById("stock-ticker").textContent = ticker
    document.getElementById("subreddit-id").textContent = subreddit

    // Load appropriate files
    if (subreddit == "overall") {
        let subreddits = localStorage.getItem("subreddits").split(',')
        

        for (let i=0; i<subreddits.length; i++) {
            let file_name = `https://raw.githubusercontent.com/janash/reddit_stocks/data/daily_data/2023-03-18_${subreddits[i]}_comments.csv`
            
            let subComments = load_file(file_name)
            let processedComments = tickerArray(subComments, subreddits[i], ticker)
            comments = comments.concat(processedComments)
        }
    }
    else {
        let file_name = `https://raw.githubusercontent.com/janash/reddit_stocks/data/daily_data/2023-03-18_${subreddit}_comments.csv`
        let subComments = load_file(file_name)
        let processedComments = tickerArray(subComments, subreddit, ticker)
        comments = processedComments
    }

    let divString = ""
    // Create cards for each comment
    for (let i=0; i<comments.length; i++) {
        divString += `<div class="card mb-3">
        <div class="card-header">
          r/${comments[i][10]}
        </div>
        <div class="card-body">
            <h3 class="card-title">${comments[i][1]}</h3>
            <blockquote class="blockquote">
                ${comments[i][2]}
            </blockquote>
            <p class="text-muted">Sentiment</p>
            <div class="d-flex justify-content-around">
                <button type="button" class="btn btn-success">${comments[i][8]}</button>
                <button type="button" class="btn btn-secondary">${comments[i][7]}</button>
                <button type="button" class="btn btn-danger">${comments[i][6]}</button>
                <button type="button" class="btn btn-outline-primary">${comments[i][9]}</button>
            </div>
            <div class="row mt-5">
                <div class="col">
                    <footer class="blockquote-footer">${comments[i][3]}</footer>
                </div>
                <div class="col">
                <footer class="blockquote-footer">See in context <cite title="permalink"><a href="https://reddit.com${comments[i][5]}">permalink</a></cite></footer>
            </div>
            </div>
        </div>
    </div>`
    }

    document.getElementById("cardDiv").innerHTML = divString
    

})