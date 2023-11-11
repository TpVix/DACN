var updateBtn = document.getElementsByClassName("update-cart")
var quantity = document.getElementsByClassName("quantity_cart")
for(i = 0; i < updateBtn.length ; i ++){
    updateBtn[i].addEventListener('click', function(){
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log('ProductID: ', productID, 'Action: ', action)
        if(user === "AnonymousUser"){
            console.log('Chưa đăng nhập')
        }else {
            updateUserOrder(productID, action)
        }
    })
}

for(i = 0; i < quantity.length ; i ++){
    quantity[i].addEventListener('click', function(){
        var productID = this.dataset.product
        var action = this.dataset.action
        if(user === "AnonymousUser"){
            console.log('Chưa đăng nhập')
        }else {
            updateUserOrder(productID, action)
        }
    })
}

function updateUserOrder(productID, action){
    console.log('Đã đăng nhập')
    var url = '/update_item/'
    fetch(url,{
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body: JSON.stringify({'productID': productID, 'action': action})
    })
    .then((response)=>{
     return response.json()
    })
    .then((data)=>{
        console.log('data', data)
        location.reload()
    })
}