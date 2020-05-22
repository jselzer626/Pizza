// JS for the order create page

document.addEventListener("DOMContentLoaded", () => {
    let menuHeader = document.querySelector('.menuHeader')


    // ----------------------------------------------------------------------------------------------------------------------------
    // configure buttons
    menuHeader.querySelectorAll('p').forEach(button => {
      button.addEventListener("click", e => {
        // section names are stored as data attributes in each header label
        var sectionToDisplay = document.getElementById(`${e.target.dataset.section}`)
        console.log(sectionToDisplay)
        sectionToDisplay.classList.add('selected')
      })
    })

// end of DOMcontentLoaded
})
