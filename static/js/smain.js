
const url = window.location.href
const searchForm = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')
const resultsBox = document.getElementById('results-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const sendSearchData = (diagnostic) => {
    $.ajax({
        type: 'POST',
        url:'search/',
        data:{
            'csrfmiddlewaretoken' : csrf,
            'diagnostic': diagnostic,
        },
        success:(res) => {
            console.log(res.data)
            const data = res.data
            if (Array.isArray(data)) {
                resultsBox.innerHTML = ""
                data.forEach(diagnostic=> {
                    resultsBox.innerHTML += `
                        <a href="/diagnostic/${diagnostic.code}" class="item">
                            <div class="row">
                                <div class="col-11">
                                    <h5 class="center-align">${diagnostic.name}</h5>
                                </div>
                            </div>
                        </a>`
                })
            } else {
                if(searchInput.value.length > 0){
                    resultsBox.innerHTML = `<b>${data}</b>`
                } else {
                    resultsBox.classList.add('not-visible')
                }
            }
        },
        error:(err) => {
            console.log(err)
        }
    })

}

searchInput.addEventListener('keyup', e=>{
    if(resultsBox.classList.contains('not-visible')){
        resultsBox.classList.remove('not-visible')
    }
    sendSearchData(e.target.value)
})