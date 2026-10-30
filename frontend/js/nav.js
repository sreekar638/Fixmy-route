// FixRoute Shared Navigation, Auth Modals & Toast Manager

document.addEventListener("DOMContentLoaded", () => {
  initNavbar();
  initAuthModals();
});

function initNavbar() {
  const authContainer = document.getElementById("nav-auth-container");
  const mobileToggle = document.getElementById("mobile-menu-toggle");
  const navLinks = document.getElementById("nav-links");

  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener("click", () => {
      navLinks.classList.toggle("open");
    });
  }

  function renderAuthUI() {
    if (!authContainer) return;
    const user = window.fixRoute.user;
    if (user) {
      authContainer.innerHTML = `
        <div style="display:flex; align-items:center; gap:0.75rem;">
          <a href="/dashboard.html" class="btn btn-outline btn-sm" title="User Dashboard">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="7" r="4"/><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/></svg>
            ${escapeHTML(user.full_name ? user.full_name.split(' ')[0] : 'Citizen')}
          </a>
          ${user.role === 'admin' ? '<a href="/admin.html" class="btn btn-navy btn-sm">Admin</a>' : ''}
          <button id="nav-logout-btn" class="btn btn-outline btn-sm" style="color:var(--error); border-color:#FECACA;">Logout</button>
        </div>
      `;
      document.getElementById("nav-logout-btn")?.addEventListener("click", () => {
        window.fixRoute.clearSession();
        showToast("You have been signed out.", "info");
        setTimeout(() => window.location.reload(), 400);
      });
    } else {
      authContainer.innerHTML = `
        <button id="nav-signin-btn" class="btn btn-outline btn-sm">Sign In</button>
        <button id="nav-getstarted-btn" class="btn btn-primary btn-sm">Get Started</button>
      `;
      document.getElementById("nav-signin-btn")?.addEventListener("click", () => openAuthModal("login"));
      document.getElementById("nav-getstarted-btn")?.addEventListener("click", () => openAuthModal("register"));
    }
  }

  renderAuthUI();
  window.addEventListener("fixroute:auth-change", renderAuthUI);
}

// Auth Modals logic
function initAuthModals() {
  let modalEl = document.getElementById("auth-modal");
  if (!modalEl) {
    modalEl = document.createElement("div");
    modalEl.id = "auth-modal";
    modalEl.className = "modal-overlay";
    modalEl.innerHTML = `
      <div class="modal-dialog">
        <button class="modal-close" onclick="closeAuthModal()">&times;</button>
        <div id="auth-modal-content"></div>
      </div>
    `;
    document.body.appendChild(modalEl);
  }
}

function openAuthModal(mode = "login") {
  const modalEl = document.getElementById("auth-modal");
  const contentEl = document.getElementById("auth-modal-content");
  if (!modalEl || !contentEl) return;

  if (mode === "login") {
    contentEl.innerHTML = `
      <h3 class="modal-title">Sign In to FixRoute</h3>
      <p style="color:var(--text-muted); margin-bottom:1.5rem; font-size:0.925rem;">
        Access your saved problem routes, evidence checklists, and complaint tracker.
      </p>
      <form id="auth-login-form" onsubmit="handleLogin(event)">
        <div style="margin-bottom:1rem;">
          <label style="display:block; font-size:0.875rem; font-weight:600; margin-bottom:0.35rem;">Email Address</label>
          <input type="email" id="login-email" class="form-input" required placeholder="you@example.com">
        </div>
        <div style="margin-bottom:1.5rem;">
          <label style="display:block; font-size:0.875rem; font-weight:600; margin-bottom:0.35rem;">Password</label>
          <input type="password" id="login-password" class="form-input" required placeholder="••••••••">
        </div>
        <div id="login-error" class="alert alert-danger" style="display:none;"></div>
        <button type="submit" class="btn btn-primary" style="width:100%; margin-bottom:1rem;">Sign In</button>
        <p style="font-size:0.875rem; text-align:center; color:var(--text-muted);">
          Don't have an account? <a href="javascript:void(0)" onclick="openAuthModal('register')">Register for free</a>
        </p>
      </form>
    `;
  } else {
    contentEl.innerHTML = `
      <h3 class="modal-title">Create Your FixRoute Account</h3>
      <p style="color:var(--text-muted); margin-bottom:1.5rem; font-size:0.925rem;">
        Keep your grievance routes organized and track dispute resolutions securely.
      </p>
      <form id="auth-register-form" onsubmit="handleRegister(event)">
        <div style="margin-bottom:1rem;">
          <label style="display:block; font-size:0.875rem; font-weight:600; margin-bottom:0.35rem;">Full Name</label>
          <input type="text" id="reg-name" class="form-input" required placeholder="Sreekar Founder">
        </div>
        <div style="margin-bottom:1rem;">
          <label style="display:block; font-size:0.875rem; font-weight:600; margin-bottom:0.35rem;">Email Address</label>
          <input type="email" id="reg-email" class="form-input" required placeholder="you@example.com">
        </div>
        <div style="margin-bottom:1.5rem;">
          <label style="display:block; font-size:0.875rem; font-weight:600; margin-bottom:0.35rem;">Password (min. 8 characters)</label>
          <input type="password" id="reg-password" class="form-input" required minlength="8" placeholder="••••••••">
        </div>
        <div id="reg-error" class="alert alert-danger" style="display:none;"></div>
        <button type="submit" class="btn btn-primary" style="width:100%; margin-bottom:1rem;">Create Free Account</button>
        <p style="font-size:0.875rem; text-align:center; color:var(--text-muted);">
          Already have an account? <a href="javascript:void(0)" onclick="openAuthModal('login')">Sign in here</a>
        </p>
      </form>
    `;
  }

  modalEl.classList.add("open");
}

function closeAuthModal() {
  document.getElementById("auth-modal")?.classList.remove("open");
}

async function handleLogin(e) {
  e.preventDefault();
  const email = document.getElementById("login-email").value.trim();
  const password = document.getElementById("login-password").value;
  const errBox = document.getElementById("login-error");
  errBox.style.display = "none";

  try {
    await window.fixRoute.login(email, password);
    closeAuthModal();
    showToast("Welcome back! Signed in successfully.", "success");
  } catch (err) {
    errBox.textContent = err.message || "Failed to sign in. Please verify your credentials.";
    errBox.style.display = "flex";
  }
}

async function handleRegister(e) {
  e.preventDefault();
  const name = document.getElementById("reg-name").value.trim();
  const email = document.getElementById("reg-email").value.trim();
  const password = document.getElementById("reg-password").value;
  const errBox = document.getElementById("reg-error");
  errBox.style.display = "none";

  try {
    await window.fixRoute.register(email, name, password);
    closeAuthModal();
    showToast("Account created successfully! Welcome to FixRoute.", "success");
  } catch (err) {
    errBox.textContent = err.message || "Registration failed. Please try again.";
    errBox.style.display = "flex";
  }
}

// Global Toast notification
function showToast(message, type = "info") {
  let toastContainer = document.getElementById("toast-container");
  if (!toastContainer) {
    toastContainer = document.createElement("div");
    toastContainer.id = "toast-container";
    toastContainer.style.cssText = "position:fixed; bottom:1.5rem; right:1.5rem; z-index:9999; display:flex; flex-direction:column; gap:0.5rem; pointer-events:none;";
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement("div");
  toast.className = `alert alert-${type === 'error' ? 'danger' : type}`;
  toast.style.cssText = "pointer-events:auto; box-shadow:0 10px 15px -3px rgba(0,0,0,0.1); margin-bottom:0; min-width:280px; max-width:400px; animation: slideIn 0.25s ease;";
  toast.innerHTML = `<span>${escapeHTML(message)}</span>`;
  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transition = "opacity 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function escapeHTML(str) {
  if (!str) return "";
  return String(str).replace(/[&<>'"]/g, 
    tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
  );
}
