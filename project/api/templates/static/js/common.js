const StorageKeys = {
  clientId: "aurea_client_id",
  cartId: "aurea_cart_id",
  cardId: "aurea_card_id"
};

const Store = {
  getNumber(key) {
    const value = Number(localStorage.getItem(key));
    return Number.isInteger(value) && value > 0 ? value : null;
  },
  setNumber(key, value) {
    if (value !== null && value !== undefined) localStorage.setItem(key, String(value));
  },
  remove(key) { localStorage.removeItem(key); },
  getClientId() { return this.getNumber(StorageKeys.clientId); },
  setClientId(id) { this.setNumber(StorageKeys.clientId, id); },
  getCartId() { return this.getNumber(StorageKeys.cartId); },
  setCartId(id) { this.setNumber(StorageKeys.cartId, id); },
  clearCart() { this.remove(StorageKeys.cartId); },
  getCardId() { return this.getNumber(StorageKeys.cardId); },
  setCardId(id) { this.setNumber(StorageKeys.cardId, id); }
};

function money(value) {
  return Number(value || 0).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function showToast(message, type = "success") {
  const root = document.getElementById("toast-root");
  if (!root) return;
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  root.appendChild(toast);
  setTimeout(() => toast.remove(), 3400);
}

function setActiveNav() {
  const current = window.location.pathname || "/";
  document.querySelectorAll("[data-nav]").forEach((link) => {
    const target = link.getAttribute("href");
    link.classList.toggle("active", target === current);
  });
}

function updateNavCartCount(quantity) {
  const badge = document.getElementById("nav-cart-count");
  if (badge) badge.textContent = String(quantity || 0);
}

async function refreshNavCart() {
  const clientId = Store.getClientId();
  const cartId = Store.getCartId();
  if (!clientId || !cartId) {
    updateNavCartCount(0);
    return;
  }

  try {
    const cart = await Api.getCart(clientId, cartId);
    const total = (cart.produto_carrinho || []).reduce((sum, item) => sum + Number(item.quantidade || 0), 0);
    updateNavCartCount(total);
  } catch (_) {
    updateNavCartCount(0);
  }
}

function initMobileMenu() {
  const button = document.getElementById("mobile-menu-button");
  const nav = document.getElementById("mobile-nav");
  if (!button || !nav) return;
  button.addEventListener("click", () => {
    const isOpen = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!isOpen));
    nav.hidden = isOpen;
  });
}

setActiveNav();
initMobileMenu();
refreshNavCart();
