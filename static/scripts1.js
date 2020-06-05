// JS for the order create page

document.addEventListener("DOMContentLoaded", () => {
    let menuHeader = document.querySelector('.menuHeader')
    let menu = document.querySelector('table')
    let alert = document.querySelector(".alert") ? document.querySelector(".alert") : ''
    let bannerImage = document.querySelector(".hero-image")

    //select pasta
    document.querySelector('#Pasta').classList.add('selected')
    menuHeader.querySelector('p[data-section="Pasta"]').style.fontWeight = 'bold'

    // ----------------------------------------------------------------------------------------------------------------------------
    // configure buttons
    menuHeader.querySelectorAll('p').forEach(button => {
      button.addEventListener("click", e => {
        // section names are stored as data attributes in each header label
        //remove previous bolding and selected section
        var previous = document.querySelector('.selected')
        menuHeader.querySelector(`p[data-section="${previous.id}"]`).style.fontWeight = ''
        previous.classList.remove('selected')

        //add bolding and visibility to current section
        var targetCategory = e.target.dataset.section
        bannerImage.style.backgroundImage = `linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url(static/images/${targetCategory}_banner.jpg)`
        bannerImage.querySelector('h1').innerHTML = targetCategory
        var sectionToDisplay = document.getElementById(`${targetCategory}`)
        e.target.style.fontWeight = 'bold'
        sectionToDisplay.classList.add('selected')
      })
    })

    menu.querySelectorAll('button').forEach(button => {
      button.addEventListener('click', e => {
        itemId = e.target.dataset.itemid
        window.location.href = `addGeneralItem/${itemId}/`
      })
    })

    //configure alert button if there
    alert ? alert.querySelector('button').onclick = () => window.location.href = "viewCart" : ''

// end of DOMcontentLoaded
})
