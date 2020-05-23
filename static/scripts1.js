// JS for the order create page

document.addEventListener("DOMContentLoaded", () => {
    let menuHeader = document.querySelector('.menuHeader')

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

// end of DOMcontentLoaded
})
