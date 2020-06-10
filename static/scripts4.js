document.addEventListener("DOMContentLoaded", () => {

  let orderList = document.querySelector("#orderList") ? document.querySelector("#orderList") : ''
  let deleteForm = document.querySelector("#deleteForm")

  console.log(orderList)

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
