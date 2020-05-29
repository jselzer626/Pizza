document.addEventListener("DOMContentLoaded", () => {

  //editing display of total
  let total = document.querySelector("#orderTotalRaw") ? parseFloat(document.querySelector("#orderTotalRaw").innerHTML).toFixed(2) : ''
  total ? document.querySelector("#orderTotalClean").innerHTML += total : ''

  //configure delete buttons
  document.querySelectorAll('.dropdown-item[data-action="delete"]').forEach(link => {
    link.addEventListener('click', e => {
      var deleteForm = document.querySelector("#deleteForm")
      deleteForm.action = e.target.dataset.link
      deleteForm.submit()
    })
  })

  //if empty message is displaying (Cart is empty) then configure menu redirect button
  let menuRedirect = document.querySelector('#emptyMessage') ? document.querySelector('#emptyMessage') : ''
  menuRedirect ? menuRedirect.querySelector('button').onclick = () => window.location.href = "loadMenu" : ''

  let footer = document.querySelector('tfoot')
  let paymentDetails = document.querySelector(".stripe-button")
  footer.querySelector('button').onclick = () => {
    document.querySelector('#paymentConfirm').style.display="block"
  }

  document.querySelector('button').addEventListener('click', () => {
    window.location.href = "loadMenu"
  })


})
