document.addEventListener("DOMContentLoaded", () => {

  //editing display of total
  let total = document.querySelector("#orderTotalRaw") ? parseFloat(document.querySelector("#orderTotalRaw").innerHTML).toFixed(2) : ''
  total ? document.querySelector("#orderTotalClean").innerHTML += total : ''

  //configure delete buttons
  document.querySelectorAll('.fa-trash').forEach(button => {
    button.addEventListener('click', e => {
      var itemToDelete = e.target.id
      var deleteForm = document.querySelector("#deleteForm")
      deleteForm.action = `deleteItem/${itemToDelete}/`
      deleteForm.submit()
    })
  })

  //if empty message is displaying (Cart is empty) then configure menu redirect button
  let menuRedirect = document.querySelector('#emptyMessage') ? document.querySelector('#emptyMessage') : ''
  menuRedirect ? menuRedirect.querySelector('button').onclick = () => window.location.href = "loadMenu" : ''

  //populate stripe widget with order number and payment amount
  let footer = document.querySelector('tfoot')
  let paymentDetails = document.querySelector(".stripe-button")
  footer.querySelector('button').onclick = () => {
    document.querySelector('#paymentConfirm').style.display="block"
    //var orderId = document.querySelector('#orderNumber') ? document.querySelector('#orderNumber').dataset.order : ''
    //orderId ? paymentDetails.dataset.description = `Order ${orderId}` : ''
    total ? paymentDetails.dataset.amount = total * 100 : ''
  }



})
