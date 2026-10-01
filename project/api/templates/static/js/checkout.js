let checkoutItems = [];

async function loadCheckout() {
  const clientId = Store.getClientId();
  const cartId = Store.getCartId();
  document.getElementById("checkout-client-label").textContent = clientId ? `Cliente #${clientId}` : "Cliente não definido";

  if (!clientId || !cartId) {
    document.getElementById("checkout-cart").innerHTML = `<div class="empty-state">Não há uma sacola pronta para finalizar.</div>`;
    return;
  }

  try {
    const [cart, products] = await Promise.all([Api.getCart(clientId, cartId), Api.getProducts()]);
    const byId = new Map(products.map((product) => [Number(product.id_prod), product]));
    checkoutItems = (cart.produto_carrinho || []).map((item) => {
      const product = byId.get(Number(item.id_prod));
      return { ...item, name: product?.nome || `Produto #${item.id_prod}`, price: Number(product?.preco || 0) };
    });
    const total = checkoutItems.reduce((sum, item) => sum + Number(item.price) * Number(item.quantidade), 0);
    document.getElementById("checkout-cart").innerHTML = checkoutItems.length
      ? checkoutItems.map((item) => `
        <div class="checkout-item">
          <div><strong>${escapeHtml(item.name)}</strong><span>${item.quantidade} × ${money(item.price)}</span></div>
          <strong>${money(Number(item.price) * Number(item.quantidade))}</strong>
        </div>`).join("")
      : `<div class="empty-state">Sua sacola está vazia.</div>`;
    document.getElementById("checkout-total-price").textContent = money(total);

    const savedCard = Store.getCardId();
    if (savedCard) document.getElementById("checkout-card-id").value = savedCard;
  } catch (error) {
    document.getElementById("checkout-cart").innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
  }
}

document.getElementById("checkout-form")?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const clientId = Store.getClientId();
  const cardId = Number(document.getElementById("checkout-card-id")?.value);
  if (!clientId || !Number.isInteger(cardId) || cardId < 1) {
    showToast("Informe uma conta e um cartão válidos.", "error");
    return;
  }

  try {
    await Api.checkout(clientId, cardId);
    Store.setCardId(cardId);
    Store.clearCart();
    document.getElementById("checkout-result").classList.remove("hidden");
    document.getElementById("checkout-result").textContent = "Compra confirmada. O pedido já foi registrado no seu histórico.";
    showToast("Compra realizada com sucesso.");
    document.getElementById("checkout-form").classList.add("hidden");
    updateNavCartCount(0);
    setTimeout(() => { window.location.href = "/historico"; }, 900);
  } catch (error) {
    showToast(error.message, "error");
  }
});

loadCheckout();
