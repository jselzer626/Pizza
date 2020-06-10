document.addEventListener("DOMContentLoaded", () => {

  //editing display of total
  let total = document.querySelector("#orderTotalRaw") ? parseFloat(document.querySelector("#orderTotalRaw").innerHTML).toFixed(2) : ''
  let headerSpace = document.querySelector(".specialHeader")

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

  let footer = document.querySelector('tfoot') ? document.querySelector('tfoot') : ''
  if (footer) {
      let paymentDetails = document.querySelector(".stripe-button")
      footer.querySelector('button').onclick = () => {
      document.querySelector('#paymentConfirm').style.display="block"
      }
  }

  headerSpace.querySelector('button').addEventListener('click', () => {
    headerSpace.querySelector('a').click()
  })

})
