document.addEventListener("DOMContentLoaded", () => {

  //editing display of total
  let total = document.querySelector("#orderTotalRaw") ? parseInt(document.querySelector("#orderTotalRaw").innerHTML).toFixed(2) : ''
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

  //properly display order total - the value returned from the db sometimes trails
  total ? document.querySelector("#orderTotalDisplay").innerHTML = total : ''


  headerSpace.querySelector('button').addEventListener('click', () => {
    headerSpace.querySelector('a').click()
  })

})
