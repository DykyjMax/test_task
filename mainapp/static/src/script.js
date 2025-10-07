document.addEventListener('click', async (e) => {
    if (e.target.classList.contains('add-to-cart')) {
      e.preventDefault();
  
      const productItem = e.target.closest('.product-item');
      const quantityInput = productItem.querySelector('input[name="quantity"]');
      const qty = quantityInput && quantityInput.value ? quantityInput.value : 1;
      const id = e.target.dataset.productId;
      
  
      const csrftoken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
  
      await fetch('/cart/add/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `product_id=${id}&quantity=${qty}`
      });
  
      alert('Товар додано у корзину');
    }
  });