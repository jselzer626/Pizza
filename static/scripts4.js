document.addEventListener("DOMContentLoaded", () => {

  let orderList = document.querySelector("#orderList") ? document.querySelector("#orderList") : ''
  let deleteForm = document.querySelector("#deleteForm")
  let showCompletedButton = document.querySelector("button[data-target='#completedOrders']")
  showCompletedButton.onclick = e => {
    e.target.ariaExpanded == 'true' ? e.target.innerHTML = "Show Completed Orders" : e.target.innerHTML = "Hide Completed Orders"
  }

  if (orderList) {
    orderList.querySelectorAll("a[data-action='delete']").forEach(link => {
      link.addEventListener('click', e => {
        var url = e.target.dataset.link
        deleteForm.action = url
        console.log(deleteForm)
        deleteForm.submit()
      })
    })
  }
})
