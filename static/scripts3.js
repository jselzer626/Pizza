// conditionally show menu items based on type of category
let componentsToHide = {"Pasta": ["toppings", "extraCheese", "sandwichToppings", "size"],
                    "Pizza": ["extraCheese", "sandwichToppings"],
                    "Salads": ["toppings", "extraCheese", "sandwichToppings", "size"],
                    "Sandwiches": ["toppings"],
                    "Platters": ["toppings", "extraCheese", "sandwichToppings"]}

document.addEventListener("DOMContentLoaded", () => {

    let toppings = []
    let action = document.querySelector('h1').dataset.action
    //if this page is being accessed to edit an existing order item
    let currentToppings = (Array.from(document.querySelector("#id_toppings"))).filter(option => option.selected == true)
    let sizeSelector = document.querySelector("#div_id_size") ? document.querySelector("#div_id_size") : ''
    let toppingSelector = document.querySelector("#div_id_toppings") ? document.querySelector("#div_id_toppings") : ''
    let category = document.querySelector("#category").innerHTML
    // if item is steak and cheese then show sandwichToppings field
    let cheesesteak = document.querySelector("#itemName").dataset.name == "Steak + Cheese Sandwich" ? true : false
    let toppingSelectBox = document.querySelector("#id_toppings") ? document.querySelector("#id_toppings") : ''

    // make add item big if mobile
    window.screen.width < 600 ? document.querySelector("#submit-id-submit").className += " btn-lg" : ''

    let hideMenuComponents = category => {

          componentsToHide[category].forEach(component => {
              document.querySelector(`#div_id_${component}`).style.display = "none"
              })
          }

    let updateToppings = (chosenToppings, requiredToppings) => {
      return `Selected: (${requiredToppings - chosenToppings} Remaining)`
    }

    let errorDisplay = (messageDisplaySpace, errorIndicationSpace, message) => {
      errorIndicationSpace.style.border = "3px solid red"
      messageDisplaySpace.innerHTML = message
      messageDisplaySpace.style.display = "block"
    }

    let errorMessageClear = (errorDisplaySpace, errorIndicationSpace) => {
      errorDisplaySpace.style.display = "none"
      errorIndicationSpace.style.border = "none"
    }

    // this hides certain parameters for the menu item based on the type of item (i.e. salad has no pizza toppings etc.)
    hideMenuComponents(category)
    category == "Sandwiches" ? !cheesesteak ? document.querySelector("#div_id_sandwichToppings").style.display = "none" : '' : ''
    //change header button to edit if update page
    action == "edit" ? document.querySelector('#submit-id-submit').value = "Update" : ''
    // this fixes the menu item selection - user can go back to the menu page to select a different item
    // document.querySelector("select[name='item']").setAttribute("disabled", true)

    // determine whether or not to display cheesesteak toppings

    //configure back button
    document.querySelector('button').addEventListener('click', () => document.querySelector("#back").click())

    //remove none option from size select drop down
    if (sizeSelector) {
      sizeSelector.querySelector('option[value="SM"]').setAttribute('selected', true)
      sizeSelector.querySelector('option').style.display="none"
    }

    //configure topping option buttons to display selected toppings in space below toppings selector
    if (toppingSelector) {
      var toppingsCount = document.querySelector("#toppingsCount").innerHTML
      toppingSelector.querySelector("label").innerHTML += `<br>(Please choose ${toppingsCount})`
      var toppingDisplayList = document.createElement('ul')
      var header = document.createElement('p')
      var errorSpace = document.createElement('p')
      errorSpace.className = "text-danger"
      header.innerHTML = `Selected: (${toppingsCount} Remaining)`
      header.style.display = "none"
      errorSpace.style.display = "none"
      toppingSelector.append(errorSpace)
      toppingDisplayList.append(header)
      toppingSelector.append(toppingDisplayList)
      toppingSelector.querySelectorAll('option').forEach(selector => {
        selector.addEventListener('click', e => {

          var toppingToAdd = e.target.value
          //clear any error messages
          errorMessageClear(errorSpace, toppingSelectBox)

          //display selected list header if first topping chosen
          header.style.display == "none" ? header.style.display = "block" : ''

          if (!toppings.includes(toppingToAdd) && toppings.length < toppingsCount) {
            toppings.push(toppingToAdd)
            var toppingDisplayItem = document.createElement('li')
            toppingDisplayItem.value = toppingToAdd
            var toppingDeleteButton = document.createElement('i')
            toppingDeleteButton.className = "fas fa-times"

              // configure topping delete button -this updates the array containing topping ID's and removes the li with the topping name from the DOM
              toppingDeleteButton.addEventListener('click', e => {

                errorMessageClear(errorSpace, toppingSelectBox)
                toppings = toppings.filter(topping => topping != e.target.parentElement.value)
                e.target.parentElement.remove()
                toppingSelector.querySelector(`option[value='${e.target.parentElement.value}']`).selected == true ? toppingSelector.querySelector(`option[value='${e.target.parentElement.value}']`).selected = false : ''
                //toppingSelector.querySelector(`[value='${e.target.parentElement.value}']`).selected = true ?   toppingSelector.querySelector(`[value=${e.target.parentElement.value}]`).selected = false : ''
                header.innerHTML = updateToppings(toppings.length, parseInt(toppingsCount))
                toppings.length == 0 ? header.style.display = "none" : ''

              })

            toppingDisplayItem.innerHTML = e.target.innerHTML
            toppingDisplayItem.append(toppingDeleteButton)
            toppingDisplayList.append(toppingDisplayItem)
            header.innerHTML = updateToppings(toppings.length, parseInt(toppingsCount))
          }
          else if (toppings.includes(toppingToAdd))
            errorDisplay(errorSpace, toppingSelectBox, "You already chose that topping")
          else if (toppings.length == toppingsCount)
            errorDisplay(errorSpace, toppingSelectBox, "Max toppings added. Please delete one before adding")
        })
      })

    }
    // if editing the item and item is a pizza than call existing process for each of the selected toppings
    currentToppings.length > 0 ? currentToppings.forEach(option => option.click()) : ''

    document.querySelector('form').onsubmit = e => {
      if (toppings.length != parseInt(toppingsCount)) {
        e.preventDefault()
        errorDisplay(toppingSelector.querySelector(".text-danger"), toppingSelectBox, "Please add more toppings")
      } else {
        toppings.forEach(topping => {
          toppingSelector.querySelector(`option[value="${topping}"]`).selected = true
        })
      }
    }
})
