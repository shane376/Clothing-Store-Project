//Handle add to cart functionality
function addToCart(productId) {
    fetch('/add_to_cart', {
        method: 'POST',
        headers: {
            'content-Type': 'application/json'
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: 1
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.status ? 'Product added to cart!' : data.error);
    })
    .catch(error => console.error('Error adding product to cart:', error));
}

//Handle checkout functionality
function checkout() {
    fetch('/checkout', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        alert(data.status ? 'Checkout sucessuful!' : data.error);
    })
    .catch(error => console.error('Error during checkout:', error));
}