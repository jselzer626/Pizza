// JS for the order create page

document.addEventListener("DOMContentLoaded", () => {
    let menuHeader = document.querySelector('.menuHeader')
    let menu = document.querySelector('table')
    let alert = document.querySelector(".alert") ? document.querySelector(".alert") : ''
    let bannerImage = document.querySelector(".hero-image")
    let large = document.querySelector("#large")
    let small = document.querySelector("#small")
    let desktopAddButton = document.querySelectorAll("#desktopItemAddButton")
    let mobileAddButton = document.querySelectorAll("#mobileItemAddButton")

    // ----------------------------------------------------------------------------------------------------------------------------
    // configure buttons
    menuHeader.querySelectorAll('p').forEach(button => {
      button.addEventListener("click", e => {
        // section names are stored as data attributes in each header label
        //remove previous bolding and selected section
        var previous = document.querySelector('.selected') || ''
        if (previous) {
          menuHeader.querySelector(`p[data-section="${previous.id}"]`).style.fontWeight = ''
          previous.classList.remove('selected')
        }

        //add bolding and visibility to current section
        var targetCategory = e.target.dataset.section
        targetCategory == "Pizza" ? document.querySelector(".notice").style.display = "block" : document.querySelector(".notice").style.display = "none"
        bannerImage.style.backgroundImage = `linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url(/static/images/${targetCategory}_banner.jpg)`
        bannerImage.querySelector('h1').innerHTML = targetCategory
        var sectionToDisplay = document.getElementById(`${targetCategory}`)
        e.target.style.fontWeight = 'bold'
        sectionToDisplay.classList.add('selected')

        //change small and large to regular if those sizes don't exist for category selected
        if (targetCategory == "Salads" || targetCategory == "Pasta") {
          large.style.display = "none"
          small.colSpan = 2
          small.innerHTML = "Regular"
          small.style.textAlign = "center"
        } else {
          large.style.display = "block"
          small.colSpan = 1
          small.innerHTML = "Small"
          small.style.textAlign = "left"
        }
      })
    })

    //select pasta to start
    menuHeader.querySelector('p').click()

    menu.querySelectorAll('button').forEach(button => {
      button.onclick = e => {
        e.target.parentElement.querySelector('a').click()
      }
    })

    //configure alert button if there
    alert ? alert.querySelector('button').onclick = () => alert.querySelector('a').click() : ''

// end of DOMcontentLoaded
})
