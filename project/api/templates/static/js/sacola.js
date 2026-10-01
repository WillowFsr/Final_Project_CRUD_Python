let cartProducts = [];

function renderCart() {
  const root = document.getElementById("cart-content");
  if (!root) return;
  if (!cartProducts.length) {
    root.innerHTML = `<div class="empty-state">Sua sacola está vazia. <a href="/loja" class="inline-arrow">Ir para a loja →</a></div>`;
    document.getElementById("cart-total-items").textContent = "0";
    document.getElementById("cart-total-price").textContent = money(0);
    return;
  }

  const totalItems = cartProducts.reduce((sum, item) => sum + Number(item.quantity), 0);
  const totalValue = cartProducts.reduce((sum, item) => sum + Number(item.price) * Number(item.quantity), 0);
  document.getElementById("cart-total-items").textContent = String(totalItems);
  document.getElementById("cart-total-price").textContent = money(totalValue);
  root.innerHTML = cartProducts.map((item) => `
    <div class="cart-row">
      <div class="cart-thumb">${String(item.name).charAt(0).toUpperCase()}</div>
      <div>
        <h3>${escapeHtml(item.name)}</h3>
        <p>Quantidade: ${item.quantity} · ${money(item.price)} cada</p>
      </div>
      <strong class="cart-row-price">${money(Number(item.price) * Number(item.quantity))}</strong>
      <button class="remove-button" type="button" data-id="${item.id_prod}">Remover</button>
    </div>`).join("");

  root.querySelectorAll(".remove-button").forEach((button) => {
    button.addEventListener("click", () => removeItem(Number(button.dataset.id)));
  });
}

async function loadCartPage() {
  const clientId = Store.getClientId();
  const cartId = Store.getCartId();
  const label = document.getElementById("cart-session-label");
  if (clientId) {
    label.textContent = `Cliente #${clientId}`;
  }
  if (!clientId || !cartId) {
    cartProducts = [];
    renderCart();
    return;
  }

  try {
    const [cart, products] = await Promise.all([Api.getCart(clientId, cartId), Api.getProducts()]);
    const byId = new Map(products.map((product) => [Number(product.id_prod), product]));
    cartProducts = (cart.produto_carrinho || []).map((item) => {
      const product = byId.get(Number(item.id_prod));
      return {
        id_prod: item.id_prod,
        quantity: Number(item.quantidade),
        name: product?.nome || `Produto #${item.id_prod}`,
        price: Number(product?.preco || 0)
      };
    });
    renderCart();
    await refreshNavCart();
  } catch (error) {
    showToast(error.message, "error");
    renderCart();
  }
}

async function removeItem(productId) {
  const clientId = Store.getClientId();
  if (!clientId) return;
  try {
    await Api.removeCartItem(clientId, productId);
    showToast("Produto removido da sacola.");
    await loadCartPage();
  } catch (error) {
    showToast(error.message, "error");
  }
}

loadCartPage();
