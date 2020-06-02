// conditionally show menu items based on type of category
let componentsToHide = {"Pasta": ["toppings", "extraCheese", "sandwichToppings", "size"],
                    "Pizza": ["extraCheese", "sandwichToppings"],
                    "Salads": ["toppings", "extraCheese", "sandwichToppings", "size"],
                    "Sandwiches": ["toppings"],
                    "Platters": ["toppings", "extraCheese", "sandwichToppings"]}

document.addEventListener("DOMContentLoaded", () => {

    let toppings = []
    let sizeSelector = document.querySelector("#div_id_size") ? document.querySelector("#div_id_size") : ''
    let toppingSelector = document.querySelector("#div_id_toppings") ? document.querySelector("#div_id_toppings") : ''
    let category = document.querySelector("#category").innerHTML
    //cheeseSteak is a context variable that indicates whether or not the sandiwch toppings select should be displayed (only available if user selects cheesesteak)
    let cheeseSteak = document.querySelector("#cheeseSteak").innerHTML
    let toppingSelectBox = document.querySelector("#id_toppings") ? document.querySelector("#id_toppings") : ''

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
    // this fixes the menu item selection - user can go back to the menu page to select a different item
    // document.querySelector("select[name='item']").setAttribute("disabled", true)

    // determine whether or not to display cheesesteak toppings
    category == "Sandwiches" ? cheeseSteak == "False" ? document.querySelector("#div_id_sandwichToppings").style.display = "none" : '' : ''

    //configure back button
    document.querySelector('button').addEventListener('click', () => window.location.href = "loadMenu")

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
