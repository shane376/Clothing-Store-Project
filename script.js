//Handle add to cart functionality
function addToCart(productId) {
    let quantity = 1;
    fetch('/add_to_cart', {
        method: 'POST',
        headers: {
            'content-Type': 'application/json'
        },
        body: JSON.stringify({product_id: productId, quantity: quantity})
    })
    .then(response => response.json())
    .then(data => {
        alert(data.status)
    });
}

//Handle checkout functionality
function checkout() {
    let cartData = {};
    let totalAmount = 100;
    fetch('/checkout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({cart: cartData, total: totalAmount})
    })
    .then(response => response.json())
    .then(data => {
        alert(data.status);
    });
}