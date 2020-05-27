// JS for the order create page

document.addEventListener("DOMContentLoaded", () => {
    let menuHeader = document.querySelector('.menuHeader')
    let menu = document.querySelector('table')
    let alert = document.querySelector(".alert") ? document.querySelector(".alert") : ''

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
        var sectionToDisplay = document.getElementById(`${e.target.dataset.section}`)
        e.target.style.fontWeight = 'bold'
        sectionToDisplay.classList.add('selected')
      })
    })

    menu.querySelectorAll('button').forEach(button => {
      button.addEventListener('click', e => {
        itemId = e.target.dataset.itemid
        window.location.href = `addGeneralItem?item=${itemId}`
      })
    })

    //configure alert button if there
    alert ? alert.querySelector('button').onclick = () => window.location.href = "viewCart" : ''

// end of DOMcontentLoaded
})
