// conditionally show menu items based on type of category
componentsToHide = {"Pasta": ["toppings", "extraCheese", "sandwichToppings", "size"],
                    "Pizza": ["extraCheese", "sandwichToppings"],
                    "Salads": ["toppings", "extraCheese", "sandwichToppings", "size"],
                    "Sandwiches": ["toppings"],
                    "Platters": ["toppings", "extraCheese", "sandwichToppings"]}

document.addEventListener("DOMContentLoaded", () => {

    let sizeSelector = document.querySelector("#div_id_size") ? document.querySelector("#div_id_size") : ''
    let category = document.querySelector("#category").innerHTML
    //cheeseSteak is a context variable that indicates whether or not the sandiwch toppings select should be displayed (only available if user selects cheesesteak)
    let cheeseSteak = document.querySelector("#cheeseSteak").innerHTML

    let hideMenuComponents = category => {

          componentsToHide[category].forEach(component => {
              document.querySelector(`#div_id_${component}`).style.display = "none"
              })
          }

    hideMenuComponents(category)
    // determine whether or not to display cheesesteak toppings
    category == "Sandwiches" ? cheeseSteak == "False" ? document.querySelector("#div_id_sandwichToppings").style.display = "none" : '' : ''

    //configure back button
    document.querySelector('button').addEventListener('click', () => window.location.href = "loadMenu")

    //remove none option from size select drop down
    if (sizeSelector) {
      sizeSelector.querySelector('option[value="SM"]').setAttribute('selected', true)
      sizeSelector.querySelector('option').style.display="none"
    }
})
